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

is_user_id = {
    'type': 'string',
    'minLength': 8,
    'maxLength': 12
}

non_negative_number = {
    'type': 'number',
    'minimum': 0
}

funds_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'funds': non_negative_number,
        'command': {'type': 'string'}
    },
    'required': ['user_id', 'funds']
}

stocks_query_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'stock_amount': non_negative_number,
        'funds': non_negative_number,
        'command': {'type': 'string'}
    },
    'required': ['user_id', 'stock_symbol', 'stock_amount', 'funds']
}

user_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'command': {'type': 'string'}
    },
    'required': ['user_id']
}

add_funds_schema = funds_schema
remove_funds_schema = funds_schema
buy_stock_schema = stocks_query_schema
sell_stock_schema = stocks_query_schema
