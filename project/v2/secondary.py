from flask import Flask, request
import asyncio
import sys

app = Flask(__name__)

messages = []

@app.route('/', methods=['GET'])
def get():
  return messages

@app.route('/', methods=['POST'])
async def post():
  msg = request.form.get('msg')
  messages.append(msg)
  await asyncio.sleep(2)
  return msg

if __name__ == '__main__':
  port = int(sys.argv[1])
  app.run(port=port)
