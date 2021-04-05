
""" Get Endpoints """
quote_endpoint = '/get/<command:string>/trans/<trans_num:int>/user/<user_id:string>/stock/<stock_symbol:string>'
display_summary_endpoint = '/get/<command:string>/trans/<trans_num:int>/user/<user_id:string>'
dumplog_endpoint = '/get/<command:string>/trans/<trans_num:int>/file/<filename:string>'  # ?user_id=string

""" Post Endpoints """
add_funds_endpoint = '/add'

buy_endpoint = '/buy'
commit_buy_endpoint = '/commit_buy'
cancel_buy_endpoint = '/cancel_buy'

set_buy_amount_endpoint = '/set_buy_amount'
set_buy_trigger_endpoint = '/set_buy_trigger'
cancel_set_buy_endpoint = '/cancel_set_buy'

sell_endpoint = '/sell'
commit_sell_endpoint = '/commit_sell'
cancel_sell_endpoint = '/cancel_sell'

set_sell_amount_endpoint = '/set_sell_amount'
set_sell_trigger_endpoint = '/set_sell_trigger'
cancel_set_sell_endpoint = '/cancel_set_sell'


