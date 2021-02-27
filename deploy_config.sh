#!/bin/bash

curr_path=$(dirname $0)

cp $curr_path/config.py $curr_path/AuditService/docker_context
cp $curr_path/config.sh $curr_path/AuditService/config.sh

cp $curr_path/config.py $curr_path/DatabaseService/docker_context
cp $curr_path/config.sh $curr_path/DatabaseService/config.sh

cp $curr_path/config.py $curr_path/DummyStockServer/docker_context
cp $curr_path/config.sh $curr_path/DummyStockServer/config.sh

# cp $curr_path/config.py $curr_path/AuditService/docker_context
# cp $curr_path/config.sh $curr_path/AuditService/config.sh

# cp $curr_path/config.py $curr_path/AuditService/docker_context
# cp $curr_path/config.sh $curr_path/AuditService/config.sh
