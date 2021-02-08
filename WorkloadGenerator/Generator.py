from UserCommands import UserCommands
import datetime


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
        elif command == 'QUOTE':
            resp = command_sender.quoteRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'BUY':
            resp = command_sender.buyRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'COMMIT_BUY':
            resp = command_sender.commitBuyRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'CANCEL_BUY':
            resp = command_sender.cancelBuyRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'SET_BUY_AMOUNT':
            resp = command_sender.setBuyAmountRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'CANCEL_SET_BUY':
            resp = command_sender.cancelSetBuyRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'SET_BUY_TRIGGER':
            resp = command_sender.setBuyTriggerRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'SELL':
            resp = command_sender.sellRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'COMMIT_SELL':
            resp = command_sender.commitSellRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'CANCEL_SELL':
            resp = command_sender.cancelSellRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'SET_SELL_AMOUNT':
            resp = command_sender.setSellAmountRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'CANCEL_SET_SELL':
            resp = command_sender.cancelSetSellRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'SET_SELL_TRIGGER':
            resp = command_sender.setSellTriggerRequest(WEBSERVER_URL, param)
            print(resp)
        elif command == 'DISPLAY_SUMMARY':
            resp = command_sender.displaySummary(WEBSERVER_URL, param)
            print(resp)
        elif command == 'DUMPLOG':
            resp = command_sender.dumplog(WEBSERVER_URL, param)
            print(resp)
        else:
            print(f'INVALID COMMAND: {command}')

    return


if __name__ == "__main__":
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print("Execution Time: " + str((end-start).total_seconds()*1000) + " ms")
