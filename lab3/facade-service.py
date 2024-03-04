from flask import Flask, request, jsonify
import requests
import uuid
import random

app = Flask(__name__)

ports = [5001, 5002, 5003]

@app.route('/', methods=['GET'])
def get():
  port = random.choice(ports)
  log_response = requests.get(f'http://localhost:{port}')
  msg_response = requests.get('http://localhost:5004')
  return log_response.text + msg_response.text

@app.route('/', methods=['POST'])
def post():
  id = str(uuid.uuid4())
  msg = request.form.get('msg')
  body = {"id": id, "msg": msg}
  port = random.choice(ports)
  requests.post(f'http://localhost:{port}', data=body)
  return jsonify(body)

if __name__ == '__main__':
  app.run(port=5000)
