from sanic import Sanic
from sanic.response import json
import requests


WEB_SERVER_NAME = 'WebService'
WEB_SERVER_IP, WEB_SERVER_PORT = 'localhost', 5000
TRANS_SERVER_IP, TRANS_SERVER_PORT = 'localhost', 5050
TRANS_SERVER_URL = f'http://{TRANS_SERVER_IP}:{TRANS_SERVER_PORT}'

app = Sanic(WEB_SERVER_NAME)


@app.route('/')
def home(request):
    return json({'hello': 'world'})


@app.route('/add/funds/', methods=['POST'])
async def addToAccount(request):
    print(request.json)
    print("Sending data to transaction service")
    resp = requests.post(f'{TRANS_SERVER_URL}/add/funds/', json=request.json)

    return json(resp.json())


if __name__ == '__main__':
    app.run(host=WEB_SERVER_IP, port=WEB_SERVER_PORT, debug=True, auto_reload=True)
