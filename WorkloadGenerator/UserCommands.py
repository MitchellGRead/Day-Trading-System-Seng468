import requests
from socket import socket, AF_INET, SOCK_STREAM
import json


class UserCommands:
    web_service_ip = None
    web_service_port = None
    web_service_socket = socket(AF_INET, SOCK_STREAM)

    def __init__(self, ip, port):
        self.web_service_ip = ip
        self.web_service_port = port
        self.connectWebService()

    def connectWebService(self):
        self.web_service_socket.connect((self.web_service_ip, self.web_service_port))

    def sendAndRecvData(self, data):
        self.web_service_socket.sendall(json.dumps(data).encode())
        data = self.web_service_socket.recv(1024).decode()
        return json.loads(data)

    def addFundsRequest(self, server_url, params):
        command, user_id, amount = params

        data = {

            'user_id': user_id,
            'amount': amount
        }
        resp = self.sendAndRecvData(data)
        # resp = requests.post(f'{server_url}/add/funds/', json=data)

        return resp

    def quoteRequest(server_url, params):
        command, user_id, stock_symbol = params

        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol
        }
        resp = requests.get(f'{server_url}/quote/{user_id}/{stock_symbol}/', json=data)
        return resp

    def displaySummary(server_url, params):
        command, user_id = params
        data = {
            'command': command,
            'user_id': user_id
        }
        resp = requests.get(f'{server_url}/summary/{user_id}/', json=data)
        return resp

    def dumplog(server_url, params):
        if len(params) == 2:
            command, filename = params
            data = {'command': command}
            resp = requests.get(f'{server_url}/dumplog/', json=data)
            return resp
        elif len(params) == 3:
            command, user_id, filename = params
            data = {
                'command': command,
                'user_id': user_id
            }
            resp = requests.get(f'{server_url}/dumplog/{user_id}/', json=data)
            return resp
        else:
            return None

    # BUY REQUESTS --------------------------------------------
    def buyRequest(server_url, params):
        command, user_id, stock_symbol, amount = params
        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': amount
        }
        resp = requests.post(f'{server_url}/buy/', json=data)
        return resp

    def commitBuyRequest(server_url, params):
        command, user_id = params
        data = {
            'command': command,
            'user_id': user_id
        }
        resp = requests.post(f'{server_url}/buy/commit/', json=data)
        return resp

    def cancelBuyRequest(server_url, params):
        command, user_id = params
        data = {
            'command': command,
            'user_id': user_id
        }
        resp = requests.post(f'{server_url}/cancel/buy/', json=data)
        return resp

    def setBuyAmountRequest(server_url, params):
        command, user_id, stock_symbol, amount = params
        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': amount
        }
        resp = requests.post(f'{server_url}/set/buy/amount/', json=data)
        return resp

    def cancelSetBuyRequest(server_url, params):
        command, user_id, stock_symbol = params
        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol
        }
        resp = requests.post(f'{server_url}/cancel/set/buy/', json=data)
        return resp

    def setBuyTriggerRequest(server_url, params):
        command, user_id, stock_symbol, amount = params
        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': amount
        }
        resp = requests.post(f'{server_url}/set/buy/trigger/', json=data)
        return resp

    # --------------------------------------------------------------

    # BUY REQUESTS --------------------------------------------
    def cancelSellRequest(server_url, params):
        command, user_id = params
        data = {
            'command': command,
            'user_id': user_id
        }
        resp = requests.post(f'{server_url}/cancel/sell/', json=data)
        return resp

    def commitSellRequest(server_url, params):
        command, user_id = params
        data = {
            'command': command,
            'user_id': user_id
        }
        resp = requests.post(f'{server_url}/buy/commit/', json=data)
        return resp

    def sellRequest(server_url, params):
        command, user_id, stock_symbol, amount = params
        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': amount
        }
        resp = requests.post(f'{server_url}/sell/', json=data)
        return resp

    def setSellAmountRequest(server_url, params):
        command, user_id, stock_symbol, amount = params
        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': amount
        }
        resp = requests.post(f'{server_url}/set/sell/amount/', json=data)
        return resp

    def cancelSetSellRequest(server_url, params):
        command, user_id, stock_symbol = params
        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol
        }
        resp = requests.post(f'{server_url}/cancel/set/sell/', json=data)
        return resp

    def setSellTriggerRequest(server_url, params):
        command, user_id, stock_symbol, amount = params
        data = {
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': amount
        }
        resp = requests.post(f'{server_url}/set/buy/trigger/', json=data)
        return resp
    # --------------------------------------------------------------
