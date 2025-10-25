"""Test GROUP BY and HAVING functionality."""

from smolql import count, identifier, query, sum_, table


def test_group_by() -> None:
    """Test GROUP BY clause."""
    t1 = table("orders")
    q = (
        query()
        .select(identifier("user_id"), count(alias="order_count"))
        .from_(t1)
        .group_by("user_id")
    )

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'GROUP BY "user_id"' in sql


def test_group_by_multiple_fields() -> None:
    """Test GROUP BY with multiple fields."""
    t1 = table("orders")
    q = (
        query()
        .select(identifier("user_id"), identifier("status"), count(alias="count"))
        .from_(t1)
        .group_by("user_id", "status")
    )

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'GROUP BY "user_id", "status"' in sql


def test_having() -> None:
    """Test HAVING clause."""
    t1 = table("orders", alias="o")
    q = (
        query()
        .select(identifier("user_id", table=t1), count(alias="order_count"))
        .from_(t1)
        .group_by(identifier("user_id", table=t1))
        .having(count() > 5)
    )

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert "GROUP BY" in sql
    assert "HAVING COUNT(*) > 5" in sql


def test_group_by_with_aggregates() -> None:
    """Test GROUP BY with multiple aggregates."""
    t1 = table("orders")
    q = (
        query()
        .select(
            identifier("user_id"),
            count(alias="total_orders"),
            sum_("amount", alias="total_amount"),
        )
        .from_(t1)
        .group_by("user_id")
    )

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'COUNT(*) AS "total_orders"' in sql
    assert 'SUM("amount") AS "total_amount"' in sql
