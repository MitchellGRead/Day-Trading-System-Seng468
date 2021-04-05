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

funds_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'amount': non_negative_number,
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'amount', 'command']
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

user_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'command']
}

update_user_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'}
    },
    'required': ['user_id']
}

update_stock_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string
    },
    'required': ['user_id', 'stock_symbol'],
}

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

add_funds_schema = funds_schema
remove_funds_schema = funds_schema

buy_stock_schema = base_transaction_schema
commit_buy_schema = user_schema
cancel_buy_schema = user_schema

sell_stock_schema = base_transaction_schema
commit_sell_schema = user_schema
cancel_sell_schema = user_schema

