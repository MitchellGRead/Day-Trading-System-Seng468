from jsonschema import validate, ValidationError


def validateRequest(data, schema):
    if not data:
        return False, 'Data is not Content-Type: application/json'

    try:
        validate(instance=data, schema=schema)
        return True, ''
    except ValidationError as err:
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
    'inclusiveMinimum': 0
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

base_user_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'command']
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

base_commit_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'command': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id', 'command']
}

buy_schema = base_transaction_schema
commit_buy_schema = base_commit_schema
cancel_buy_schema = base_user_schema

sell_schema = base_transaction_schema
commit_sell_schema = base_commit_schema
cancel_sell_schema = base_user_schema

add_funds_schema = funds_schema
