from flask import Flask, request
import requests
import asyncio
import sys

app = Flask(__name__)

messages = []

future_messages = {}

@app.route('/', methods=['GET'])
def get():
  return messages

@app.route('/', methods=['POST'])
async def post():
  _id = int(request.form.get('_id'))
  msg = request.form.get('msg')
  if _id == len(messages):
    messages.append(msg)
    i = _id + 1
    while i in future_messages:
      messages.append(future_messages.pop(i))
      i += 1
  elif _id > len(messages):
    future_messages[_id] = msg
  await asyncio.sleep(2)
  return msg

if __name__ == '__main__':
  port = int(sys.argv[1])
  response = requests.post('http://127.0.0.1:5000/rejoin', data={'url': f'http://127.0.0.1:{port}'})
  messages = response.json()
  app.run(port=port)
