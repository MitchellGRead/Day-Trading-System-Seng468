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

run_test () {
	get_all_funds
	echo 
	get_all_stocks
	echo
	get_funds_for_user larry
	echo
	sell_stocks larry ANC 101 10000.7878
	echo
	buy_stocks larry ANC 254 25000
	echo
	add_funds larry 12000.45
	echo
	get_funds_for_user larry
	echo
	buy_stocks larry ANC 254 25000
	echo
	sell_stocks larry ANC 101 10000.7878
	echo
	buy_stocks larry ANC 254 2000.3246575
	echo
	get_funds_for_user larry
	echo
	get_stocks_for_user larry
	echo
	sell_stocks larry ANC 101 10000.7878
	echo
	get_funds_for_user larry
	echo
	get_stocks_for_user larry
	echo
}

run_test
