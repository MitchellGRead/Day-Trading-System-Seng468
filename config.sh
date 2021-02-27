#!/bin/bash

audit_base_name=audit
audit_base_num=1

audit_service_port=6500

audit_service_image=$audit_base_name:$audit_base_num
audit_service_name=$audit_base_name-$audit_base_num