import datetime
import asyncio
import aiohttp
import config
from UserCommands import UserCommands

CURRENT_FILE_NAME = "./100_user_workload.txt"


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
        await command_sender.handleCommand(param)

    await client.close()
    return


if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    end = datetime.datetime.now()
    print("Execution Time: " + str((end-start).total_seconds()*1000) + " ms")
