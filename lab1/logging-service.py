from flask import Flask, request

app = Flask(__name__)

messages = {}

@app.route('/', methods=['GET'])
def get():
  return messages

@app.route('/', methods=['POST'])
def post():
  id = request.form.get('id')
  msg = request.form.get('msg')
  messages[id] = msg
  print(msg)
  return ''

if __name__ == '__main__':
  app.run(port=5001)
