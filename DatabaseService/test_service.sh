#!/bin/bash

base_url=http://localhost:5656

add_funds () {
	local id=\"$1\"
	local funds=$2
	echo Adding \$$funds to $id
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$id, \"funds\":$funds}" $base_url/funds/add_funds
}

buy_stocks () {
	local user=\"$1\"
	local stock=\"$2\"
	local amount=$3
	local funds=$4
	echo Buying $amount $stock stocks for $user at cost of $funds
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock, \"stock_amount\":$amount, \"funds\":$funds}" $base_url/stocks/buy_stocks
}

sell_stocks () {
	local user=\"$1\"
	local stock=\"$2\"
	local amount=$3
	local funds=$4
	echo Selling $amount $stock stocks for $user at cost of $funds
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock, \"stock_amount\":$amount, \"funds\":$funds}" $base_url/stocks/sell_stocks
}

set_buy_trigger_amount () {
	local user=\"$1\"
	local stock=\"$2\"
	local amount=$3
	echo Setting buy trigger amount for $user for stock $stock at amount $amount
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock, \"amount\":$amount}" $base_url/triggers/buy/set/amount
}

set_buy_trigger_price () {
	local user=\"$1\"
	local stock=\"$2\"
	local price=$3
	local trans_num=999
	echo Setting buy trigger price for $user for stock $stock at price $price
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock, \"price\":$price, \"transaction_num\": $trans_num}" $base_url/triggers/buy/set/price
}

set_buy_trigger () {
	local user=$1
	local stock=$2
	local amount=$3
	local price=$4
	set_buy_trigger_amount $user $stock $amount
	echo
	set_buy_trigger_price $user $stock $price
}

execute_buy_trigger () {
	local user=\"$1\"
	local stock=\"$2\"
	local funds=$3
	echo Executing buy trigger for user $user, stock $stock for total of $funds
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock, \"funds\":$funds}" $base_url/triggers/execute/buy
}

cancel_buy_trigger () {
	local user=\"$1\"
	local stock=\"$2\"
	echo Cancelling buy trigger for $user for stock $stock
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock}" $base_url/triggers/buy/cancel
}

set_sell_trigger_amount () {
	local user=\"$1\"
	local stock=\"$2\"
	local amount=$3
	echo Setting sell trigger amount for $user for stock $stock at amount $amount
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock, \"amount\":$amount}" $base_url/triggers/sell/set/amount
}

set_sell_trigger_price () {
	local user=\"$1\"
	local stock=\"$2\"
	local price=$3
	local trans_num=888
	echo Setting sell trigger price for $user for stock $stock at price $price
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock, \"price\":$price, \"transaction_num\": $trans_num}" $base_url/triggers/sell/set/price
}

set_sell_trigger () {
	local user=$1
	local stock=$2
	local amount=$3
	local price=$4
	set_sell_trigger_amount $user $stock $amount
	echo
	set_sell_trigger_price $user $stock $price
}

execute_sell_trigger () {
	local user=\"$1\"
	local stock=\"$2\"
	local funds=$3
	echo Executing sell trigger for user $user, stock $stock for total of $funds
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock, \"funds\":$funds}" $base_url/triggers/execute/sell
}

cancel_sell_trigger () {
	local user=\"$1\"
	local stock=\"$2\"
	echo Cancelling sell trigger for $user for stock $stock
	curl --header "Content-Type: application/json" --request POST --data "{\"user_id\":$user, \"stock_symbol\":$stock}" $base_url/triggers/sell/cancel
}

get_all_funds () {
	echo Getting funds for all users
	curl --request GET $base_url/funds/get/all
}

get_funds_for_user () {
	local user=$1
	echo Getting funds for $user
	curl --request GET $base_url/funds/get/user/$user
}

get_all_stocks () {
	echo Getting stocks for all stocks
	curl --request GET $base_url/stocks/get/all
}

get_stocks_for_user () {
	local user=$1
	echo Getting stocks for $user
	curl --request GET $base_url/stocks/get/user/$user
}

get_all_bulk_triggers() {
	echo Getting triggers for all users through the bulk endpoint
	curl --request GET $base_url/triggers/all/get
}

get_all_triggers() {
	echo Getting triggers for all users
	echo Buy triggers:
	curl --request GET $base_url/triggers/buy/get/all
	echo
	echo Sell triggers:
	curl --request GET $base_url/triggers/sell/get/all
}

get_user_triggers() {
	local user=$1
	echo Getting triggers for $user
	echo Buy triggers:
	curl --request GET $base_url/triggers/buy/get/user/$user
	echo
	echo Sell triggers:
	curl --request GET $base_url/triggers/sell/get/user/$user
}

get_all_users_info() {
	get_all_funds
	echo && echo
	get_all_stocks
	echo && echo
	get_all_triggers
	echo && echo
	get_all_bulk_triggers
}

get_user_info() {
	local user=$1
	get_funds_for_user $user
	echo && echo
	get_stocks_for_user $user
	echo && echo
	get_user_triggers $user
}

run_test () {
	# No user exists on clean state
	get_all_users_info
	echo && echo
	get_user_info larry
	echo && echo
	sell_stocks larry ANC 101 10000.7878
	echo && echo
	buy_stocks larry ANC 254 25000
	echo && echo
	set_buy_trigger larry ABC 5000 500
	echo && echo
	set_sell_trigger larry DEF 500 5000
	echo && echo
	execute_buy_trigger larry ABC 5000
	echo && echo
	execute_sell_trigger larry ABC 50000
	echo && echo
	cancel_buy_trigger larry ABC
	echo && echo
	cancel_sell_trigger larry DEF
	echo && echo

	# User creation
	add_funds larry 12000.45
	echo && echo
	get_all_users_info
	echo && echo
	set_buy_trigger_price larry XYZ 4000
	echo && echo
	set_sell_trigger_price larry UVW 5500
	echo && echo
	get_user_info larry
	echo && echo
	buy_stocks larry ANC 254 25000
	echo && echo
	sell_stocks larry ANC 101 10000.7878
	echo && echo
	buy_stocks larry ANC 254 2000.3246575
	echo && echo
	get_user_info larry
	echo && echo
	sell_stocks larry ANC 101 10000.7878
	echo && echo
	get_user_info larry
	echo && echo
	cancel_buy_trigger larry ABC
	echo && echo
	cancel_sell_trigger larry DEF
	echo && echo
	set_buy_trigger larry ABC 5000 500
	echo && echo
	set_sell_trigger larry DEF 500 5000
	echo && echo
	get_user_info larry
	echo && echo
	set_buy_trigger larry ABC 5000 1.1
	echo && echo
	set_sell_trigger larry ANC 50 5000
	echo && echo
	get_user_info larry
	echo && echo
	get_all_users_info
	echo && echo
	set_buy_trigger larry ABC 2000 1.1
	echo && echo
	set_sell_trigger larry ANC 25 5000
	echo && echo
	execute_buy_trigger larry XYZ 5000
	echo && echo
	execute_sell_trigger larry UVW 50000
	echo && echo
	get_user_info larry
	echo && echo
	cancel_buy_trigger larry ABC
	echo && echo
	cancel_sell_trigger larry ANC
	echo && echo
	get_user_info larry
	echo && echo
	set_buy_trigger larry ABC 2000 1.1
	echo && echo
	set_sell_trigger larry ANC 25 100
	echo && echo
	get_user_info larry
	echo && echo
	execute_buy_trigger larry ABC 2000
	echo && echo
	execute_sell_trigger larry ANC 5000
	echo && echo
	get_user_info larry
	echo && echo
	get_all_users_info
	echo && echo
}

run_test
