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

cache_base_name=cache
cache_base_num=1

cache_service_port=9999

cache_service_image=$cache_base_name:$cache_base_num
cache_service_name=$cache_base_name-$cache_base_num

trans_base_name=trsrvr
trans_base_num=1

trans_service_port=6666

trans_service_image=$trans_base_name:$trans_base_num
trans_service_name=$trans_base_name-$trans_base_num

trigger_base_name=trigger
trigger_base_num=1

trigger_service_port=7000

trigger_service_image=$trigger_base_name:$trigger_base_num
trigger_service_name=$trigger_base_name-$trigger_base_num

web_base_name=web
web_base_num=1

web_service_port=5000

web_service_image=$web_base_name:$web_base_num
web_service_name=$web_base_name-$web_base_num

generator_base_name=gen
generator_base_num=1

generator_port=5555

generator_image=$generator_base_name:$generator_base_num
generator_name=$generator_base_name-$generator_base_num

client_base_name=client
client_base_num=1

client_port=3000

client_image=$client_base_name:$client_base_num
client_name=$client_base_name-$client_base_num