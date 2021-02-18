import datetime
import asyncio
import aiohttp
import config
from UserCommands import UserCommands

CURRENT_FILE_NAME = "./1_user_workload.txt"

def readWorkloadFile():
    with open(CURRENT_FILE_NAME, "r") as workload:
        contents = workload.read()
    return contents.split('\n')


async def main():
    workload_actions = readWorkloadFile()
    user_commands = [command.split(' ')[1] for command in workload_actions]
    params = [[idx, *command.split(',')] for idx, command in enumerate(user_commands, 1)]

    client = aiohttp.ClientSession()
    command_sender = UserCommands(config.WEB_SERVER_IP, config.WEB_SERVER_PORT, client)

    for param in params:
        command = param[1]

        if command == 'ADD':
            resp = await command_sender.addFundsRequest(param)
            print(resp)
        elif command == 'QUOTE':
            resp = await command_sender.quoteRequest(param)
            print(resp)
        elif command == 'BUY':
            resp = await command_sender.buyRequest(param)
            print(resp)
        elif command == 'COMMIT_BUY':
            resp = await command_sender.commitBuyRequest(param)
            print(resp)
        elif command == 'CANCEL_BUY':
            resp = await command_sender.cancelBuyRequest(param)
            print(resp)
        elif command == 'SET_BUY_AMOUNT':
            resp = await command_sender.setBuyAmountRequest(param)
            print(resp)
        elif command == 'CANCEL_SET_BUY':
            resp = await command_sender.cancelSetBuyRequest(param)
            print(resp)
        elif command == 'SET_BUY_TRIGGER':
            resp = await command_sender.setBuyTriggerRequest(param)
            print(resp)
        elif command == 'SELL':
            resp = await command_sender.sellRequest(param)
            print(resp)
        elif command == 'COMMIT_SELL':
            resp = await command_sender.commitSellRequest(param)
            print(resp)
        elif command == 'CANCEL_SELL':
            resp = await command_sender.cancelSellRequest(param)
            print(resp)
        elif command == 'SET_SELL_AMOUNT':
            resp = await command_sender.setSellAmountRequest(param)
            print(resp)
        elif command == 'CANCEL_SET_SELL':
            resp = await command_sender.cancelSetSellRequest(param)
            print(resp)
        elif command == 'SET_SELL_TRIGGER':
            resp = await command_sender.setSellTriggerRequest(param)
            print(resp)
        elif command == 'DISPLAY_SUMMARY':
            resp = await command_sender.displaySummary(param)
            print(resp)
        elif command == 'DUMPLOG':
            resp = await command_sender.dumplog(param)
            print(resp)
        else:
            print(f'INVALID COMMAND: {command}')

    await client.close()
    return


if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    end = datetime.datetime.now()
    print("Execution Time: " + str((end-start).total_seconds()*1000) + " ms")
