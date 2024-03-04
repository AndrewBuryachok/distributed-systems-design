from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
  return 'Not implemented yet'

if __name__ == '__main__':
  app.run(port=5004)
