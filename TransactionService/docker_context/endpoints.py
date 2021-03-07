
""" Get Endpoints """
quote_endpoint = '/get/<command:string>/trans/<trans_num:int>/user/<user_id:string>/stock/<stock_symbol:string>'

""" Post Endpoints """
add_funds_endpoint = '/add'

buy_endpoint = '/buy'
commit_buy_endpoint = '/buy/commit'
cancel_buy_endpoint = '/buy/cancel'

sell_endpoint = '/sell'
commit_sell_endpoint = '/sell/commit'
cancel_sell_endpoint = '/sell/cancel'
