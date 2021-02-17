#!/bin/bash

source $(dirname $0)/config.sh

cont=$trans_service_name

echo 'Stopping transaction service...'
sudo docker stop $cont > /dev/null