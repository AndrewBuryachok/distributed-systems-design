from flask import Flask, request
import aiohttp
import asyncio
import sys
import os

# urls = ['http://127.0.0.1:5001', 'http://127.0.0.1:5002']
urls = os.getenv('URLS', '').split(',')

app = Flask(__name__)

messages = []

async def send(url, body):
  async with aiohttp.ClientSession() as session:
    async with session.post(url, data=body) as response:
      return response.status == 200

@app.route('/', methods=['GET'])
def get():
  return messages

@app.route('/', methods=['POST'])
async def post():
  msg = request.form.get('msg')
  messages.append(msg)
  tasks = [send(url, {'msg': msg}) for url in urls]
  await asyncio.gather(*tasks)
  return msg

if __name__ == '__main__':
  port = int(sys.argv[1])
  app.run(host='0.0.0.0', port=port)
