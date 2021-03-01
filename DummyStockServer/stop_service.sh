#!/bin/bash

source $(dirname $0)/config.sh

cont=$dummy_service_name

echo 'Stopping dummy stock service...'
sudo docker stop $cont > /dev/null