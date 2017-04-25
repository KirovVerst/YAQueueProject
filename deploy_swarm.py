import digitalocean
import os
import subprocess
from qproject.config import DO_TOKEN

TAG = 'qproject'

MANAGER_NAME = 'manager-{}'.format(TAG)

client = digitalocean.Manager(token=DO_TOKEN)

WORKER_NUMBER = 1

WORKER_NAMES = list(map(lambda number: "worker-{}-{}".format(number + 1, TAG), range(WORKER_NUMBER)))

WORKER_UFW_PORTS = ["22/tcp", "2376/tcp", "7946/tcp", "7946/udp", "4789/udp"]

MANAGER_UFW_PORTS = WORKER_UFW_PORTS + ["2377/tcp"]

ENV = os.environ.copy()
ENV['PATH'] = '/usr/local/bin/:' + ENV['PATH']


def print_commands(commands):
    print('$ {}'.format(" ".join(commands)))


def call(commands):
    return subprocess.call([" ".join(commands)], env=ENV, shell=True)


def check_output(commands):
    return subprocess.check_output([" ".join(commands)], env=ENV, shell=True)


def create_droplet(droplet_name):
    commands = ['docker-machine', 'create',
                '--driver', 'digitalocean',
                '--digitalocean-image', 'ubuntu-16-04-x64',
                '--digitalocean-access-token', DO_TOKEN,
                droplet_name]
    call(commands)


def get_manager():
    droplets = list(filter(lambda droplet: droplet.name == MANAGER_NAME, client.get_all_droplets()))
    return droplets[0] if len(droplets) > 0 else None


def get_workers():
    droplets = list(filter(lambda droplet: droplet.name in WORKER_NAMES, client.get_all_droplets()))
    return droplets


def ufw_update(ports, node_name):
    connect_commands = ['docker-machine', "ssh", node_name]

    for port in ports:
        commands = connect_commands + ["\"ufw", "allow", "{}\"".format(port)]
        print("$ {}".format(" ".join(commands)))
        call(commands)

    commands = connect_commands + ["\"ufw", "reload\""]
    print_commands(commands)
    result = str(check_output(commands))
    print(result)

    if "not enabled" in result:
        commands = connect_commands + ["\"ufw", "enable\""]
        print_commands(commands)
        call(commands)

    commands = connect_commands + ["\"systemctl", "restart", "docker\""]
    print_commands(commands)
    call(commands)


def create_manager():
    create_droplet(MANAGER_NAME)


def create_workers():
    for worker_name in WORKER_NAMES:
        create_droplet(worker_name)


def init_manager(manager_ip_address):
    commands = ['docker-machine', "ssh", MANAGER_NAME, '"',
                "docker", "swarm", "init",
                "--advertise-addr", manager_ip_address, '"']
    call(commands)


def join_workers(manager_ip_address):
    commands = ['docker', 'swarm', 'join-token', 'worker', '-q']
    token = check_output(commands)
    for worker_name in WORKER_NAMES:
        commands = ['docker-machine', 'ssh', worker_name,
                    '\"',
                    "docker", 'swarm', "join", "--token", token, "{}:2377".format(manager_ip_address)]
        call(commands)


if __name__ == "__main__":
    print("Creating manager ...")
    create_manager()
    print("Creating workers ...")
    create_workers()
    print("UFW issues ...")
    ufw_update(ports=MANAGER_UFW_PORTS, node_name=MANAGER_NAME)
    for worker in WORKER_NAMES:
        ufw_update(ports=WORKER_UFW_PORTS, node_name=worker)
    print("Getting manager instance ...")
    manager = get_manager()
    print("Manager initialization ...")
    init_manager(manager_ip_address=manager.ip_address)
    print("Worker initialization ...")
    join_workers(manager_ip_address=manager.ip_address)
    print("hello")
