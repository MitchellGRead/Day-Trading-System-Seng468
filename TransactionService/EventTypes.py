from dataclasses import dataclass
import time


def timeInMs():
    return round(time.time() * 1000)


# User commands or inputs from UI. i.e. Buy, Add, etc
@dataclass
class UserCommandEvent:
    server: str
    transactionNumber: int
    command: str
    userName: str
    funds: float = 0
    stockSymbol: str = ''  # required where symbol needed for command
    filename: str = ''  # required for dumplog
    timestamp: int = timeInMs()
    xmlName: str = 'userCommand'


# Anything that alters a users account. i.e. add or remove
@dataclass
class AccountTransaction:
    server: str
    transactionNumber: int
    action: str
    userName: str
    funds: float
    timestamp: int = timeInMs()
    xmlName: str = 'accountTransaction'


# Current user commands, interserver comms, or executing previously set triggers
@dataclass
class SystemEvent:
    server: str
    transactionNumber: int
    command: str
    stockSymbol: str = ''
    funds: float = 0
    filename: str = ''
    userName: str = ''
    timestamp: int = timeInMs()
    xmlName: str = 'systemEvent'


# When quote server successfully hit
@dataclass
class QuoteServerEvent:
    quoteServerTimestamp: int
    server: str
    transactionNumber: int
    userName: str
    stockSymbol: str
    price: float
    cryptoKey: str
    timestamp: int = timeInMs()
    xmlName: str = 'quoteServer'


# Whenever error occurs. Should contain all info from original command and an error message
@dataclass
class ErrorEvent:
    server: str
    transactionNumber: int
    command: str
    errorMessage: str
    userName: str = ''
    stockSymbol: str = ''
    filename: str = ''
    funds: float = 0
    timestamp: int = timeInMs()
    xmlName: str = 'errorEvent'
