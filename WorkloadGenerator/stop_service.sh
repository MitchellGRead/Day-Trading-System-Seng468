#!/bin/bash

source $(dirname $0)/config.sh

cont=$generator_name

echo 'Stopping generator...'
sudo docker stop $cont > /dev/null