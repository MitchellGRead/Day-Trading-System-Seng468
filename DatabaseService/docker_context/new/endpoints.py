""" GET Endpoints """
get_users_endpoint = '/users/get'
get_all_funds_endpoint = '/funds/get/all'
get_user_funds_endpoint = '/funds/get/user/<user_id:string>'
get_all_stocks_endpoint = '/stocks/get/all'
get_user_stocks_endpoint = '/stocks/get/user/<user_id:string>' # ?stock_id=string
get_summary_endpoint = '/reports/summary/user/<user_id:string>'
get_logs_endpoint = '/logs' # ?user_id=string

""" POST Endpoints """
add_funds_endpoint = '/funds/add_funds'
remove_funds_endpoint = '/funds/remove_funds'
buy_stocks_endpoint = '/stocks/buy_stocks'
sell_stocks_endpoint = '/stocks/sell_stocks'

# TODO: Add methods for these endpoints
set_sell_trigger_amount_endpoint = '/triggers/sell/set_amount'
set_sell_trigger_price_endpoint = '/triggers/sell/set_price'
set_buy_trigger_amount_endpoint = '/triggers/buy/set_amount'
set_buy_trigger_price_endpoint = '/triggers/buy/set_price'