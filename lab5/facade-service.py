from flask import Flask, request, jsonify
import hazelcast
import consul
import requests
import random
import uuid
import sys

app = Flask(__name__)

c = consul.Consul(host='127.0.0.1', port=8500)

client = hazelcast.HazelcastClient()

_, queue_name = c.kv.get('messages_queue_name')

my_queue = client.get_queue(queue_name['Value'].decode('utf-8')).blocking()

def get_service_url(service_name):
  _, services = c.catalog.service(service_name)
  service = random.choice(services)
  address = service['ServiceAddress']
  port = service['ServicePort']
  return f'http://{address}:{port}'

@app.route('/', methods=['GET'])
def get():
  log_response = requests.get(get_service_url('logging_service'))
  msg_response = requests.get(get_service_url('messages_service'))
  return log_response.text + msg_response.text

@app.route('/', methods=['POST'])
def post():
  id = str(uuid.uuid4())
  msg = request.form.get('msg')
  body = {'id': id, 'msg': msg}
  requests.post(get_service_url('logging_service'), data=body)
  my_queue.offer(msg)
  return jsonify(body)

if __name__ == '__main__':
  port = int(sys.argv[1])
  app.run(port=port)
  c.agent.service.register(id=str(uuid.uuid4()), name='facade_service', address='127.0.0.1', port=port)
