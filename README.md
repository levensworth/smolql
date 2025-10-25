# smolql

A micro SQL statement builder library for Python. **smolql** allows you to easily create SQL statements that can be compiled to various database backends (PostgreSQL, SQLite, and more).

## Features

- 🔧 **Easy to use**: Simple, fluent API for building SQL queries
- 🎯 **Type-safe**: Fully typed Python code with mypy support
- 🔄 **Multi-dialect**: Support for PostgreSQL and SQLite (extensible for more)
- 🧩 **Extensible**: Easy to add new operators and dialects
- 📦 **Lightweight**: Minimal dependencies, focused on query building
- 🎨 **Pythonic**: Natural Python syntax with operator overloading

## Installation

```bash
uv add smolql
```

Or with pip:
```bash
pip install smolql
```

## Quick Start

```python
from smolql import table, query, identifier, placeholder, Dialect, compile_to_sql

# Create table references
users = table('users', schema='public', alias='u')
groups = table('groups', schema='public', alias='g')

# Build a query
q = (
    query()
    .select(
        identifier('full_name', alias='name', table=users),
        identifier('age')
    )
    .from_(users)
    .join(groups, on=users.id == groups.user_id)
    .where(identifier('group_name', table=groups) == placeholder('group_name'))
)

# Compile to SQL
sql = compile_to_sql(q, Dialect.POSTGRESQL)
print(sql)
# SELECT "u"."full_name" AS "name", "age" FROM "public"."users" AS "u" 
# INNER JOIN "public"."groups" AS "g" ON "u"."id" = "g"."user_id" 
# WHERE "g"."group_name" = :group_name
```

## More Natural Syntax

You can use attribute access for a more natural experience:

```python
from smolql import table, query, Dialect, compile_to_sql

users = table('users', alias='u')
groups = table('groups', alias='g')

q = (
    query()
    .select(users.full_name, users.age, groups.name)
    .from_(users)
    .join(groups, on=users.group_id == groups.id)
    .where(users.active == True)
    .order_by(users.full_name, 'ASC')
    .limit(10)
)

sql = compile_to_sql(q, Dialect.POSTGRESQL)
```

## Operators and Functions

smolql supports common SQL operators and functions:

```python
from smolql import (
    table, query, count, sum_, avg, min_, max_, 
    lower, upper, concat, coalesce, now, Dialect, compile_to_sql
)

orders = table('orders', alias='o')
users = table('users', alias='u')

q = (
    query()
    .select(
        users.email,
        count(alias='order_count'),
        sum_(orders.total, alias='total_spent'),
        avg(orders.total, alias='avg_order')
    )
    .from_(orders)
    .join(users, on=orders.user_id == users.id)
    .where(orders.status == 'completed')
    .group_by(users.email)
    .having(count() > 1)
    .order_by(sum_(orders.total), 'DESC')
    .limit(20)
)

sql = compile_to_sql(q, Dialect.POSTGRESQL)
```

### Available Operators

**Aggregate Functions:**
- `count()` - COUNT
- `sum_()` - SUM
- `avg()` - AVG
- `min_()` - MIN
- `max_()` - MAX

**String Functions:**
- `lower()` - LOWER
- `upper()` - UPPER
- `concat()` - CONCAT

**Utility Functions:**
- `coalesce()` - COALESCE
- `cast()` - CAST
- `distinct()` - DISTINCT

**Date/Time Functions:**
- `now()` - NOW
- `current_date()` - CURRENT_DATE
- `current_timestamp()` - CURRENT_TIMESTAMP
- `date_trunc()` - DATE_TRUNC
- `extract()` - EXTRACT

**Window Functions:**
- `row_number()` - ROW_NUMBER
- `rank()` - RANK
- `dense_rank()` - DENSE_RANK
- `lag()` - LAG
- `lead()` - LEAD

**Algebraic Operators:**
```python
# Using Python operators on identifiers
users.age + 1
users.salary * 1.1
users.total / users.count
```

## JOIN Operations

```python
from smolql import table, query

users = table('users', alias='u')
orders = table('orders', alias='o')
products = table('products', alias='p')

q = (
    query()
    .select('*')
    .from_(users)
    .join(orders, on=users.id == orders.user_id)  # INNER JOIN
    .left_join(products, on=orders.product_id == products.id)  # LEFT JOIN
)
```

## WHERE Conditions

```python
from smolql import table, query, placeholder

users = table('users', alias='u')

# Simple conditions
q = query().select('*').from_(users).where(users.age > 18)

# Multiple conditions (combined with AND)
q = query().select('*').from_(users).where(users.age > 18, users.active == True)

# Complex conditions with AND/OR
condition = (users.age > 18) & (users.active == True) | (users.role == 'admin')
q = query().select('*').from_(users).where(condition)

# Using placeholders for parameterized queries
q = query().select('*').from_(users).where(users.name == placeholder('user_name'))
```

## GROUP BY and HAVING

```python
from smolql import table, query, count, sum_

orders = table('orders')

q = (
    query()
    .select('user_id', count(alias='order_count'), sum_('amount', alias='total'))
    .from_(orders)
    .group_by('user_id')
    .having(count() > 5)
)
```

## Raw SQL Injection

For cases where smolql doesn't have direct support yet:

```python
from smolql import table, query, raw

users = table('users')

q = query().select(raw('COUNT(*) OVER ()'), 'name').from_(users)
```

## Supported Dialects

- **PostgreSQL** (`Dialect.POSTGRESQL`)
- **SQLite** (`Dialect.SQLITE`)

Each dialect handles differences like:
- Schema support (PostgreSQL supports schemas, SQLite doesn't)
- Identifier quoting
- Placeholder syntax

## Extending smolql

### Adding Custom Operators

```python
from smolql.domain.entities import Operator, _to_sql_node
from smolql.domain.interfaces import ISQLNode

def my_custom_function(field: ISQLNode | str, alias: str | None = None) -> Operator:
    """Create a custom function operator."""
    return Operator(
        _operator_name="MY_FUNCTION",
        _arguments=[_to_sql_node(field)],
        _alias=alias
    )
```

### Adding New Dialects

Implement the `IVisitor` interface:

```python
from smolql.domain.interfaces import IVisitor

class MySQLVisitor(IVisitor):
    def visit_table(self, table):
        # Implement MySQL-specific table rendering
        pass
    
    # Implement other visit methods...
```

## Development

### Setup

```bash
# Install dependencies
make install

# Run tests
make test

# Run linting
make lint
```

### Requirements

- Python >= 3.10
- uv (for dependency management)

## Architecture

smolql follows Domain-Driven Design principles:

- **Domain Layer**: Interfaces and entities (Table, Query, Identifier, etc.)
- **Services Layer**: Compiler service for different SQL dialects
- **API Layer**: Public functions and operators

The library uses the Visitor pattern for compiling queries to different SQL dialects, making it easy to add new database backends.

## License

MIT License

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass (`make test`)
2. Code follows linting rules (`make lint`)
3. New features include tests
4. Code is well-documented and readable

