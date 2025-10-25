"""Test JOIN functionality."""

from smolql import query, table


def test_inner_join() -> None:
    """Test INNER JOIN."""
    t1 = table("users", alias="u")
    t2 = table("orders", alias="o")
    q = query().select("*").from_(t1).join(t2, on=t1.id == t2.user_id)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'INNER JOIN "orders" AS "o"' in sql
    assert 'ON "u"."id" = "o"."user_id"' in sql


def test_left_join() -> None:
    """Test LEFT JOIN."""
    t1 = table("users", alias="u")
    t2 = table("orders", alias="o")
    q = query().select("*").from_(t1).left_join(t2, on=t1.id == t2.user_id)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'LEFT JOIN "orders" AS "o"' in sql


def test_right_join() -> None:
    """Test RIGHT JOIN."""
    t1 = table("users", alias="u")
    t2 = table("orders", alias="o")
    q = query().select("*").from_(t1).right_join(t2, on=t1.id == t2.user_id)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'RIGHT JOIN "orders" AS "o"' in sql


def test_multiple_joins() -> None:
    """Test multiple JOINs."""
    t1 = table("users", alias="u")
    t2 = table("orders", alias="o")
    t3 = table("products", alias="p")
    q = (
        query()
        .select("*")
        .from_(t1)
        .join(t2, on=t1.id == t2.user_id)
        .join(t3, on=t2.product_id == t3.id)
    )

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'INNER JOIN "orders" AS "o"' in sql
    assert 'INNER JOIN "products" AS "p"' in sql


def test_join_with_schema() -> None:
    """Test JOIN with schema."""
    t1 = table("users", schema="public", alias="u")
    t2 = table("orders", schema="sales", alias="o")
    q = query().select("*").from_(t1).join(t2, on=t1.id == t2.user_id)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert '"public"."users"' in sql
    assert '"sales"."orders"' in sql
