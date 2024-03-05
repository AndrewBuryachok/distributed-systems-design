from flask import Flask, request
import hazelcast

app = Flask(__name__)

client = hazelcast.HazelcastClient()

messages = client.get_map('messages').blocking()

@app.route('/', methods=['GET'])
def get():
  return messages.entry_set()

@app.route('/', methods=['POST'])
def post():
  id = request.form.get('id')
  msg = request.form.get('msg')
  messages.put(id, msg)
  print(msg)
  return ''

if __name__ == '__main__':
  app.run(port=5001)
  # app.run(port=5002)
  # app.run(port=5003)
