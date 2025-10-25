from smolql.domain import interfaces


class SQLiteVisitor(interfaces.IVisitor):
    """Visitor for SQLite dialect."""

    def visit_table(self, table: interfaces.ITable) -> str:
        """Visit a table node."""
        # SQLite doesn't support schemas in the same way
        # Access private attributes to avoid __getattr__ interception
        name = table._name if hasattr(table, "_name") else table.name  # type: ignore
        alias_val = table._alias if hasattr(table, "_alias") else table.alias  # type: ignore

        result = f'"{name}"'
        if alias_val:
            result += f' AS "{alias_val}"'
        return result

    def visit_identifier(self, identifier: interfaces.IIdentifier) -> str:
        """Visit an identifier node."""
        parts = []
        if identifier.table:
            alias_val = (
                identifier.table._alias
                if hasattr(identifier.table, "_alias")
                else identifier.table.alias
            )  # type: ignore
            name = (
                identifier.table._name
                if hasattr(identifier.table, "_name")
                else identifier.table.name
            )  # type: ignore
            table_ref = alias_val or name
            parts.append(f'"{table_ref}"')

        ident_name = (
            identifier._name if hasattr(identifier, "_name") else identifier.name
        )  # type: ignore
        parts.append(f'"{ident_name}"')
        result = ".".join(parts)

        ident_alias = (
            identifier._alias if hasattr(identifier, "_alias") else identifier.alias
        )  # type: ignore
        if ident_alias:
            result += f' AS "{ident_alias}"'
        return result

    def visit_predicate(self, predicate: interfaces.IPredicate) -> str:
        """Visit a predicate node."""
        operator = predicate.operator.upper()

        # Handle logical operators
        if operator in ("AND", "OR"):
            left = predicate.left.accept(self)
            right = predicate.right.accept(self)
            return f"({left} {operator} {right})"

        # Handle comparison operators
        left = predicate.left.accept(self)
        right = predicate.right.accept(self)
        return f"{left} {operator} {right}"

    def visit_placeholder(self, placeholder: interfaces.IPlaceholder) -> str:
        """Visit a placeholder node."""
        # SQLite uses ? or :name for placeholders
        return f":{placeholder.name}"

    def visit_query(self, query: interfaces.IQuery) -> str:
        """Visit a query node."""
        parts = []

        # SELECT clause
        if query.select_fields:
            select_items = [field.accept(self) for field in query.select_fields]
            parts.append(f"SELECT {', '.join(select_items)}")
        else:
            parts.append("SELECT *")

        # FROM clause
        if query.from_table:
            parts.append(f"FROM {query.from_table.accept(self)}")

        # JOIN clauses
        for join in query.joins:
            parts.append(join.accept(self))

        # WHERE clause
        if query.where_conditions:
            conditions = [cond.accept(self) for cond in query.where_conditions]
            parts.append(f"WHERE {' AND '.join(conditions)}")

        # GROUP BY clause
        if query.group_by_fields:
            group_items = [field.accept(self) for field in query.group_by_fields]
            parts.append(f"GROUP BY {', '.join(group_items)}")

        # HAVING clause
        if query.having_conditions:
            conditions = [cond.accept(self) for cond in query.having_conditions]
            parts.append(f"HAVING {' AND '.join(conditions)}")

        # ORDER BY clause
        if query.order_by_fields:
            order_items = [
                f"{field.accept(self)} {direction}"
                for field, direction in query.order_by_fields
            ]
            parts.append(f"ORDER BY {', '.join(order_items)}")

        # LIMIT clause
        if query.limit_value is not None:
            parts.append(f"LIMIT {query.limit_value}")

        # OFFSET clause
        if query.offset_value is not None:
            parts.append(f"OFFSET {query.offset_value}")

        return " ".join(parts)

    def visit_join(self, join: interfaces.IJoin) -> str:
        """Visit a join node."""
        join_type = join.join_type.upper()
        result = f"{join_type} JOIN {join.table.accept(self)}"
        if join.on_condition:
            result += f" ON {join.on_condition.accept(self)}"
        return result

    def visit_operator(self, operator: interfaces.IOperator) -> str:
        """Visit an operator node."""
        op_name = operator.operator_name.upper()

        # Handle algebraic operators
        if op_name in ("+", "-", "*", "/", "%"):
            args = [arg.accept(self) for arg in operator.arguments]
            result = f"({' {} '.format(op_name).join(args)})"
        # Handle function operators
        else:
            args = [arg.accept(self) for arg in operator.arguments]
            result = f"{op_name}({', '.join(args)})"

        if operator.alias:
            result += f' AS "{operator.alias}"'
        return result

    def visit_raw_sql(self, raw_sql: interfaces.IRawSQL) -> str:
        """Visit a raw SQL node."""
        return raw_sql.sql
