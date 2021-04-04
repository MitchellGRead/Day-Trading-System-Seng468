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
        'price': non_negative_number,
        'transaction_num': non_negative_number
    },
    'required': ['user_id', 'stock_symbol', 'price', 'transaction_num']
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

user_command_event_schema = {
    'type': 'object',
    'properties': {
        'xmlName': {'type': 'string'},
        'server': {'type': 'string'},
        'timestamp': {'type': 'integer'},
        'transaction_num': {'type': 'integer'},
        'command': {'type': 'string'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'amount': non_negative_number,
        'filename': {'type': 'string'}
    },
    'anyOf': [
        {
            'required': [  # Regular stock commands
                'xmlName',
                'server',
                'timestamp',
                'transaction_num',
                'command',
                'user_id',
                'stock_symbol',
                'amount'
            ]
        },
        {
            'required': [  # DUMPLOG commands
                'xmlName',
                'server',
                'timestamp',
                'transaction_num',
                'command',
                'filename'
            ]
        },
        {
            'required': [  # Display Summary, commit, and cancel commands
                'xmlName',
                'server',
                'timestamp',
                'transaction_num',
                'command',
                'user_id'
            ]
        }
    ]
}

account_transaction_event_schema = {
    'type': 'object',
    'properties': {
        'xmlName': {'type': 'string'},
        'server': {'type': 'string'},
        'timestamp': {'type': 'integer'},
        'transaction_num': {'type': 'integer'},
        'action': {'type': 'string'},  # add or remove
        'user_id': {'type': 'string'},
        'amount': non_negative_number
    },
    'required': [
        'xmlName',
        'server',
        'timestamp',
        'transaction_num',
        'action',
        'user_id',
        'amount'
    ]
}

system_event_schema = {
    'type': 'object',
    'properties': {
        'xmlName': {'type': 'string'},
        'server': {'type': 'string'},
        'timestamp': {'type': 'integer'},
        'transaction_num': {'type': 'integer'},
        'command': {'type': 'string'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'amount': non_negative_number,
        'filename': {'type': 'string'},
    },
    'required': [
        'xmlName',
        'server',
        'timestamp',
        'transaction_num',
        'command'
    ]
}

quote_server_event_schema = {
    'type': 'object',
    'properties': {
        'xmlName': {'type': 'string'},
        'server': {'type': 'string'},
        'timestamp': {'type': 'integer'},
        'transaction_num': {'type': 'integer'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'price': non_negative_number,
        'quote_server_timestamp': {'type': 'integer'},
        'cryptokey': {'type': 'string'},
    },
    'required': [
        'xmlName',
        'server',
        'timestamp',
        'transaction_num',
        'user_id',
        'stock_symbol',
        'price',
        'quote_server_timestamp',
        'cryptokey'
    ]
}

error_event_schema = {
    'type': 'object',
    'properties': {
        'xmlName': {'type': 'string'},
        'server': {'type': 'string'},
        'timestamp': {'type': 'integer'},
        'transaction_num': {'type': 'integer'},
        'command': {'type': 'string'},
        'error_msg': {'type': 'string'},
        'user_id': {'type': 'string'},
        'stock_symbol': one_to_three_letter_string,
        'amount': non_negative_number,
        'filename': {'type': 'string'}
    },
    'required': [
        'xmlName',
        'server',
        'timestamp',
        'transaction_num',
        'command',
        'error_msg'
    ]
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
audit_events_schemas = {"errorEvent": error_event_schema, "userCommand": user_command_event_schema, 
        "quoteServer": quote_server_event_schema, "systemEvent": system_event_schema,
        "accountTransaction": account_transaction_event_schema}
