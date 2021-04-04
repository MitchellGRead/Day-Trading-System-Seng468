import asyncio
import time
from datetime import datetime

import config
from Client import Client
from DataAnalyser import DataAnalyser
from User import User
from UserCommands import UserCommands
from eventLogger import logger

CURRENT_FILE_NAME = "./10_user_workload.txt"
NUM_USERS = 10


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

    results = await asyncio.gather(*tasks)  # times for each command broken down by users
    return results


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


def combineUserTimes(times):
    all_times = {}
    for userTimes in times:
        for command in userTimes.keys():
            if command in all_times:
                all_times[command].extend(userTimes[command])
            else:
                all_times[command] = userTimes[command]
    return all_times


async def main():
    workload_actions = readWorkloadFile()
    num_commands = len(workload_actions)
    user_workloads, dumplog = parseUserCommands(workload_actions)

    logger.info(user_workloads.keys())
    logger.info(dumplog)
    assert len(user_workloads.keys()) == NUM_USERS

    loop = asyncio.get_event_loop()
    users = createUsers(user_workloads, loop)

    start = time.time()
    times = await runUsers(users)
    await generateDumplog(dumplog)
    end = time.time()

    execution_time = end - start
    command_times = combineUserTimes(times)

    analyser = DataAnalyser(NUM_USERS, num_commands, execution_time, command_times)
    analyser.saveCommandTimes()
    analyser.logSummary()

    return


if __name__ == '__main__':
    asyncio.run(main())
