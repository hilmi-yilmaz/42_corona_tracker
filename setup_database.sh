#!/bin/bash

# This script creates a database and tables included in the file given as argument.

# Usage:
# ./setup_database.sh new_database_name tables_file

# Arguments:
#	new_database_name: the name of the database you want to create.
#	tables_file: file containing the name of the tables you want to create. Each table name on a new line.

# Input checking
if [[ "$1" == "" ]] || [[ "$2" == "" ]]; then
	echo "Missing arguments." >&2
	echo "Run as: ./setup_database.sh new_database_name tables_file"
	exit 1
fi

if [[ "$3" != "" ]]; then
	echo "To many arguments."
	echo "Run as: ./setup_database.sh new_database_name tables_file"
	exit 1
fi

# Set variable
DB_NAME="$1"
TABLES="$2"
SQL_FILE="setup_database.sql"

# The temporary sql file.
touch $SQL_FILE

# Create the database
create_database="CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
echo "$create_database" > $SQL_FILE
echo "USE $DB_NAME;" >> $SQL_FILE

# Create the tables
while IFS="" read -r host || [ -n "$host" ]; do
	if [[ "$host" =~ ^f ]]; then
		host_name=${host%%.*}
		echo "CREATE TABLE $host_name (session_id INT, login VARCHAR(100), begin_at DATETIME, end_at DATETIME);" >> $SQL_FILE
	fi
done < $TABLES