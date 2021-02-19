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

user_command_event_schema = {
    'type': 'object',
    'properties': {
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
                'server',
                'timestamp',
                'transaction_num',
                'command',
                'filename'
            ]
        },
        {
            'required': [
                'server',
                'timestamp',
                'transaction_num',
                'user_id'
            ]
        },
        {
            'required': [  # ADD commands
                'server',
                'timestamp',
                'transaction_num',
                'command',
                'user_id',
                'amount'
            ]
        }
    ]
}

system_event_schema = {
    'type': 'object',
    'properties': {
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
        'server',
        'timestamp',
        'transaction_num',
        'command'
    ]
}

quote_server_event_schema = {
    'type': 'object',
    'properties': {
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
        'server',
        'timestamp',
        'transaction_num',
        'command',
        'error_msg'
    ]
}
