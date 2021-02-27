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