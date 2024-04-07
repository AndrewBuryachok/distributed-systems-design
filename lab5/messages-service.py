from flask import Flask
import hazelcast
import threading
import consul
import uuid
import sys

app = Flask(__name__)

c = consul.Consul(host='127.0.0.1', port=8500)

messages = []

client = hazelcast.HazelcastClient()

_, queue_name = c.kv.get('messages_queue_name')

my_queue = client.get_queue(queue_name['Value'].decode('utf-8'))

@app.route('/', methods=['GET'])
def get():
  return messages

if __name__ == '__main__':
  port = int(sys.argv[1])
  app.run(port=port)
  c.agent.service.register(id=str(uuid.uuid4()), name='messages_service', address='127.0.0.1', port=port)

def consume():
  while True:
    msg = my_queue.take().result()
    print(msg)
    messages.append(msg)

thread = threading.Thread(target=consume)
thread.start()
thread.join()
