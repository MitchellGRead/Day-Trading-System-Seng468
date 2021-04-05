#!/bin/bash
curr_path=$(dirname $0)
source $curr_path/config.sh

echo 'Checking container logs for errors...'

echo 'Database Service errors:'
sudo docker logs $db_service_name | grep 'ERROR'

echo 'Cache Service errors:'
sudo docker logs $cache_service_name | grep 'ERROR'

echo 'Redis Service errors:'
sudo docker logs $redis_service_name | grep 'ERROR'

echo 'Triggers Service errors:'
sudo docker logs $trigger_service_name | grep 'ERROR'

echo 'Audit Service errors:'
sudo docker logs $audit_service_name | grep 'ERROR'

echo 'Web Service errors:'
sudo docker logs $web_service_name | grep 'ERROR'

echo 'Dummy Stock Service errors:'
sudo docker logs $dummy_service_name | grep 'ERROR'

