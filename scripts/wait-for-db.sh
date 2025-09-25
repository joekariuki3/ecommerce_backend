#!/bin/bash
set -e

echo "Checking database connectivity..."

# Wait for PostgreSQL server to be ready
echo "Waiting for database server..."
for i in {1..30}; do
    if python -c "
import psycopg2, os
try:
    conn = psycopg2.connect(
        host='db',
        port='5432',
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        dbname='postgres'
    )
    conn.close()
    print('Database server is ready!')
    exit(0)
except psycopg2.OperationalError:
    exit(1)
" 2>/dev/null; then
        break
    fi
    echo "Waiting for database server... ($i/30)"
    sleep 2
done

if [ $i -eq 30 ]; then
    echo "Database server not ready after 60 seconds"
    exit 1
fi

# Check if our database exists, create if not
echo "Checking if database ${DB_NAME} exists..."
if python -c "
import psycopg2, os
try:
    conn = psycopg2.connect(
        host='db',
        port='5432',
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        dbname=os.getenv('DB_NAME')
    )
    conn.close()
    print(f'Database {os.getenv(\"DB_NAME\")} exists and is accessible!')
    exit(0)
except psycopg2.OperationalError:
    exit(1)
" 2>/dev/null; then
    echo "Database check completed successfully"
else
    echo "Database ${DB_NAME} does not exist, creating..."
    python -c "
import psycopg2, os
conn = psycopg2.connect(
    host='db',
    port='5432',
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    dbname='postgres'
)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute(f'CREATE DATABASE {os.getenv(\"DB_NAME\")};')
cursor.close()
conn.close()
print(f'Database {os.getenv(\"DB_NAME\")} created successfully!')
"
fi

echo "Database setup completed!"