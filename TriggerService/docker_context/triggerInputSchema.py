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
        'command': {'type': 'string'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'amount': non_negative_number
    },
    'required': ['transaction_num', 'user_id', 'stock_symbol', 'amount', 'command']
}


base_user_symbol_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'command': {'type': 'string'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string
    },
    'required': ['transaction_num', 'user_id', 'stock_symbol', 'command']
}

set_buy_amount_schema = base_transaction_schema
set_buy_trigger_schema = base_transaction_schema
cancel_buy_trigger_schema = base_user_symbol_schema

set_sell_amount_schema = base_transaction_schema
set_sell_trigger_schema = base_transaction_schema
cancel_sell_trigger_schema = base_user_symbol_schema
