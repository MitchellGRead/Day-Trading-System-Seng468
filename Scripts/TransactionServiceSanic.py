from sanic import Sanic
from sanic.response import json
from socket import socket, AF_INET, SOCK_STREAM

TRANS_SERVER_NAME = 'TransactionService'
TRANS_SERVER_IP, TRANS_SERVER_PORT = 'localhost', 5050
DUMBY_SOCKET_SERVICE_IP, DUMBY_SOCKET_SERVICE_PORT = 'localhost', 5075

app = Sanic(TRANS_SERVER_NAME)


@app.route('/add/funds/', methods=['POST'])
async def addUserFunds(request):
    print(request.json)

    # Can now perform async calls to other methods and wait for them!
    # addOp = await Transactions.add('mitch', 20)
    # print(addOp)

    # I know this sucks but for the time being I think it will be okay to at least move forward in development
    # Two reasons to move forward. The actual server may react very differently to what we have here. Or they move
    # the quote server to AWS and we don't need sockets.
    quoteSocket = socket(AF_INET, SOCK_STREAM)
    quoteSocket.connect((DUMBY_SOCKET_SERVICE_IP, DUMBY_SOCKET_SERVICE_PORT))
    quoteSocket.sendall('why do you do this to me'.encode())
    resp = quoteSocket.recv(1024)
    print(resp.decode())
    quoteSocket.close()

    return json(request.json)


if __name__ == '__main__':
    app.run(host=TRANS_SERVER_IP, port=TRANS_SERVER_PORT, debug=True, auto_reload=True)
