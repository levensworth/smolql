"""Test basic query construction."""

from smolql import identifier, placeholder, query, table


def test_simple_select() -> None:
    """Test simple SELECT query."""
    t1 = table("users")
    q = query().select(identifier("name"), identifier("email")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'SELECT "name", "email"' in sql
    assert 'FROM "users"' in sql


def test_select_with_table_alias() -> None:
    """Test SELECT with table alias."""
    t1 = table("users", alias="u")
    q = (
        query()
        .select(identifier("name", table=t1), identifier("email", table=t1))
        .from_(t1)
    )

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert '"u"."name"' in sql
    assert '"u"."email"' in sql
    assert 'FROM "users" AS "u"' in sql


def test_select_with_schema() -> None:
    """Test SELECT with schema."""
    t1 = table("users", schema="public")
    q = query().select(identifier("name")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'FROM "public"."users"' in sql


def test_select_with_field_alias() -> None:
    """Test SELECT with field alias."""
    t1 = table("users")
    q = query().select(identifier("full_name", alias="name")).from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert '"full_name" AS "name"' in sql


def test_select_wildcard() -> None:
    """Test SELECT with wildcard."""
    t1 = table("users")
    q = query().select("*").from_(t1)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert "SELECT *" in sql


def test_where_clause() -> None:
    """Test WHERE clause."""
    t1 = table("users", alias="u")
    q = query().select("*").from_(t1).where(t1.age > 18)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'WHERE "u"."age" > 18' in sql


def test_where_with_placeholder() -> None:
    """Test WHERE with placeholder."""
    t1 = table("users")
    q = query().select("*").from_(t1).where(t1.col("name") == placeholder("user_name"))

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert '"users"."name" = :user_name' in sql


def test_multiple_where_conditions() -> None:
    """Test multiple WHERE conditions."""
    t1 = table("users", alias="u")
    q = query().select("*").from_(t1).where(t1.age > 18, t1.active == True)  # noqa: E712

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert '"u"."age" > 18' in sql
    assert '"u"."active" = True' in sql
    assert "AND" in sql


def test_combined_predicates() -> None:
    """Test combined predicates with AND/OR."""
    t1 = table("users", alias="u")
    condition = (t1.age > 18) & (t1.active == True)  # noqa: E712
    q = query().select("*").from_(t1).where(condition)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert "(" in sql
    assert "AND" in sql


def test_order_by() -> None:
    """Test ORDER BY clause."""
    t1 = table("users")
    q = query().select("*").from_(t1).order_by(identifier("name"), "ASC")

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert 'ORDER BY "name" ASC' in sql


def test_limit_offset() -> None:
    """Test LIMIT and OFFSET."""
    t1 = table("users")
    q = query().select("*").from_(t1).limit(10).offset(5)

    sql = q.accept(
        __import__(
            "smolql.services.compiler_service", fromlist=["PostgreSQLVisitor"]
        ).PostgreSQLVisitor()
    )
    assert "LIMIT 10" in sql
    assert "OFFSET 5" in sql
