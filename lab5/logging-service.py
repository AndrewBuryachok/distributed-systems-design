from flask import Flask, request
import hazelcast
import consul
import uuid
import sys

app = Flask(__name__)

c = consul.Consul(host='127.0.0.1', port=8500)

client = hazelcast.HazelcastClient()

_, map_name = c.kv.get('messages_map_name')

my_map = client.get_map(map_name['Value'].decode('utf-8')).blocking()

@app.route('/', methods=['GET'])
def get():
  return my_map.entry_set()

@app.route('/', methods=['POST'])
def post():
  id = request.form.get('id')
  msg = request.form.get('msg')
  my_map.put(id, msg)
  print(msg)
  return ''

if __name__ == '__main__':
  port = int(sys.argv[1])
  app.run(port=port)
  c.agent.service.register(id=str(uuid.uuid4()), name='logging_service', address='127.0.0.1', port=port)
