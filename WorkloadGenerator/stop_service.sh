#!/bin/bash

source $(dirname $0)/config.sh

cont=$web_service_name

echo 'Stopping generator...'
sudo docker stop $cont > /dev/null