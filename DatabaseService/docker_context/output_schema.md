# Purpose
This document describes the format of the returned data to expect in response to commands sent to 
the Database Service's HTTP API. All returned data is sent in JSON format, embedded in the HTTP response message.

# Return Data Format
This section describes in detail the return data format to be expected for each endpoint of the API. The formats here correspond to the data embedded
in the respone HTTP messages sent after a request. All formats are in JSON.

## GET Endpoints

### Get all users' funds - /funds/get/all

#### Success
    {'some_user_id': {'available_funds': number, 'reserved_funds':number}, ...}
Each entry contains as its key the user id to which the data belongs.

#### Failure
    {'errorMessage': '<some_string>'}

### Get a user's funds - /funds/get/user/user_id

#### Success
    {'available_funds': number, 'reserved_funds':number}

#### Failure
    {'errorMessage': '<some_string>'}

### Get all users' stocks - /stocks/get/all

#### Success
    {'some_user_id': [{'some_stock_id':[stock_available, stock_reserved], ...}], ...}
stock_available and stock_reserved are some numbers

#### Failure
    {'errorMessage': '<some_string>'}

### Get a user's stocks - /stock/get/user/user_id?stock_id=<stock_id>

#### Success
    {'some_stock_id':[stock_available, stock_reserved], ...}
stock_available and stock_reserved are some numbers

#### Failure
    {'errorMessage': '<some_string>'}

### Get all triggers for all users - /triggers/all/get

#### Success
    {'some_stock_id': {'buy_triggers': {'some_user_id':[stock_amount, stock_price, transaction_num], ...}, 'sell_triggers': {'some_user_id':[stock_amount, stock_price, transaction_num], ...}}, ...}
stock_amount, stock_price and transaction_num are some numbers

#### Failure
    {'errorMessage': '<some_string>'}

### Get all users' buy triggers - /triggers/buy/get/all

#### Success
    {'some_stock_id': [{'some_user_id':[stock_amount, stock_price, transaction_num], ...}], ...}
stock_amount, stock_price and transaction_num are some numbers

#### Failure
    {'errorMessage': '<some_string>'}

### Get a user's buy triggers - /triggers/buy/get/user/user_id

#### Success
    {'some_stock_id':[stock_amount, stock_price, transaction_num], ...}
stock_amount, stock_price and transaction_num are some numbers

#### Failure
    {'errorMessage': '<some_string>'}

### Get all users' sell triggers - /triggers/sell/get/all

#### Success
    {'some_stock_id': [{'some_user_id':[stock_amount, stock_price, transaction_num], ...}], ...}
stock_amount, stock_price and transaction_num are some numbers

#### Failure
    {'errorMessage': '<some_string>'}

### Get a user's sell triggers - /triggers/sell/get/user/user_id

#### Success
    {'some_stock_id':[stock_amount, stock_price, transaction_num], ...}
stock_amount, stock_price and transaction_num are some numbers

#### Failure
    {'errorMessage': '<some_string>'}

### Get a user's summary - /summary/user_id

#### Success
    {
     'user_id': some_user_id, 'user_funds': {'available_funds': funds1, 'reserved_funds': funds2}, 
     'stock_holdings': {'some_stock_id':[stock_available, stock_reserved], ...},
     'active_buy_triggers': {'some_stock_id':[stock_amount, stock_price, transaction_num], ...},
     'active_sell_triggers': {'some_stock_id':[stock_amount, stock_price, transaction_num], ...}
    }

some_user_id is a string while funds1, funds2, stock_available, stock_reserved, stock_amount, stock_price and transaction_num are some numbers

#### Failure
    {'errorMessage': '<some_string>'}

### Get the dumplog (user or system) - /dumplog?user_id=<user_id>

#### Success
    [log1, log2, log3, log4, ...]
log1, log2, log3, and log4 are audit events in the same format as the one they were passed in to the Database service.

#### Failure
    {'errorMessage': '<some_string>'}

## POST Endpoints

### Add funds - /funds/add_funds

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Buy stocks - /stocks/buy_stock

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Sell stocks - /stocks/sell_stocks

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Set buy trigger amount - /triggers/buy/set/amount

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Set buy trigger price - /triggers/buy/set/price

#### Success
    {'user_id': 'some_user_id', 'stock_id': 'some_stock_id', 'stock_amount': some_stock_amount, 'price': some_stock_price, 'transaction_num': transaction_num, 'replace': 'true'/'false'}
The 'replace' field is used to indicate whether or not an existing trigger was replaced. 'true' means replacement took place.

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Execute buy trigger - /triggers/execute/buy

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Cancel buy trigger - /triggers/buy/cancel

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Set sell trigger amount - /triggers/sell/set/amount

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Set sell trigger price - /triggers/sell/set/price

#### Success
    {'user_id': 'some_user_id', 'stock_id': 'some_stock_id', 'stock_amount': some_stock_amount, 'price': some_stock_price, 'transaction_num': transaction_num, 'replace': 'true'/'false'}
The 'replace' field is used to indicate whether or not an existing trigger was replaced. 'true' means replacement took place.

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Execute sell trigger - /triggers/execute/sell

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Cancel sell trigger - /trigger/sell/cancel

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}

### Add audit event to either user or system log - /audit/event

#### Success
    {'status': 'success', 'message':'<some_message>'}

#### Failure
    {'status': 'failure', 'message':'<some_message>'}
