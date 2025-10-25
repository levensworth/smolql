"""Test SQL operators and functions."""

from smolql import (
    avg,
    cast,
    coalesce,
    concat,
    count,
    current_date,
    lower,
    max_,
    min_,
    now,
    query,
    sum_,
    table,
    upper,
)


def test_count_operator() -> None:
    """Test COUNT operator."""
    t1 = table("users")
    q = query().select(count(alias="total")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'COUNT(*) AS "total"' in sql


def test_count_with_field() -> None:
    """Test COUNT with field."""
    t1 = table("users")
    q = query().select(count("id", alias="user_count")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'COUNT("id") AS "user_count"' in sql


def test_sum_operator() -> None:
    """Test SUM operator."""
    t1 = table("orders")
    q = query().select(sum_("amount", alias="total_amount")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'SUM("amount") AS "total_amount"' in sql


def test_avg_operator() -> None:
    """Test AVG operator."""
    t1 = table("orders")
    q = query().select(avg("amount", alias="avg_amount")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'AVG("amount") AS "avg_amount"' in sql


def test_min_max_operators() -> None:
    """Test MIN and MAX operators."""
    t1 = table("orders")
    q = (
        query()
        .select(min_("amount", alias="min_amt"), max_("amount", alias="max_amt"))
        .from_(t1)
    )

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'MIN("amount") AS "min_amt"' in sql
    assert 'MAX("amount") AS "max_amt"' in sql


def test_lower_upper_operators() -> None:
    """Test LOWER and UPPER operators."""
    t1 = table("users")
    q = query().select(lower("name"), upper("email")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'LOWER("name")' in sql
    assert 'UPPER("email")' in sql


def test_concat_operator() -> None:
    """Test CONCAT operator."""
    t1 = table("users")
    q = query().select(concat("first_name", "last_name", alias="full_name")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'CONCAT("first_name", "last_name") AS "full_name"' in sql


def test_coalesce_operator() -> None:
    """Test COALESCE operator."""
    t1 = table("users")
    q = (
        query()
        .select(coalesce("nickname", "first_name", alias="display_name"))
        .from_(t1)
    )

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'COALESCE("nickname", "first_name") AS "display_name"' in sql


def test_cast_operator() -> None:
    """Test CAST operator."""
    t1 = table("users")
    q = query().select(cast("age", "VARCHAR")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'CAST("age", AS VARCHAR)' in sql


def test_now_operator() -> None:
    """Test NOW operator."""
    t1 = table("users")
    q = query().select(now(alias="current_time")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'NOW() AS "current_time"' in sql


def test_current_date_operator() -> None:
    """Test CURRENT_DATE operator."""
    t1 = table("users")
    q = query().select(current_date()).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert "CURRENT_DATE()" in sql


def test_algebraic_operators() -> None:
    """Test algebraic operators."""
    t1 = table("orders", alias="o")
    q = query().select(t1.price * t1.quantity).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert '"o"."price"' in sql
    assert '"o"."quantity"' in sql
    assert "*" in sql
