from flask import Flask
import hazelcast
import threading

app = Flask(__name__)

messages = []

client = hazelcast.HazelcastClient()

queue = client.get_queue('messages')

@app.route('/', methods=['GET'])
def get():
  return messages

if __name__ == '__main__':
  app.run(port=5004)
  # app.run(port=5005)

def consume():
  while True:
    msg = queue.take().result()
    print(msg)
    messages.append(msg)

thread = threading.Thread(target=consume)
thread.start()
thread.join()
