#!/bin/bash

trigger_base_name=trigger
trigger_base_num=1

trigger_service_port=7000

trigger_service_image=$trigger_base_name:$trigger_base_num
trigger_service_name=$trigger_base_name-$trigger_base_num