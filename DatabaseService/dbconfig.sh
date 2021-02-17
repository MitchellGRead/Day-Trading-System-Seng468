#!/bin/bash

postgres_tag=13
postgres_name=trading-db

postgres_image_name=$postgres_name:$postgres_tag
postgres_db_name=$postgres_name-$postgres_tag

mongo_tag=4.4
mongo_name=mongo-db

mongo_image_name=$mongo_name:$mongo_tag
mongo_db_name=$mongo_name-$mongo_tag