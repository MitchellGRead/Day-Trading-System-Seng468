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

run_test () {
	get_all_funds
	echo && echo
	get_all_stocks
	echo && echo
	get_all_triggers
	echo && echo
	get_funds_for_user larry
	echo && echo
	get_user_triggers larry
	echo && echo
	sell_stocks larry ANC 101 10000.7878
	echo && echo
	buy_stocks larry ANC 254 25000
	echo && echo
	add_funds larry 12000.45
	echo && echo
	get_funds_for_user larry
	echo && echo
	buy_stocks larry ANC 254 25000
	echo && echo
	sell_stocks larry ANC 101 10000.7878
	echo && echo
	buy_stocks larry ANC 254 2000.3246575
	echo && echo
	get_funds_for_user larry
	echo && echo
	get_stocks_for_user larry
	echo && echo
	sell_stocks larry ANC 101 10000.7878
	echo && echo
	get_funds_for_user larry
	echo && echo
	get_stocks_for_user larry
	echo && echo
	get_user_triggers larry
	echo && echo
}

run_test
