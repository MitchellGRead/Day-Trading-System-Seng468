#!/bin/bash

source $(dirname $0)/config.sh

cont=$audit_service_name

echo 'Stopping audit service...'
sudo docker stop $cont > /dev/null