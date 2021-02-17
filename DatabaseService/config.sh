#!/bin/bash

db_base_name=dbmgr
db_base_num=1

db_service_port=5656

db_service_image=$db_base_name:$db_base_num
db_service_name=$db_base_name-$db_base_num