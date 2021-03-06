from jsonschema import validate, ValidationError
from sanic.log import logger


def validateRequest(data, schema):
    if not data:
        err_msg = 'Data is not Content-Type: application/json'
        logger.error(f'{err_msg} - {data}')
        return False, err_msg

    try:
        validate(instance=data, schema=schema)
        return True, ''
    except ValidationError as err:
        logger.error(f'{err.message} - {data}')
        return False, err.message


def errorResult(err, data):
    return {
        'errorMessage': err,
        'content': data
    }


one_to_three_letter_string = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 3
}

non_negative_number = {
    'type': 'number',
    'minimum': 0
}

base_transaction_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'amount': non_negative_number,
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'stock_symbol', 'amount', 'command']
}


base_user_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'command']
}

base_user_symbol_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'stock_symbol', 'command']
}

# Buy Schemas --------------------------------------------------

buy_schema = base_transaction_schema
commit_buy_schema = base_user_schema
cancel_buy_schema = base_user_schema
set_buy_amount_schema = base_transaction_schema
set_buy_trigger_schema = base_transaction_schema
cancel_set_buy_schema = base_user_symbol_schema

# --------------------------------------------------------------

# Sell Schemas --------------------------------------------------

sell_schema = base_transaction_schema
commit_sell_schema = base_user_schema
cancel_sell_schema = base_user_schema
set_sell_amount_schema = base_transaction_schema
set_sell_trigger_schema = base_transaction_schema
cancel_set_sell_schema = base_user_symbol_schema

# --------------------------------------------------------------

# Account Schemas ----------------------------------------------

add_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'amount': non_negative_number,
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'amount', 'command']
}

# --------------------------------------------------------------

# Legacy Server Schemas ----------------------------------------

quote_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'stock_symbol', 'command']
}

# --------------------------------------------------------------

# Audit Schemas ------------------------------------------------

display_summary_schema = base_user_schema
dumplog_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'filename': {'type': 'string'},
        'user_id': {'type': 'string'},
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'filename', 'command']
}

# --------------------------------------------------------------
