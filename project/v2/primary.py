from flask import Flask, request
import threading
import aiohttp
import asyncio
import sys
import os

urls = ['http://127.0.0.1:5001', 'http://127.0.0.1:5002']
# urls = os.getenv('URLS', '').split(',')

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
  concern = int(request.form.get('concern'))
  messages.append(msg)
  async def send_to_services():
    tasks = [send(url, {'msg': msg}) for url in urls]
    if concern > 1:
      count = 1
      for task in asyncio.as_completed(tasks):
        await task
        count += 1
        if count >= concern:
          break
    else:
      def await_for_services():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async def await_for_tasks():
          await asyncio.gather(*tasks)
        loop.run_until_complete(await_for_tasks())
        loop.close()
      threading.Thread(target=await_for_services).start()
  await send_to_services()
  return msg

if __name__ == '__main__':
  port = int(sys.argv[1])
  app.run(port=port)
