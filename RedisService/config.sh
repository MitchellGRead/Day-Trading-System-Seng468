#!/bin/bash

redis_base_name=redis
redis_base_num=1

redis_service_port=6379

redis_service_image=$redis_base_name:latest
redis_service_name=$redis_base_name-$redis_base_num