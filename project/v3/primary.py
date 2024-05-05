from flask import Flask, request
import threading
import aiohttp
import asyncio
import sys

urls = {}

app = Flask(__name__)

messages = []

missed_messages = {}

@app.route('/rejoin', methods=['POST'])
def rejoin():
  url = request.form.get('url')
  urls[url] = True
  if url not in missed_messages:
    missed_messages[url] = []
  result = missed_messages[url]
  missed_messages[url] = []
  return result

async def send(url, body):
  async with aiohttp.ClientSession() as session:
    try:
      async with session.post(url, data=body) as response:
        return response.status == 200
    except aiohttp.ClientError:
      return None

async def send_with_retry(url, body):
  if (urls[url] == True):
    for i in range(3):
      print(f'attempt {i} to {url}')
      response = await send(url, body)
      if response is not None:
        return response
  urls[url] = False
  if (urls[url] == False):
    missed_messages[url].append(body['msg'])
  return False

@app.route('/', methods=['GET'])
def get():
  return messages

@app.route('/', methods=['POST'])
async def post():
  msg = request.form.get('msg')
  concern = int(request.form.get('concern'))
  async def send_to_services():
    tasks = [send_with_retry(url, {'_id': len(messages), 'msg': msg}) for url in urls]
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
  messages.append(msg)
  return msg

if __name__ == '__main__':
  port = int(sys.argv[1])
  app.run(port=port)
