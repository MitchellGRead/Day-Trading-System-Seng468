
account_summary = '/get/<command:string>/trans/<trans_num:int>/user/<user_id:string>'
generate_dumplog = '/get/<command:string>/trans/<trans_num:int>/filename/<filename:string>'  # ?user_id:<string>

user_command_endpoint = '/event/user_command'
account_transaction_endpoint = '/event/account_transaction'
system_endpoint = '/event/system'
quote_server_endpoint = '/event/quote'
error_endpoint = '/event/error'
