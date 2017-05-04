import requests
import time
import pika

host = 'http://my.rabbitmq.com'
vhost = 'vhost'
username = 'username'
password = 'password'

# get names of queues
response = requests.get('%s/api/queues' % host, auth=(username, password))
json = response.json()
names = [queue['name'] for queue in json]
filtered_names = [name for name in names if name.startswith('amq.gen')]

# delete selected queues
total = len(filtered_names)
for index, name in enumerate(filtered_names):
    print('%d/%d: %s' % (index+1, total, name))
    requests.delete('%s/api/queues/%s/%s' % (host, vhost, name), auth=(username, password))
