from dataclasses import dataclass


# User commands or inputs from UI. i.e. Buy, Add, etc
@dataclass
class UserCommandEvent:
    timestamp: int
    server: str
    transactionNumber: int
    command: str
    userName: str
    funds: float = 0
    stockSymbol: str = ''  # required where symbol needed for command
    filename: str = ''  # required for dumplog
    xmlName: str = 'userCommand'


# Anything that alters a users account. i.e. add or remove
@dataclass
class AccountTransaction:
    timestamp: int
    server: str
    transactionNumber: int
    action: str
    userName: str
    funds: float
    xmlName: str = 'accountTransaction'


# Current user commands, interserver comms, or executing previously set triggers
@dataclass
class SystemEvent:
    timestamp: int
    server: str
    transactionNumber: int
    command: str
    stockSymbol: str = ''
    funds: float = 0
    filename: str = ''
    userName: str = ''
    xmlName: str = 'systemEvent'


# When quote server successfully hit
@dataclass
class QuoteServerEvent:
    timestamp: int
    quoteServerTimestamp: int
    server: str
    transactionNumber: int
    userName: str
    stockSymbol: str
    price: float
    cryptoKey: str
    xmlName: str = 'quoteServer'


# Whenever error occurs. Should contain all info from original command and an error message
@dataclass
class ErrorEvent:
    timestamp: int
    server: str
    transactionNumber: int
    command: str
    errorMessage: str
    userName: str = ''
    stockSymbol: str = ''
    filename: str = ''
    funds: float = 0
    xmlName: str = 'errorEvent'
