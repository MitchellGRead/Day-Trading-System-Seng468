#!/bin/bash

source $(dirname $0)/dbconfig.sh

pgres_id=$(sudo -s docker ps -aq --filter NAME=$postgres_db_name)
mongo_id=$(sudo -s docker ps -aq --filter NAME=$mongo_db_name)

if [[ -z $pgres_id  ]]
then
	echo "Starting Postgres container"
	$(dirname $0)/PostgreSQL/start_container.sh
else
	:
fi