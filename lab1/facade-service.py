from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
  log_response = requests.get('http://localhost:5001')
  msg_response = requests.get('http://localhost:5002')
  return log_response.text + msg_response.text

@app.route('/', methods=['POST'])
def post():
  id = str(uuid.uuid4())
  msg = request.form.get('msg')
  body = {"id": id, "msg": msg}
  requests.post('http://localhost:5001', data=body)
  return jsonify(body)

if __name__ == '__main__':
  app.run(port=5000)
