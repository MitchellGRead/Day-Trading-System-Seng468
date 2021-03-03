import time
import asyncio
import config
from User import User
from UserCommands import UserCommands
from Client import Client
from eventLogger import logger

CURRENT_FILE_NAME = "./45_user_workload.txt"
NUM_USERS = 45


def readWorkloadFile():
    with open(CURRENT_FILE_NAME, "r") as workload:
        contents = workload.read()
    return contents.split('\n')


def parseUserCommands(workload):
    user_commands = [command.split(' ')[1] for command in workload]
    dumplog_command = ''

    user_workloads = {}
    for idx, command in enumerate(user_commands, 1):
        params = [idx, *command.split(',')]
        if params[1] == 'DUMPLOG' and len(params) == 3:  # no user_id
            dumplog_command = params
            break
        user_id = params[2]
        if user_id in user_workloads:
            user_workloads[user_id].append(params)
        else:
            user_workloads[user_id] = [params]
    return user_workloads, dumplog_command


def createUsers(workloads, loop):
    users = []
    for key in workloads:
        users.append(
            User(
                config.WEB_SERVER_IP,
                config.WEB_SERVER_PORT,
                key,
                workloads[key],
                loop
            )
        )
    return users


async def runUsers(users):
    tasks = []
    for user in users:
        task = asyncio.create_task(user.processCommands(), name=user.user_id)
        tasks.append(task)

    resp = await asyncio.gather(*tasks)
    return resp


async def generateDumplog(command):
    loop = asyncio.get_event_loop()
    client = Client(loop)
    command_handler = UserCommands(
        config.WEB_SERVER_IP,
        config.WEB_SERVER_PORT,
        client
    )
    await command_handler.handleCommand(command)
    await client.stop()


async def main():
    workload_actions = readWorkloadFile()
    user_workloads, dumplog = parseUserCommands(workload_actions)

    logger.info(user_workloads.keys())
    logger.info(dumplog)
    assert len(user_workloads.keys()) == NUM_USERS

    loop = asyncio.get_event_loop()
    users = createUsers(user_workloads, loop)

    start = time.time()
    res = await runUsers(users)
    await generateDumplog(dumplog)
    end = time.time()

    logger.info(f'Total elapsed time {end - start}')
    return


if __name__ == '__main__':
    asyncio.run(main())
