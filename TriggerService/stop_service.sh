#!/bin/bash

source $(dirname $0)/config.sh

cont=$trigger_service_name

echo 'Stopping trigger service...'
sudo docker stop $cont > /dev/null