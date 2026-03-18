---
name: database-tools
description: Unified database operations for SQL and NoSQL databases. Use when working with PostgreSQL, MySQL, SQLite, MongoDB, or Redis to perform connection management, querying, schema inspection, data export, and CRUD operations.
---

# Database Tools

Unified database operations supporting PostgreSQL, MySQL, SQLite, MongoDB, and Redis.

## Installation

```bash
pip install sqlalchemy pymongo redis
```

For PostgreSQL, also install:
```bash
pip install psycopg2-binary
```

For MySQL, also install:
```bash
pip install pymysql
```

## Quick Start

```python
from scripts.database_tools import connect, query, tables, schema, export

# Connect to SQLite
conn = connect('database.db', 'sqlite')

# Query data
results = query(conn, "SELECT * FROM users WHERE age > :age", {"age": 18})

# List tables
table_list = tables(conn)

# Get table schema
table_schema = schema(conn, 'users')

# Export to CSV
export(conn, 'users', 'users.csv', 'csv')
```

## API Reference

### SQL Databases (PostgreSQL, MySQL, SQLite)

#### connect(connection_string, db_type='postgresql', **kwargs)
Create a database connection.

**Parameters:**
- `connection_string`: Database connection string or path (SQLite)
- `db_type`: One of 'postgresql', 'mysql', 'sqlite', 'mongodb', 'redis'
- `**kwargs`: Connection pool options (pool_size, max_overflow, pool_timeout)

**Connection String Examples:**
```python
# SQLite
connect('data.db', 'sqlite')
connect('/path/to/data.db', 'sqlite')

# PostgreSQL
connect('postgresql://user:pass@localhost:5432/dbname')
connect('localhost:5432/dbname', 'postgresql')

# MySQL
connect('mysql://user:pass@localhost:3306/dbname')
connect('localhost:3306/dbname', 'mysql')
```

#### query(connection, sql, params=None)
Execute SQL and return results as list of dictionaries.

```python
results = query(conn, "SELECT * FROM users WHERE id = :id", {"id": 1})
# Returns: [{"id": 1, "name": "Alice", "email": "alice@example.com"}]
```

#### tables(connection)
List all tables in the database.

```python
table_names = tables(conn)  # ['users', 'orders', 'products']
```

#### schema(connection, table_name)
Get detailed table structure including columns, primary keys, foreign keys, and indexes.

```python
schema_info = schema(conn, 'users')
# Returns: {
#   "table_name": "users",
#   "columns": [{"name": "id", "type": "INTEGER", "nullable": false}, ...],
#   "primary_key": ["id"],
#   "foreign_keys": [...],
#   "indexes": [...]
# }
```

#### export(connection, table_name, output_path, format='csv')
Export table data to CSV or JSON.

```python
export(conn, 'users', 'users.csv', 'csv')
export(conn, 'users', 'users.json', 'json')
```

### MongoDB

#### connect(connection_string, 'mongodb')
Connect to MongoDB. Returns dict with 'client' and 'database' keys.

```python
conn = connect('mongodb://localhost:27017/mydb', 'mongodb')
# Or without database in URI:
conn = connect('mongodb://localhost:27017', 'mongodb')
conn['database'] = 'mydb'  # Set database name separately
```

#### mongo_query(connection, collection, filter_dict)
Query MongoDB collection.

```python
results = mongo_query(conn, 'users', {'age': {'$gte': 18}})
# Returns list of documents with ObjectId converted to string
```

#### mongo_collections(connection)
List all collections in the database.

```python
collections = mongo_collections(conn)  # ['users', 'orders']
```

### Redis

#### connect(connection_string, 'redis')
Connect to Redis.

```python
conn = connect('redis://localhost:6379/0', 'redis')
# With password:
conn = connect('redis://:password@localhost:6379/0', 'redis')
```

#### redis_get(connection, key)
Get a value by key.

```python
value = redis_get(conn, 'user:1')  # Returns string or None
```

#### redis_set(connection, key, value, expire=None)
Set a value with optional TTL (in seconds).

```python
redis_set(conn, 'user:1', 'Alice')
redis_set(conn, 'temp_key', 'value', expire=300)  # Expires in 5 minutes
```

#### redis_keys(connection, pattern='*')
List keys matching a pattern.

```python
keys = redis_keys(conn, 'user:*')  # ['user:1', 'user:2', ...]
```

## CLI Usage

The script can also be used from the command line:

```bash
# Connect test
python3 scripts/database_tools.py connect "database.db" --type sqlite

# Execute query
python3 scripts/database_tools.py query "database.db" "SELECT * FROM users" --type sqlite

# List tables
python3 scripts/database_tools.py tables "database.db" --type sqlite

# Show schema
python3 scripts/database_tools.py schema "database.db" "users" --type sqlite

# Export table
python3 scripts/database_tools.py export "database.db" "users" "output.csv" --type sqlite --format csv

# MongoDB query
python3 scripts/database_tools.py mongo-query "mongodb://localhost:27017" "mydb" "users" --filter '{"age": {"$gte": 18}}'

# Redis operations
python3 scripts/database_tools.py redis-get "redis://localhost:6379" "mykey"
python3 scripts/database_tools.py redis-set "redis://localhost:6379" "mykey" "myvalue" --expire 300
python3 scripts/database_tools.py redis-keys "redis://localhost:6379" --pattern "user:*"
```

## Resources

### scripts/
- `database_tools.py` - Main module with all database operations
