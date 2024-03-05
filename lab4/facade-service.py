from flask import Flask, request, jsonify
import hazelcast
import requests
import uuid
import random

app = Flask(__name__)

l_ports = [5001, 5002, 5003]
m_ports = [5004, 5005]

client = hazelcast.HazelcastClient()

queue = client.get_queue('messages').blocking()

@app.route('/', methods=['GET'])
def get():
  l_port = random.choice(l_ports)
  m_port = random.choice(m_ports)
  log_response = requests.get(f'http://localhost:{l_port}')
  msg_response = requests.get(f'http://localhost:{m_port}')
  return log_response.text + msg_response.text

@app.route('/', methods=['POST'])
def post():
  id = str(uuid.uuid4())
  msg = request.form.get('msg')
  body = {"id": id, "msg": msg}
  l_port = random.choice(l_ports)
  requests.post(f'http://localhost:{l_port}', data=body)
  queue.offer(msg)
  return jsonify(body)

if __name__ == '__main__':
  app.run(port=5000)
