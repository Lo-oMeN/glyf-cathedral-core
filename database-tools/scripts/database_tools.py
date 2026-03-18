#!/usr/bin/env python3
"""
Database Tools - Unified database operations for SQL and NoSQL databases.
Supports PostgreSQL, MySQL, SQLite, MongoDB, and Redis.
"""

import argparse
import csv
import json
import sys
import urllib.parse
from typing import Any, Dict, List, Optional, Union

# SQLAlchemy imports
from sqlalchemy import create_engine, inspect, text, MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool

# MongoDB import (optional)
try:
    from pymongo import MongoClient
    from pymongo.database import Database as MongoDatabase
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

# Redis import (optional)
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


def parse_connection_string(conn_string: str, db_type: str = 'postgresql') -> Dict[str, Any]:
    """Parse a connection string and return connection parameters."""
    parsed = urllib.parse.urlparse(conn_string)
    
    # Handle SQLite special case
    if db_type == 'sqlite' or conn_string.startswith('sqlite://'):
        return {
            'type': 'sqlite',
            'database': parsed.path.lstrip('/') if parsed.path else conn_string.replace('sqlite:///', '').replace('sqlite://', '')
        }
    
    # Handle MongoDB
    if db_type == 'mongodb' or conn_string.startswith('mongodb://') or conn_string.startswith('mongodb+srv://'):
        return {
            'type': 'mongodb',
            'uri': conn_string,
            'database': parsed.path.lstrip('/') if parsed.path else None
        }
    
    # Handle Redis
    if db_type == 'redis' or conn_string.startswith('redis://') or conn_string.startswith('rediss://'):
        return {
            'type': 'redis',
            'host': parsed.hostname or 'localhost',
            'port': parsed.port or 6379,
            'password': parsed.password,
            'database': int(parsed.path.lstrip('/')) if parsed.path else 0,
            'ssl': parsed.scheme == 'rediss'
        }
    
    # Handle SQL databases
    return {
        'type': db_type,
        'host': parsed.hostname or 'localhost',
        'port': parsed.port,
        'username': parsed.username,
        'password': parsed.password,
        'database': parsed.path.lstrip('/') if parsed.path else None,
        'query': urllib.parse.parse_qs(parsed.query) if parsed.query else {}
    }


def connect(connection_string: str, db_type: str = 'postgresql', **kwargs) -> Any:
    """
    Create a connection pool to the specified database.
    
    Args:
        connection_string: Database connection string or path (for SQLite)
        db_type: Database type ('postgresql', 'mysql', 'sqlite', 'mongodb', 'redis')
        **kwargs: Additional connection parameters
    
    Returns:
        Connection object (Engine for SQL, Client for MongoDB/Redis)
    """
    parsed = parse_connection_string(connection_string, db_type)
    db_type = parsed['type']
    
    if db_type == 'sqlite':
        # SQLite connection
        db_path = parsed['database']
        if not db_path or db_path == ':memory:':
            engine_url = 'sqlite:///:memory:'
        else:
            engine_url = f'sqlite:///{db_path}'
        
        engine = create_engine(
            engine_url,
            poolclass=QueuePool,
            pool_size=kwargs.get('pool_size', 5),
            max_overflow=kwargs.get('max_overflow', 10),
            pool_timeout=kwargs.get('pool_timeout', 30)
        )
        return engine
    
    elif db_type == 'mongodb':
        if not PYMONGO_AVAILABLE:
            raise ImportError("pymongo is required for MongoDB connections. Install with: pip install pymongo")
        
        client = MongoClient(connection_string)
        # Return client and database name separately
        db_name = parsed.get('database') or kwargs.get('database_name')
        return {'client': client, 'database': db_name}
    
    elif db_type == 'redis':
        if not REDIS_AVAILABLE:
            raise ImportError("redis is required for Redis connections. Install with: pip install redis")
        
        r = redis.Redis(
            host=parsed['host'],
            port=parsed['port'],
            password=parsed['password'],
            db=parsed['database'],
            ssl=parsed.get('ssl', False),
            decode_responses=True,
            **{k: v for k, v in kwargs.items() if k not in ['pool_size', 'max_overflow', 'pool_timeout']}
        )
        # Test connection
        r.ping()
        return r
    
    else:
        # SQL databases (PostgreSQL, MySQL)
        conn_params = []
        if parsed.get('host'):
            conn_params.append(f"host={parsed['host']}")
        if parsed.get('port'):
            conn_params.append(f"port={parsed['port']}")
        if parsed.get('database'):
            conn_params.append(f"dbname={parsed['database']}")
        if parsed.get('username'):
            conn_params.append(f"user={parsed['username']}")
        if parsed.get('password'):
            conn_params.append(f"password={parsed['password']}")
        
        # Add any additional query parameters
        for key, values in parsed.get('query', {}).items():
            for value in values:
                conn_params.append(f"{key}={value}")
        
        conn_str = ' '.join(conn_params)
        
        if db_type == 'postgresql':
            engine_url = f"postgresql+psycopg2://"
            if parsed.get('username'):
                engine_url += f"{parsed['username']}"
                if parsed.get('password'):
                    engine_url += f":{parsed['password']}"
                engine_url += "@"
            if parsed.get('host'):
                engine_url += f"{parsed['host']}"
                if parsed.get('port'):
                    engine_url += f":{parsed['port']}"
            if parsed.get('database'):
                engine_url += f"/{parsed['database']}"
        
        elif db_type == 'mysql':
            engine_url = f"mysql+pymysql://"
            if parsed.get('username'):
                engine_url += f"{parsed['username']}"
                if parsed.get('password'):
                    engine_url += f":{parsed['password']}"
                engine_url += "@"
            if parsed.get('host'):
                engine_url += f"{parsed['host']}"
                if parsed.get('port'):
                    engine_url += f":{parsed['port']}"
            if parsed.get('database'):
                engine_url += f"/{parsed['database']}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        
        engine = create_engine(
            engine_url,
            pool_size=kwargs.get('pool_size', 5),
            max_overflow=kwargs.get('max_overflow', 10),
            pool_timeout=kwargs.get('pool_timeout', 30)
        )
        return engine


def query(connection: Engine, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Execute a SQL query and return results.
    
    Args:
        connection: SQLAlchemy Engine object
        sql: SQL query string
        params: Optional dictionary of query parameters
    
    Returns:
        List of dictionaries representing query results (empty for INSERT/UPDATE/DELETE)
    """
    with connection.connect() as conn:
        result = conn.execute(text(sql), params or {})
        conn.commit()
        # Only return rows for SELECT statements
        if result.returns_rows:
            rows = [dict(row._mapping) for row in result]
            return rows
        return []


def schema(connection: Engine, table_name: str) -> Dict[str, Any]:
    """
    Get the structure of a table.
    
    Args:
        connection: SQLAlchemy Engine object
        table_name: Name of the table
    
    Returns:
        Dictionary containing table schema information
    """
    inspector = inspect(connection)
    
    columns = inspector.get_columns(table_name)
    pk = inspector.get_pk_constraint(table_name)
    fks = inspector.get_foreign_keys(table_name)
    indexes = inspector.get_indexes(table_name)
    
    return {
        'table_name': table_name,
        'columns': [
            {
                'name': col['name'],
                'type': str(col['type']),
                'nullable': col.get('nullable', True),
                'default': col.get('default')
            }
            for col in columns
        ],
        'primary_key': pk.get('constrained_columns', []),
        'foreign_keys': [
            {
                'name': fk.get('name'),
                'constrained_columns': fk.get('constrained_columns', []),
                'referred_table': fk.get('referred_table'),
                'referred_columns': fk.get('referred_columns', [])
            }
            for fk in fks
        ],
        'indexes': [
            {
                'name': idx['name'],
                'columns': idx.get('column_names', []),
                'unique': idx.get('unique', False)
            }
            for idx in indexes
        ]
    }


def tables(connection: Engine) -> List[str]:
    """
    List all tables in the database.
    
    Args:
        connection: SQLAlchemy Engine object
    
    Returns:
        List of table names
    """
    inspector = inspect(connection)
    return inspector.get_table_names()


def export(connection: Engine, table_name: str, output_path: str, format: str = 'csv') -> str:
    """
    Export a table to a file.
    
    Args:
        connection: SQLAlchemy Engine object
        table_name: Name of the table to export
        output_path: Path to the output file
        format: Export format ('csv' or 'json')
    
    Returns:
        Path to the exported file
    """
    data = query(connection, f"SELECT * FROM {table_name}")
    
    if format.lower() == 'csv':
        if not data:
            with open(output_path, 'w', newline='') as f:
                pass
            return output_path
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    elif format.lower() == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    else:
        raise ValueError(f"Unsupported export format: {format}. Use 'csv' or 'json'.")
    
    return output_path


def mongo_query(connection: Dict[str, Any], collection: str, filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Query a MongoDB collection.
    
    Args:
        connection: MongoDB connection dict with 'client' and 'database' keys
        collection: Name of the collection
        filter_dict: MongoDB filter/query dictionary
    
    Returns:
        List of documents
    """
    if not PYMONGO_AVAILABLE:
        raise ImportError("pymongo is required for MongoDB operations. Install with: pip install pymongo")
    
    client = connection['client']
    db_name = connection['database']
    
    if not db_name:
        raise ValueError("Database name is required for MongoDB operations")
    
    db = client[db_name]
    coll = db[collection]
    
    cursor = coll.find(filter_dict or {})
    results = list(cursor)
    
    # Convert ObjectId to string for JSON serialization
    for doc in results:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
    
    return results


def mongo_collections(connection: Dict[str, Any]) -> List[str]:
    """List all collections in a MongoDB database."""
    if not PYMONGO_AVAILABLE:
        raise ImportError("pymongo is required for MongoDB operations. Install with: pip install pymongo")
    
    client = connection['client']
    db_name = connection['database']
    
    if not db_name:
        raise ValueError("Database name is required for MongoDB operations")
    
    db = client[db_name]
    return db.list_collection_names()


def redis_get(connection, key: str) -> Optional[str]:
    """
    Get a value from Redis.
    
    Args:
        connection: Redis connection object
        key: Redis key
    
    Returns:
        Value as string, or None if key doesn't exist
    """
    if not REDIS_AVAILABLE:
        raise ImportError("redis is required for Redis operations. Install with: pip install redis")
    
    value = connection.get(key)
    return value.decode('utf-8') if isinstance(value, bytes) else value


def redis_set(connection, key: str, value: str, expire: Optional[int] = None) -> bool:
    """
    Set a value in Redis.
    
    Args:
        connection: Redis connection object
        key: Redis key
        value: Value to store
        expire: Optional TTL in seconds
    
    Returns:
        True if successful
    """
    if not REDIS_AVAILABLE:
        raise ImportError("redis is required for Redis operations. Install with: pip install redis")
    
    return connection.set(key, value, ex=expire)


def redis_keys(connection, pattern: str = '*') -> List[str]:
    """List Redis keys matching a pattern."""
    if not REDIS_AVAILABLE:
        raise ImportError("redis is required for Redis operations. Install with: pip install redis")
    
    return list(connection.scan_iter(match=pattern))


def main():
    parser = argparse.ArgumentParser(description='Database Tools CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Connect command
    connect_parser = subparsers.add_parser('connect', help='Test database connection')
    connect_parser.add_argument('connection_string', help='Database connection string')
    connect_parser.add_argument('--type', default='postgresql', help='Database type')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Execute SQL query')
    query_parser.add_argument('connection_string', help='Database connection string')
    query_parser.add_argument('sql', help='SQL query')
    query_parser.add_argument('--type', default='sqlite', help='Database type')
    
    # Tables command
    tables_parser = subparsers.add_parser('tables', help='List tables')
    tables_parser.add_argument('connection_string', help='Database connection string')
    tables_parser.add_argument('--type', default='sqlite', help='Database type')
    
    # Schema command
    schema_parser = subparsers.add_parser('schema', help='Show table schema')
    schema_parser.add_argument('connection_string', help='Database connection string')
    schema_parser.add_argument('table_name', help='Table name')
    schema_parser.add_argument('--type', default='sqlite', help='Database type')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export table to file')
    export_parser.add_argument('connection_string', help='Database connection string')
    export_parser.add_argument('table_name', help='Table name')
    export_parser.add_argument('output_path', help='Output file path')
    export_parser.add_argument('--format', default='csv', choices=['csv', 'json'], help='Export format')
    export_parser.add_argument('--type', default='sqlite', help='Database type')
    
    # MongoDB query command
    mongo_parser = subparsers.add_parser('mongo-query', help='Query MongoDB collection')
    mongo_parser.add_argument('connection_string', help='MongoDB connection string')
    mongo_parser.add_argument('database', help='Database name')
    mongo_parser.add_argument('collection', help='Collection name')
    mongo_parser.add_argument('--filter', default='{}', help='JSON filter string')
    
    # MongoDB collections command
    mongo_coll_parser = subparsers.add_parser('mongo-collections', help='List MongoDB collections')
    mongo_coll_parser.add_argument('connection_string', help='MongoDB connection string')
    mongo_coll_parser.add_argument('database', help='Database name')
    
    # Redis get command
    redis_get_parser = subparsers.add_parser('redis-get', help='Get Redis value')
    redis_get_parser.add_argument('connection_string', help='Redis connection string')
    redis_get_parser.add_argument('key', help='Redis key')
    
    # Redis set command
    redis_set_parser = subparsers.add_parser('redis-set', help='Set Redis value')
    redis_set_parser.add_argument('connection_string', help='Redis connection string')
    redis_set_parser.add_argument('key', help='Redis key')
    redis_set_parser.add_argument('value', help='Value to set')
    redis_set_parser.add_argument('--expire', type=int, help='TTL in seconds')
    
    # Redis keys command
    redis_keys_parser = subparsers.add_parser('redis-keys', help='List Redis keys')
    redis_keys_parser.add_argument('connection_string', help='Redis connection string')
    redis_keys_parser.add_argument('--pattern', default='*', help='Key pattern')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'connect':
            conn = connect(args.connection_string, args.type)
            if isinstance(conn, dict) and 'client' in conn:
                # MongoDB
                print(f"Connected to MongoDB (database: {conn['database'] or 'not specified'})")
            else:
                print(f"Connected to {args.type}")
        
        elif args.command == 'query':
            conn = connect(args.connection_string, args.type)
            results = query(conn, args.sql)
            print(json.dumps(results, indent=2, default=str))
        
        elif args.command == 'tables':
            conn = connect(args.connection_string, args.type)
            if args.type == 'mongodb':
                results = mongo_collections(conn)
            else:
                results = tables(conn)
            print(json.dumps(results, indent=2))
        
        elif args.command == 'schema':
            conn = connect(args.connection_string, args.type)
            results = schema(conn, args.table_name)
            print(json.dumps(results, indent=2))
        
        elif args.command == 'export':
            conn = connect(args.connection_string, args.type)
            path = export(conn, args.table_name, args.output_path, args.format)
            print(f"Exported to {path}")
        
        elif args.command == 'mongo-query':
            conn = connect(args.connection_string, 'mongodb')
            conn['database'] = args.database
            filter_dict = json.loads(args.filter)
            results = mongo_query(conn, args.collection, filter_dict)
            print(json.dumps(results, indent=2))
        
        elif args.command == 'mongo-collections':
            conn = connect(args.connection_string, 'mongodb')
            conn['database'] = args.database
            results = mongo_collections(conn)
            print(json.dumps(results, indent=2))
        
        elif args.command == 'redis-get':
            conn = connect(args.connection_string, 'redis')
            value = redis_get(conn, args.key)
            print(value if value else "(nil)")
        
        elif args.command == 'redis-set':
            conn = connect(args.connection_string, 'redis')
            result = redis_set(conn, args.key, args.value, args.expire)
            print("OK" if result else "FAILED")
        
        elif args.command == 'redis-keys':
            conn = connect(args.connection_string, 'redis')
            results = redis_keys(conn, args.pattern)
            print(json.dumps(results, indent=2))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
