#!/bin/bash
set -e

# First, in /etc/environment, set values for: COOKIE_SECRET_KEY, DB_PASSWORD, USER_PASSWORD_SALT

# This script is intended to be run on top of a fresh install of Ubuntu

apt-get update
apt-get install emacs23 git libmysqlclient-dev mysql-server nginx python-dev python-pip zsh

# python dependencies
sudo pip install MySQL-python==1.2.3 pyramid==1.4a2 supervisor zope.interface==4.0.1 awscli


git clone https://github.com/TobyRoseman/PS4M.git
mkdir ~PS4M/var ~logs

# Create database
echo 'create database PS4M;' | mysql --user=root --password=$DB_PASSWORD
mysql --user=root --password=$DB_PASSWORD PS4M <  /tmp/database_dump.sql

mkdir -p /data/nginx/cache

# In /etc/mysql/my.cnf add the following lines, in the [mysqld] section:
# log-bin=mysql-bin
# server-id=1
# and bind address to 0.0.0.0

