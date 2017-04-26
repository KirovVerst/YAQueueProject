import nginx


def create_conf(ip_address, path_to_file):
    c = nginx.Conf()
    django = dict(name='django', port='8000')
    flower = dict(name='flower', port='5555')
    visualizer = dict(name='visualizer', port='8080')

    for server in [django, visualizer, flower]:
        c.add(nginx.Comment(server['name']))
        nginx_server = nginx.Server()
        nginx_server.add(
            nginx.Key('listen', server['port']),
            nginx.Key('server_name', ip_address),
            nginx.Location('/',
                           nginx.Key('proxy_pass', 'http://localhost:{}/'.format(server['port'])),
                           nginx.Key('proxy_redirect', 'off'),
                           nginx.Key('proxy_set_header', 'Host $host'),
                           nginx.Key('proxy_set_header', 'X-Real-IP $remote_addr'),
                           nginx.Key('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for')
                           )
        )
        c.add(nginx_server)
    nginx.dumpf(c, path_to_file)


if __name__ == '__main__':
    create_conf('127.0.0.1', 'qproject_nginx')
