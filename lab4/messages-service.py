from flask import Flask
import hazelcast

app = Flask(__name__)

messages = []

client = hazelcast.HazelcastClient()

queue = client.get_queue('messages').blocking()

@app.route('/', methods=['GET'])
def get():
  for _ in range(5):
    msg = queue.take()
    messages.append(msg)
    print(msg)
  return messages

if __name__ == '__main__':
  app.run(port=5004)
  # app.run(port=5005)
