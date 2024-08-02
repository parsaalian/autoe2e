#!/bin/bash

# Fix starting problem mysql
# chown -R mysql:mysql /var/lib/mysql /var/run/mysqld
find /var/lib/mysql -type f -exec touch {} \;

# Start mysql
result=$(/etc/init.d/mysql start)
echo "Result starting mysql: " result

# Start npm server
npm start
