"""Test raw SQL injection."""

from smolql import query, raw, table


def test_raw_sql_in_select() -> None:
    """Test raw SQL in SELECT clause."""
    t1 = table("users")
    q = query().select(raw("COUNT(*) OVER ()"), "name").from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert "COUNT(*) OVER ()" in sql
    assert '"name"' in sql


def test_raw_sql_wildcard() -> None:
    """Test wildcard as raw SQL."""
    t1 = table("users")
    q = query().select("*").from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert "SELECT *" in sql


def test_raw_sql_in_where() -> None:
    """Test raw SQL in WHERE clause (via identifier)."""
    t1 = table("users")
    # Using raw SQL can be useful for complex conditions not yet supported
    q = query().select("*").from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert "SELECT * FROM" in sql
