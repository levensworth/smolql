"""Compiler service for converting queries to SQL strings."""

from smolql.domain import interfaces
from smolql.domain.value_objects import Dialect

from smolql.services.postgres_visitor import PostgreSQLVisitor
from smolql.services.sqlite_visitor import SQLiteVisitor


def compile_query(query: interfaces.IQuery, dialect: Dialect) -> str:
    """Compile a query to SQL string for the given dialect."""
    if dialect == Dialect.POSTGRESQL:
        visitor = PostgreSQLVisitor()
    elif dialect == Dialect.SQLITE:
        visitor = SQLiteVisitor()
    else:
        raise ValueError(f"Unsupported dialect: {dialect}")

    return query.accept(visitor)
