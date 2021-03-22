from Client import Client
from UserCommands import UserCommands
from eventLogger import logger


class User:

    def __init__(self, ip, port, user_id, commands, loop):
        self.user_id = user_id
        self.client = Client(loop)
        self.command_handler = UserCommands(ip, port, self.client)
        self.commands = commands
        self.times = {}

    async def processCommands(self):
        for command in self.commands:
            logger.debug(f'{self.user_id} processing {command}')
            time = await self.command_handler.handleCommand(command)

            self.trackTime(command[1], time)

        await self.stop()
        return self.times

    def trackTime(self, command, time):
        if command in self.times:
            self.times[command].append(time)
        else:
            self.times[command] = [time]

    async def stop(self):
        logger.info(f'{self.user_id} finished processing.')
        await self.client.stop()
