from eventLogger import logger
from UserCommands import UserCommands
from Client import Client


class User:

    def __init__(self, ip, port, user_id, commands, loop):
        self.user_id = user_id
        self.client = Client(loop)
        self.command_handler = UserCommands(ip, port, self.client)
        self.commands = commands

    async def processCommands(self):
        resps = []
        for command in self.commands:
            logger.debug(f'{self.user_id} processing {command}')
            # TODO Update so that this saves the amount of time taken to run each command and which command was run for analysis
            resp = await self.command_handler.handleCommand(command)
            resps.append(resp)

        await self.stop()
        return resps

    async def stop(self):
        logger.info(f'{self.user_id} finished processing.')
        await self.client.stop()
