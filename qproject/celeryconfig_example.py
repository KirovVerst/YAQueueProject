broker_url = 'amqp://'
result_backend = 'rpc://'
include = ['qproject.tasks']
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True
