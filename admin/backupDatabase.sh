#!/bin/bash
set -e

temp_file=/tmp/PS4M.db-$(date +\%m-\%d-\%Y)
mysqldump --user=root --password=$DB_PASSWORD PS4M > $temp_file 2> /home/ubuntu/logs/dbBackup.txt
gzip $temp_file
aws s3 cp ${temp_file}.gz s3://ps4m/databaseBackup/
rm ${temp_file}.gz
