from flask import Flask
import hazelcast
import consul
import uuid
import sys

app = Flask(__name__)

c = consul.Consul(host='127.0.0.1', port=8500)

messages = []

client = hazelcast.HazelcastClient()

_, queue_name = c.kv.get('messages_queue_name')

my_queue = client.get_queue(queue_name['Value'].decode('utf-8')).blocking()

@app.route('/', methods=['GET'])
def get():
  for _ in range(5):
    msg = my_queue.take()
    messages.append(msg)
    print(msg)
  return messages

if __name__ == '__main__':
  port = int(sys.argv[1])
  app.run(port=port)
  c.agent.service.register(id=str(uuid.uuid4()), name='messages_service', address='127.0.0.1', port=port)
