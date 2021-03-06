""" GET Endpoints """
get_users_endpoint = '/users/get'
get_all_funds_endpoint = '/funds/get/all'
get_user_funds_endpoint = '/funds/get/user/<user_id:string>'
get_all_stocks_endpoint = '/stocks/get/all'
get_user_stocks_endpoint = '/stocks/get/user/<user_id:string>' # ?stock_id=string
get_all_triggers_endpoint = '/triggers/all/get'
get_all_buy_triggers_endpoint = '/triggers/buy/get/all'
get_user_buy_triggers_endpoint = '/triggers/buy/get/user/<user_id:string>'
get_all_sell_triggers_endpoint = '/triggers/sell/get/all'
get_user_sell_triggers_endpoint = '/triggers/sell/get/user/<user_id:string>'
get_summary_endpoint = '/summary/<user_id:string>'
get_dumplog_endpoint = '/dumplog' # ?user_id=string

""" POST Endpoints """
add_funds_endpoint = '/funds/add_funds'
buy_stocks_endpoint = '/stocks/buy_stocks'
sell_stocks_endpoint = '/stocks/sell_stocks'
set_buy_trigger_amount_endpoint = '/triggers/buy/set/amount'
set_buy_trigger_price_endpoint = '/triggers/buy/set/price'
execute_buy_trigger_endpoint = '/triggers/execute/buy'
cancel_set_buy_endpoint = '/triggers/buy/cancel'
set_sell_trigger_amount_endpoint = '/triggers/sell/set/amount'
set_sell_trigger_price_endpoint = '/triggers/sell/set/price'
execute_sell_trigger_endpoint = '/triggers/execute/sell'
cancel_set_sell_endpoint = '/triggers/sell/cancel'
add_audit_event = '/audit/event' # ?user_id=string
