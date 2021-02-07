from dataclasses import dataclass


@dataclass
class UserCommandEvent:
    timestamp: int
    server: str
    transactionNumber: int
    command: str
    userName: str
    stockSymbol: str
    funds: float
    xmlName: str = 'userCommand'


@dataclass
class AccountTransaction:
    timestamp: int
    server: str
    transactionNumber: int
    command: str
    userName: str
    funds: float
    xmlName: str = 'accountTransaction'


@dataclass
class SystemEvent:
    timestamp: int
    server: str
    transactionNumber: int
    command: str
    userName: str
    stockSymbol: str
    funds: float
    xmlName: str = 'systemEvent'


@dataclass
class QuoteServerEvent:
    quoteServerTimestamp: int
    server: str
    transactionNumber: int
    userName: str
    stockSymbol: str
    price: float
    cryptoKey: str
    xmlName: str = 'quoteServer'


@dataclass
class ErrorEvent:
    timestamp: int
    server: str
    transactionNumber: int
    command: str
    userName: str
    stockSymbol: str
    errorMessage: str
    funds: float = 0
    xmlName: str = 'systemEvent'


@dataclass
class DebugEvent:
    timestamp: int
    server: str
    debugMessage: str
    transactionNumber: int = -1
    stockSymbol: str = ''
    command: str = ''
    userName: str = ''
    xmlName: str = 'debugEvent'
