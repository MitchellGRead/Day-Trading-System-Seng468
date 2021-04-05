from datetime import datetime
from pathlib import Path

import pandas as pd

from eventLogger import logger


class DataAnalyser:

    def __init__(
            self,
            num_users,  # int
            num_commands,  # int
            execution_time,  # float
            command_times  # dict
    ):
        self.num_users = num_users
        self.num_commands = num_commands
        self.execution_time = execution_time
        self.command_times = self._toDataFrame(command_times)
        self.cps = self.num_commands / self.execution_time  # Commands per second
        self._SAVE_PATH = f'./commandanalysis/{num_users}_users_{self._currentDate()}/'

    def _toDataFrame(self, data):
        return pd.DataFrame(data=dict([(k, pd.Series(v)) for k, v in data.items()]))

    def _makePath(self, pathToMake):
        path = Path(pathToMake)
        path.mkdir(parents=True, exist_ok=True)

    def _currentDate(self):
        return datetime.now().strftime('%m-%d-%Y_%H-%M-%S')

    def saveCommandTimes(self):
        self._makePath(self._SAVE_PATH)

        save_path = f'{self._SAVE_PATH}command_times.csv'
        self.command_times.to_csv(save_path, index=False)

    def logSummary(self, save=True):
        logger.info(f'Total commands executed - {self.num_commands}')
        logger.info(f'Total execution time (s) - {self.execution_time}')
        logger.info(f'Commands per second - {self.cps}')
        logger.info(self.command_times.describe())

        if save:
            self.saveSummary()

    def saveSummary(self):
        self._makePath(self._SAVE_PATH)
        save_path = f'{self._SAVE_PATH}summary.csv'

        self.command_times.describe().to_csv(save_path)
        with open(save_path, 'a') as file:
            file.write(f'Total commands executed - {self.num_commands}\n')
            file.write(f'Total execution time (s) - {self.execution_time}\n')
            file.write(f'Commands per second - {self.cps}\n')

