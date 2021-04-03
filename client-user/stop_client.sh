#!/bin/bash

source $(dirname $0)/config.sh 

cont=$client_name

echo 'Stopping client...'
sudo docker stop $cont > /dev/null