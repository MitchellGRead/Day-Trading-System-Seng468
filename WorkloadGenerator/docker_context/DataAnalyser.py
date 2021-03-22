import pandas as pd
from eventLogger import logger


class Grapher:

    def __init__(
            self,
            num_users,
            num_commands,
            execution_time,
            command_times
    ):
        self.num_users = num_users
        self.num_commands = num_commands
        self.execution_time = execution_time
        self.command_times = command_times
        self.cps = self.num_commands / self.execution_time  # Commands per second

    def logSummary(self):
        logger.info(f'Total commands executed - {self.num_commands}')
        logger.info(f'Total execution time - {self.execution_time}s')
        logger.info(f'Commands per second - {self.cps}')
