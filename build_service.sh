#!/bin/bash

curr_path=$(dirname $0)

$curr_path/DummyStockServer/build_service.sh 2> /dev/null
$curr_path/RedisService/build_service.sh 2> /dev/null
$curr_path/DatabaseService/build_service.sh 2> /dev/null
$curr_path/AuditService/build_service.sh 2> /dev/null
$curr_path/TransactionService/build_service.sh 2> /dev/null
$curr_path/WebService/build_service.sh 2> /dev/null