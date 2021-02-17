from jsonschema import validate, ValidationError


def validateRequest(data, schema):
    if not data:
        return False, 'Data is not Content-Type: application/json'

    try:
        validate(instance=data, schema=schema)
        return True, ''
    except ValidationError as err:
        return False, str(err)


def errorResult(err, data):
    return {
        'errorMessage': err,
        'content': data
    }


base_transaction_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'stock_symbol': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 3
        },
        'amount': {
            'type': 'number',
            'inclusiveMinimum': 0
        }
    },
    'required': ['transaction_num', 'user_id', 'stock_symbol', 'amount']
}


base_user_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'}
    },
    'required': ['transaction_num', 'user_id']
}

# Buy Schemas --------------------------------------------------

buy_schema = base_transaction_schema
commit_buy_schema = base_user_schema
cancel_buy_schema = base_user_schema
set_buy_amount_schema = base_transaction_schema
set_buy_trigger_schema = base_transaction_schema
cancel_set_buy_schema = base_user_schema

# --------------------------------------------------------------

# Sell Schemas --------------------------------------------------

sell_schema = base_transaction_schema
commit_sell_schema = base_user_schema
cancel_sell_schema = base_user_schema
set_sell_amount_schema = base_transaction_schema
set_sell_trigger_schema = base_transaction_schema
cancel_set_sell_schema = base_user_schema

# --------------------------------------------------------------

# Account Schemas ----------------------------------------------

add_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'amount': {
            'type': 'number',
            'inclusiveMinimum': 0
        }
    },
    'required': ['transaction_num', 'user_id', 'amount']
}

# --------------------------------------------------------------

# Legacy Server Schemas ----------------------------------------

quote_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'stock_symbol': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 3
        }
    },
    'required': ['transaction_num', 'user_id', 'stock_symbol']
}

# --------------------------------------------------------------

# Audit Schemas ------------------------------------------------

display_summary_schema = base_user_schema
dumplog_schema = {
    'type': 'object',
    'properties': {
        'transaction_num': {'type': 'integer'},
        'filename': {'type': 'string'},
        'user_id': {'type': 'string'}
    },
    'required': ['transaction_num', 'filename']
}

# --------------------------------------------------------------
