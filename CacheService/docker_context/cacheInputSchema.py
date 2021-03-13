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

stocks_query_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'stock_amount': non_negative_number,
        'funds': non_negative_number,
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'stock_symbol', 'stock_amount', 'funds', 'command']
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

add_funds_schema = funds_schema
remove_funds_schema = funds_schema
buy_stock_schema = stocks_query_schema
sell_stock_schema = stocks_query_schema
