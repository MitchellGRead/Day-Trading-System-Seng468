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
    {'error_message': '<some_string>'}

### Get a user's funds - /funds/get/user/user_id

#### Success
    {'available_funds': number, 'reserved_funds':number}

#### Failure
    {'error_message': '<some_string>'}

### Get all users' stocks - /stocks/get/all

#### Success
    {'some_user_id': [{'some_stock_id':[stock_available, stock_reserved], ...}], ...}
stock_available and stock_reserved are some numbers

#### Failure
    {'error_message': '<some_string>'}

### Get a user's stocks - /stock/get/user/user_id

#### Success
    {'some_stock_id':[stock_available, stock_reserved], ...}
stock_available and stock_reserved are some numbers

#### Failure
    {'error_message': '<some_string>'}

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