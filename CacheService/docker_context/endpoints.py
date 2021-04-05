""" GET Endpoints """
get_user_funds_endpoint = '/funds/get/user/<user_id:string>'
get_user_stocks_endpoint = '/stocks/get/user/<user_id:string>/<stock_id:string>'
get_quote_endpoint = '/quote/get/<user_id:string>/<stock_id:string>/<trans_num:int>'
get_bulk_quotes_endpoint = '/quote'  # ?stock_id=id1&stock_id=id2...&user_id=id1&user_id=id2...&transaction_num=num1&transaction_num=num2
get_buy_endpoint = '/stocks/get_buy/<user_id:string>'
get_sell_endpoint = '/stocks/get_sell/<user_id:string>'

""" POST Endpoints """
add_funds_endpoint = '/funds/add_funds'
remove_funds_endpoint = '/funds/remove_funds'
buy_stocks_endpoint = '/stocks/buy_stocks'
sell_stocks_endpoint = '/stocks/sell_stocks'
commit_buy_endpoint = '/stocks/commit_buy'
commit_sell_endpoint = '/stocks/commit_sell'
cancel_buy_endpoint = '/stocks/cancel_buy'
cancel_sell_endpoint = '/stocks/cancel_sell'

update_user_cache = '/update/user'
update_stock_cache = '/update/stock'
