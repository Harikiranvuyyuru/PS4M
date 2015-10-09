#!/bin/bash
set -e
set -x

temp_file=/tmp/PS4M.db-$(date +\%m-\%d-\%Y)
mysqldump --user=root --password=$DB_PASSWORD PS4M > $temp_file 2> /home/ubuntu/logs/dbBackup.txt
gzip $temp_file
source /etc/environment
aws s3 cp ${temp_file}.gz s3://ps4m/databaseBackup/
rm ${temp_file}.gz
echo [Done]

