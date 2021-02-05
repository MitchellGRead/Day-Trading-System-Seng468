from UserCommands import UserCommands


CURRENT_FILE_NAME = "./1_user_workload.txt"
WEBSERVER_IP, WEBSERVER_PORT = "localhost", 5000
WEBSERVER_URL = f'{WEBSERVER_IP}:{WEBSERVER_PORT}'


def readWorkloadFile():
    with open(CURRENT_FILE_NAME, "r") as workload:
        contents = workload.read()
    return contents.split('\n')


def main():
    workload_actions = readWorkloadFile()
    user_commands = [command.split(' ')[1] for command in workload_actions]
    params = [command.split(',') for command in user_commands]
    command_sender = UserCommands(WEBSERVER_IP, WEBSERVER_PORT)

    print(params)
    for param in params:
        command = param[0]

        if command == 'ADD':
            resp = command_sender.addFundsRequest(WEBSERVER_URL, param)
            print(resp)
        # elif command == 'QUOTE':
        #     resp = UserCommands.quoteRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'BUY':
        #     resp = UserCommands.buyRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'COMMIT_BUY':
        #     resp = UserCommands.commitBuyRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'CANCEL_BUY':
        #     resp = UserCommands.cancelBuyRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'SET_BUY_AMOUNT':
        #     resp = UserCommands.setBuyAmountRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'CANCEL_SET_BUY':
        #     resp = UserCommands.cancelSetBuyRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'SET_BUY_TRIGGER':
        #     resp = UserCommands.setBuyTriggerRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'SELL':
        #     resp = UserCommands.sellRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'COMMIT_SELL':
        #     resp = UserCommands.commitSellRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'CANCEL_SELL':
        #     resp = UserCommands.cancelSellRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'SET_SELL_AMOUNT':
        #     resp = UserCommands.setSellAmountRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'CANCEL_SET_SELL':
        #     resp = UserCommands.cancelSetSellRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'SET_SELL_TRIGGER':
        #     resp = UserCommands.setSellTriggerRequest(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'DISPLAY_SUMMARY':
        #     resp = UserCommands.displaySummary(WEBSERVER_URL, param)
        #     print(resp.json())
        # elif command == 'DUMPLOG':
        #     resp = UserCommands.dumplog(WEBSERVER_URL, param)
        #     print(resp)
        # else:
        #     print(f'INVALID COMMAND: {command}')

    return


if __name__ == "__main__":
    main()
