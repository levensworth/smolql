"""Test the intended user experience from the README."""

from smolql import (
    Dialect,
    compile_to_sql,
    identifier,
    placeholder,
    predicate,
    query,
    table,
)


def test_intended_user_experience() -> None:
    """Test the exact example from the intended user experience."""
    t1 = table("users", schema="public", alias="t")
    t2 = table("groups", schema="public", alias="g")
    q = (
        query()
        .select(identifier("full_name", alias="name", table=t1), identifier("age"))
        .from_(t1)
        .join(t2, on=t1.id == t2.user_id)
        .where(
            predicate(identifier("group_name", table=t2) == placeholder("group_name"))
        )
    )

    sql = compile_to_sql(q, Dialect.POSTGRESQL)

    # Verify key parts of the query
    assert "SELECT" in sql
    assert '"t"."full_name" AS "name"' in sql
    assert '"age"' in sql
    assert 'FROM "public"."users" AS "t"' in sql
    assert 'INNER JOIN "public"."groups" AS "g"' in sql
    assert '"t"."id" = "g"."user_id"' in sql
    assert 'WHERE "g"."group_name" = :group_name' in sql


def test_simpler_experience() -> None:
    """Test a simpler, more natural experience."""
    users = table("users", alias="u")
    groups = table("groups", alias="g")

    q = (
        query()
        .select(users.full_name, users.age, groups.col("name"))
        .from_(users)
        .join(groups, on=users.group_id == groups.id)
        .where(users.active == True)  # noqa: E712
        .order_by(users.full_name, "ASC")
        .limit(10)
    )

    sql = compile_to_sql(q, Dialect.POSTGRESQL)

    assert 'SELECT "u"."full_name", "u"."age", "g"."name"' in sql
    assert 'FROM "users" AS "u"' in sql
    assert 'INNER JOIN "groups" AS "g"' in sql
    assert 'WHERE "u"."active" = True' in sql
    assert 'ORDER BY "u"."full_name" ASC' in sql
    assert "LIMIT 10" in sql


def test_complex_query() -> None:
    """Test a more complex query with multiple features."""
    from smolql import count, sum_

    orders = table("orders", schema="public", alias="o")
    users = table("users", schema="public", alias="u")

    q = (
        query()
        .select(
            users.email,
            count(alias="order_count"),
            sum_(orders.total, alias="total_spent"),
        )
        .from_(orders)
        .join(users, on=orders.user_id == users.id)
        .where(orders.status == "completed")
        .group_by(users.email)
        .having(count() > 1)
        .order_by(sum_(orders.total), "DESC")
        .limit(20)
    )

    sql = compile_to_sql(q, Dialect.POSTGRESQL)

    assert '"u"."email"' in sql
    assert 'COUNT(*) AS "order_count"' in sql
    assert 'SUM("o"."total") AS "total_spent"' in sql
    assert 'WHERE "o"."status" = "completed"' in sql
    assert 'GROUP BY "u"."email"' in sql
    assert "HAVING COUNT(*) > 1" in sql
    assert "ORDER BY" in sql
    assert "LIMIT 20" in sql
