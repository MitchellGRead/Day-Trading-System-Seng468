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
    'minimum': 0
}

funds_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'funds': non_negative_number
    },
    'required': ['user_id', 'funds']
}

stocks_query_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'stock_amount': non_negative_number,
        'funds': non_negative_number
    },
    'required': ['user_id', 'stock_symbol', 'stock_amount', 'funds']
}

triggers_amount_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'amount': non_negative_number
    },
    'required': ['user_id', 'stock_symbol', 'amount']
}

triggers_price_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'price': non_negative_number
    },
    'required': ['user_id', 'stock_symbol', 'price']
}

triggers_cancel_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string
    },
    'required': ['user_id', 'stock_symbol']
}

triggers_execute_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'funds': non_negative_number
    },
    'required': ['user_id', 'stock_symbol', 'funds']
}

add_funds_schema = funds_schema
remove_funds_schema = funds_schema
buy_stock_schema = stocks_query_schema
sell_stock_schema = stocks_query_schema
buy_trigger_amount_schema = triggers_amount_schema
buy_trigger_price_schema = triggers_price_schema
sell_trigger_amount_schema = triggers_amount_schema
sell_trigger_price_schema = triggers_price_schema
cancel_set_buy_schema = triggers_cancel_schema
cancel_set_sell_schema = triggers_cancel_schema
execute_buy_trigger_schema = triggers_execute_schema
execute_sell_trigger_schema = triggers_execute_schema