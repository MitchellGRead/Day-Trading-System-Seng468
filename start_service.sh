#!/bin/bash

echo 'Creating docker network for containers...'
sudo docker network create myNetwork >/dev/null 2>&1

curr_path=$(dirname $0)

$curr_path/DummyStockServer/start_service.sh
$curr_path/RedisService/start_service.sh
$curr_path/DatabaseService/start_service.sh
$curr_path/AuditService/start_service.sh
$curr_path/TriggerService/start_service.sh
$curr_path/TransactionService/start_service.sh
$curr_path/WebService/start_service.sh