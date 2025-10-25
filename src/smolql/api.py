"""Public API helper functions."""

from smolql.domain.entities import (
    Identifier,
    Placeholder,
    Predicate,
    Query,
    RawSQL,
    Table,
)
from smolql.domain.value_objects import Dialect
from smolql.services.compiler_service import compile_query


def table(name: str, schema: str | None = None, alias: str | None = None) -> Table:
    """Create a table reference."""
    return Table(_name=name, _schema=schema, _alias=alias)


def identifier(
    name: str, table: Table | None = None, alias: str | None = None
) -> Identifier:
    """Create a column identifier."""
    return Identifier(_name=name, _table=table, _alias=alias)


def placeholder(name: str) -> Placeholder:
    """Create a parameter placeholder."""
    return Placeholder(_name=name)


def predicate(condition: Predicate) -> Predicate:
    """Create a predicate (mainly for clarity in code)."""
    return condition


def raw(sql: str) -> RawSQL:
    """Create a raw SQL node for direct injection."""
    return RawSQL(_sql=sql)


def query() -> Query:
    """Create a new query builder."""
    return Query(_select_fields=[])


def compile_to_sql(query_obj: Query, dialect: Dialect) -> str:
    """Compile a query to SQL string."""
    return compile_query(query_obj, dialect)
