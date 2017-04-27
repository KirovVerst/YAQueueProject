import digitalocean
import os
from time import sleep
from fabric.api import *
from utilts.nginx_conf_generator import create_conf
from qproject.settings import BASE_DIR

try:
    from deploy_config import *
except ImportError:
    from deploy_config_example import *

MANAGER = digitalocean.Manager(token=DO_TOKEN)


def check_configuration():
    print("Checking your droplet configuration ...")
    droplets = MANAGER.get_all_droplets()
    available_name = len(list(filter(lambda droplet: droplet.name == ONE_DROPLET_NAME, droplets))) == 0
    if not available_name:
        print("Error: droplet with name \'{}\' already exists.".format(ONE_DROPLET_NAME))
        exit()
    print("Everything is alright")


def create_droplet():
    """
    Create a digital ocean droplet with configuration that is set in deploy_config.py
    :return: digitalocean droplet
    """

    keys = MANAGER.get_all_sshkeys()
    droplet = digitalocean.Droplet(token=DO_TOKEN,
                                   name=ONE_DROPLET_NAME,
                                   image=ONE_DROPLET_IMAGE,
                                   size_slug=ONE_DROPLET_SIZE,
                                   ssh_keys=keys,
                                   region='nyc2',
                                   backups=False,
                                   tags=['qproject'])
    droplet.create()
    print("Creating of droplet can take about 1 minute. Please, wait for ...")
    sleep(60)
    droplet = get_droplet(ONE_DROPLET_NAME)
    return droplet


def get_droplet(droplet_name):
    droplets = list(filter(lambda droplet: droplet.name == droplet_name, MANAGER.get_all_droplets()))
    if len(droplets) > 0:
        return droplets[0]
    else:
        return digitalocean.Droplet()


commands = {
    'apt': 'apt update',
    'nginx': {
        'install': 'apt install nginx',
        'restart': 'service nginx restart',
        'status': 'service nginx status'
    }
}


def init():
    # check_configuration()
    # droplet = create_droplet()
    droplet = get_droplet(ONE_DROPLET_NAME)
    env.hosts = [droplet.ip_address]
    env.user = 'root'


def deploy():
    droplet = get_droplet(ONE_DROPLET_NAME)
    """
    run(commands['apt'])
    run(commands['nginx']['install'])
    run('rm /etc/nginx/sites-enabled/*')
    run('rm /etc/nginx/sites-available/*')
    local_config = 'qproject-nginx'
    remote_config = '/etc/nginx/sites-available/{}'.format(local_config)
    remote_config_link = '/etc/nginx/sites-enabled/{}'.format(local_config)
    create_conf(droplet.ip_address, local_config)
    put(local_config, remote_config)
    run('ln -s {} {}'.format(remote_config, remote_config_link))
    run(commands['nginx']['restart'])
    """
    run('rm -r ~/*')
    run('git clone https://github.com/KirovVerst/qproject.git')
    put(os.path.join(BASE_DIR, 'variables.env'), '/root/qproject/variables.env')
    with cd('~/qproject'):
        run('docker build -t worker -f Dockerfile.worker .')
        run('docker build -t gateway -f Dockerfile.gateway .')
        run('docker swarm init --advertise-addr={}'.format(droplet.ip_address))
        run('docker stack deploy -c docker-compose.yml qproject')
