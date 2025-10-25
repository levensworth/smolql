"""Test different SQL dialects."""

from smolql import Dialect, compile_to_sql, query, table
from smolql.services.compiler_service import PostgreSQLVisitor, SQLiteVisitor


def test_postgresql_dialect() -> None:
    """Test PostgreSQL dialect compilation."""
    t1 = table("users", schema="public", alias="u")
    q = query().select("*").from_(t1).where(t1.age > 18)

    sql = q.accept(PostgreSQLVisitor())
    assert '"public"."users"' in sql
    assert 'AS "u"' in sql


def test_sqlite_dialect() -> None:
    """Test SQLite dialect compilation."""
    t1 = table("users", alias="u")
    q = query().select("*").from_(t1).where(t1.age > 18)

    sql = q.accept(SQLiteVisitor())
    # SQLite should not include schema
    assert '"users" AS "u"' in sql
    assert "public" not in sql


def test_compile_to_sql_postgresql() -> None:
    """Test compile_to_sql with PostgreSQL."""
    t1 = table("users")
    q = query().select("*").from_(t1)

    sql = compile_to_sql(q, Dialect.POSTGRESQL)
    assert "SELECT" in sql
    assert "FROM" in sql


def test_compile_to_sql_sqlite() -> None:
    """Test compile_to_sql with SQLite."""
    t1 = table("users")
    q = query().select("*").from_(t1)

    sql = compile_to_sql(q, Dialect.SQLITE)
    assert "SELECT" in sql
    assert "FROM" in sql


def test_schema_handling() -> None:
    """Test schema handling differs between dialects."""
    t1 = table("users", schema="public")

    pg_sql = t1.accept(PostgreSQLVisitor())
    sqlite_sql = t1.accept(SQLiteVisitor())

    # PostgreSQL includes schema
    assert '"public"."users"' in pg_sql
    # SQLite does not
    assert "public" not in sqlite_sql
    assert '"users"' in sqlite_sql
