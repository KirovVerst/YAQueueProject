import nginx


def create_conf(ip_address, path_to_file):
    c = nginx.Conf()
    c.add(nginx.Comment('django'))
    django_server = nginx.Server()
    django_server.add(
        nginx.Key('listen', '80'),
        nginx.Key('server_name', ip_address),
        nginx.Location('/',
                       nginx.Key('proxy_pass', 'http://localhost:8000/'),
                       nginx.Key('proxy_redirect', 'off'),
                       nginx.Key('proxy_set_header', 'Host $host'),
                       nginx.Key('proxy_set_header', 'X-Real-IP $remote_addr'),
                       nginx.Key('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for')
                       )
    )
    c.add(django_server)
    c.add(nginx.Comment('flower'))
    flower_server = nginx.Server()
    flower_server.add(
        nginx.Key('listen', '5555'),
        nginx.Key('server_name', ip_address),
        nginx.Location('/',
                       nginx.Key('proxy_pass', 'http://localhost:5555/'),
                       nginx.Key('proxy_redirect', 'off'),
                       nginx.Key('proxy_set_header', 'Host $host'),
                       nginx.Key('proxy_set_header', 'X-Real-IP $remote_addr'),
                       nginx.Key('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for')
                       )
    )
    c.add(flower_server)
    c.add(nginx.Comment('visualizer'))
    visualizer_server = nginx.Server()
    visualizer_server.add(
        nginx.Key('listen', '8080'),
        nginx.Key('server_name', ip_address),
        nginx.Location('/',
                       nginx.Key('proxy_pass', 'http://localhost:8080/'),
                       nginx.Key('proxy_redirect', 'off'),
                       nginx.Key('proxy_set_header', 'Host $host'),
                       nginx.Key('proxy_set_header', 'X-Real-IP $remote_addr'),
                       nginx.Key('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for')
                       )
    )
    c.add(visualizer_server)
    nginx.dumpf(c, path_to_file)


if __name__ == '__main__':
    create_conf('127.0.0.1', 'qproject_nginx')
