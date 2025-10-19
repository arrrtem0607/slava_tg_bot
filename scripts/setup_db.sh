#!/bin/bash

DB_USER="magic_user"
DB_PASSWORD="magic_pass"
DB_NAME="magic_db"

set -e

echo "Creating PostgreSQL user and database..."

psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "✅ Database and user created successfully."
