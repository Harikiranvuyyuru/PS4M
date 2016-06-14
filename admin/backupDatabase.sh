#!/bin/bash
set -e
set -x

temp_file='/tmp/PS4M.db'
if [ $# -gt 1 ]; then
    echo "Usage: $0 [label]"
    exit 1
elif  [ $# -gt 0 ]; then
    echo "Using label: $1"
    temp_file=$temp_file'-'$1
fi
temp_file=$temp_file'-'$(date +\%m-\%d-\%Y)

mysqldump --user=root --password=$DB_PASSWORD PS4M > $temp_file 2> /home/ubuntu/logs/dbBackup.txt
gzip $temp_file
source /etc/environment
aws s3 cp ${temp_file}.gz s3://ps4m/databaseBackup/
rm ${temp_file}.gz
echo [Done]
