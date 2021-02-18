#!/bin/bash

curr_path=$(dirname $0)

$curr_path/WebService/stop_service.sh 2> /dev/null
$curr_path/TransactionService/stop_service.sh 2> /dev/null
$curr_path/TriggerService/stop_service.sh 2> /dev/null
$curr_path/DummyStockServer/stop_service.sh 2> /dev/null
$curr_path/RedisService/stop_service.sh 2> /dev/null
$curr_path/DatabaseService/stop_service.sh 2> /dev/null
$curr_path/AuditService/stop_service.sh 2> /dev/null