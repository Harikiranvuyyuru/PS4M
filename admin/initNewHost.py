# In /etc/environment, set values for: COOKIE_SECRET_KEY, DB_PASSWORD, USER_PASSWORD_SALT

# mysql

# python dependencies

# Create database
mysql --user=root --password=$DB_PASSWORD PS4M <  /tmp/database_dump.sql
