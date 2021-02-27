#!/bin/bash

network_name=myNetwork

audit_base_name=audit
audit_base_num=1

audit_service_port=6500

audit_service_image=$audit_base_name:$audit_base_num
audit_service_name=$audit_base_name-$audit_base_num

db_base_name=dbmgr
db_base_num=1

db_service_port=5656

db_service_image=$db_base_name:$db_base_num
db_service_name=$db_base_name-$db_base_num

dummy_base_name=dummy-stock
dummy_base_num=1

dummy_service_port=4444

dummy_service_image=$dummy_base_name:$dummy_base_num
dummy_service_name=$dummy_base_name-$dummy_base_num

redis_base_name=redis
redis_base_num=1

redis_service_port=6379

redis_service_image=$redis_base_name:latest
redis_service_name=$redis_base_name-$redis_base_num