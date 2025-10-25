"""Domain entities for smolql query builder."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from smolql.domain.interfaces import IVisitor

from smolql.domain import interfaces


@dataclass(frozen=True)
class Table(interfaces.ITable):
    """Represents a database table."""

    _name: str
    _schema: str | None = None
    _alias: str | None = None

    @property
    def name(self) -> str:
        """Get table name."""
        return self._name

    @property
    def schema(self) -> str | None:
        """Get schema name."""
        return self._schema

    @property
    def alias(self) -> str | None:
        """Get table alias."""
        return self._alias

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        return visitor.visit_table(self)

    def __getattr__(self, name: str) -> "Identifier":
        """Allow accessing columns as attributes (e.g., table.column_name)."""
        if name.startswith("_"):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )
        return Identifier(_name=name, _table=self, _alias=None)

    def col(self, name: str) -> "Identifier":
        """Explicitly access a column by name (useful for columns named 'name', 'schema', or 'alias')."""
        return Identifier(_name=name, _table=self, _alias=None)


@dataclass(frozen=True)
class Identifier(interfaces.IIdentifier):
    """Represents a column or field identifier."""

    _name: str
    _table: interfaces.ITable | None = None
    _alias: str | None = None

    @property
    def name(self) -> str:
        """Get identifier name."""
        return self._name

    @property
    def table(self) -> interfaces.ITable | None:
        """Get associated table."""
        return self._table

    @property
    def alias(self) -> str | None:
        """Get identifier alias."""
        return self._alias

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        return visitor.visit_identifier(self)

    def __eq__(self, other: Any) -> "Predicate":  # type: ignore[override]
        """Create an equality predicate."""
        return Predicate(_operator="=", _left=self, _right=_to_sql_node(other))

    def __ne__(self, other: Any) -> "Predicate":  # type: ignore[override]
        """Create an inequality predicate."""
        return Predicate(_operator="!=", _left=self, _right=_to_sql_node(other))

    def __lt__(self, other: Any) -> "Predicate":
        """Create a less than predicate."""
        return Predicate(_operator="<", _left=self, _right=_to_sql_node(other))

    def __le__(self, other: Any) -> "Predicate":
        """Create a less than or equal predicate."""
        return Predicate(_operator="<=", _left=self, _right=_to_sql_node(other))

    def __gt__(self, other: Any) -> "Predicate":
        """Create a greater than predicate."""
        return Predicate(_operator=">", _left=self, _right=_to_sql_node(other))

    def __ge__(self, other: Any) -> "Predicate":
        """Create a greater than or equal predicate."""
        return Predicate(_operator=">=", _left=self, _right=_to_sql_node(other))

    def __add__(self, other: Any) -> "Operator":
        """Create an addition operator."""
        return Operator(
            _operator_name="+", _arguments=[self, _to_sql_node(other)], _alias=None
        )

    def __sub__(self, other: Any) -> "Operator":
        """Create a subtraction operator."""
        return Operator(
            _operator_name="-", _arguments=[self, _to_sql_node(other)], _alias=None
        )

    def __mul__(self, other: Any) -> "Operator":
        """Create a multiplication operator."""
        return Operator(
            _operator_name="*", _arguments=[self, _to_sql_node(other)], _alias=None
        )

    def __truediv__(self, other: Any) -> "Operator":
        """Create a division operator."""
        return Operator(
            _operator_name="/", _arguments=[self, _to_sql_node(other)], _alias=None
        )


@dataclass(frozen=True)
class Predicate(interfaces.IPredicate):
    """Represents a predicate (condition)."""

    _operator: str
    _left: interfaces.ISQLNode
    _right: interfaces.ISQLNode

    @property
    def operator(self) -> str:
        """Get operator."""
        return self._operator

    @property
    def left(self) -> interfaces.ISQLNode:
        """Get left operand."""
        return self._left

    @property
    def right(self) -> interfaces.ISQLNode:
        """Get right operand."""
        return self._right

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        return visitor.visit_predicate(self)

    def __and__(self, other: "Predicate") -> "Predicate":
        """Combine predicates with AND."""
        return Predicate(_operator="AND", _left=self, _right=other)

    def __or__(self, other: "Predicate") -> "Predicate":
        """Combine predicates with OR."""
        return Predicate(_operator="OR", _left=self, _right=other)


@dataclass(frozen=True)
class Placeholder(interfaces.IPlaceholder):
    """Represents a parameter placeholder."""

    _name: str

    @property
    def name(self) -> str:
        """Get placeholder name."""
        return self._name

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        return visitor.visit_placeholder(self)


@dataclass(frozen=True)
class Join(interfaces.IJoin):
    """Represents a JOIN clause."""

    _table: interfaces.ITable
    _join_type: str
    _on_condition: interfaces.IPredicate | None

    @property
    def table(self) -> interfaces.ITable:
        """Get table to join."""
        return self._table

    @property
    def join_type(self) -> str:
        """Get join type."""
        return self._join_type

    @property
    def on_condition(self) -> interfaces.IPredicate | None:
        """Get ON condition."""
        return self._on_condition

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        return visitor.visit_join(self)


@dataclass
class Query(interfaces.IQuery):
    """Represents a SQL query."""

    _select_fields: list[interfaces.ISQLNode]
    _from_table: interfaces.ITable | None = None
    _joins: list[interfaces.IJoin] | None = None
    _where_conditions: list[interfaces.IPredicate] | None = None
    _group_by_fields: list[interfaces.ISQLNode] | None = None
    _having_conditions: list[interfaces.IPredicate] | None = None
    _order_by_fields: list[tuple[interfaces.ISQLNode, str]] | None = None
    _limit_value: int | None = None
    _offset_value: int | None = None

    @property
    def select_fields(self) -> list[interfaces.ISQLNode]:
        """Get selected fields."""
        return self._select_fields

    @property
    def from_table(self) -> interfaces.ITable | None:
        """Get FROM table."""
        return self._from_table

    @property
    def joins(self) -> list[interfaces.IJoin]:
        """Get JOIN clauses."""
        return self._joins or []

    @property
    def where_conditions(self) -> list[interfaces.IPredicate]:
        """Get WHERE conditions."""
        return self._where_conditions or []

    @property
    def group_by_fields(self) -> list[interfaces.ISQLNode]:
        """Get GROUP BY fields."""
        return self._group_by_fields or []

    @property
    def having_conditions(self) -> list[interfaces.IPredicate]:
        """Get HAVING conditions."""
        return self._having_conditions or []

    @property
    def order_by_fields(self) -> list[tuple[interfaces.ISQLNode, str]]:
        """Get ORDER BY fields."""
        return self._order_by_fields or []

    @property
    def limit_value(self) -> int | None:
        """Get LIMIT value."""
        return self._limit_value

    @property
    def offset_value(self) -> int | None:
        """Get OFFSET value."""
        return self._offset_value

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        return visitor.visit_query(self)

    def select(self, *fields: interfaces.ISQLNode | str) -> "Query":
        """Add SELECT fields."""
        converted_fields = [_to_sql_node(f) for f in fields]
        self._select_fields.extend(converted_fields)
        return self

    def from_(self, table: interfaces.ITable) -> "Query":
        """Set FROM table."""
        self._from_table = table
        return self

    def join(
        self,
        table: interfaces.ITable,
        on: interfaces.IPredicate | None = None,
        join_type: str = "INNER",
    ) -> "Query":
        """Add a JOIN clause."""
        if self._joins is None:
            self._joins = []
        self._joins.append(Join(_table=table, _join_type=join_type, _on_condition=on))
        return self

    def left_join(
        self, table: interfaces.ITable, on: interfaces.IPredicate | None = None
    ) -> "Query":
        """Add a LEFT JOIN clause."""
        return self.join(table, on, "LEFT")

    def right_join(
        self, table: interfaces.ITable, on: interfaces.IPredicate | None = None
    ) -> "Query":
        """Add a RIGHT JOIN clause."""
        return self.join(table, on, "RIGHT")

    def where(self, *conditions: interfaces.IPredicate) -> "Query":
        """Add WHERE conditions."""
        if self._where_conditions is None:
            self._where_conditions = []
        self._where_conditions.extend(conditions)
        return self

    def group_by(self, *fields: interfaces.ISQLNode | str) -> "Query":
        """Add GROUP BY fields."""
        if self._group_by_fields is None:
            self._group_by_fields = []
        converted_fields = [_to_sql_node(f) for f in fields]
        self._group_by_fields.extend(converted_fields)
        return self

    def having(self, *conditions: interfaces.IPredicate) -> "Query":
        """Add HAVING conditions."""
        if self._having_conditions is None:
            self._having_conditions = []
        self._having_conditions.extend(conditions)
        return self

    def order_by(
        self, field: interfaces.ISQLNode | str, direction: str = "ASC"
    ) -> "Query":
        """Add ORDER BY field."""
        if self._order_by_fields is None:
            self._order_by_fields = []
        converted_field = _to_sql_node(field)
        self._order_by_fields.append((converted_field, direction))
        return self

    def limit(self, value: int) -> "Query":
        """Set LIMIT value."""
        self._limit_value = value
        return self

    def offset(self, value: int) -> "Query":
        """Set OFFSET value."""
        self._offset_value = value
        return self


@dataclass(frozen=True)
class Operator(interfaces.IOperator):
    """Represents a SQL operator."""

    _operator_name: str
    _arguments: list[interfaces.ISQLNode]
    _alias: str | None = None

    @property
    def operator_name(self) -> str:
        """Get operator name."""
        return self._operator_name

    @property
    def arguments(self) -> list[interfaces.ISQLNode]:
        """Get operator arguments."""
        return self._arguments

    @property
    def alias(self) -> str | None:
        """Get operator alias."""
        return self._alias

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        return visitor.visit_operator(self)

    def __eq__(self, other: Any) -> "Predicate":  # type: ignore[override]
        """Create an equality predicate."""
        return Predicate(_operator="=", _left=self, _right=_to_sql_node(other))

    def __ne__(self, other: Any) -> "Predicate":  # type: ignore[override]
        """Create an inequality predicate."""
        return Predicate(_operator="!=", _left=self, _right=_to_sql_node(other))

    def __lt__(self, other: Any) -> "Predicate":
        """Create a less than predicate."""
        return Predicate(_operator="<", _left=self, _right=_to_sql_node(other))

    def __le__(self, other: Any) -> "Predicate":
        """Create a less than or equal predicate."""
        return Predicate(_operator="<=", _left=self, _right=_to_sql_node(other))

    def __gt__(self, other: Any) -> "Predicate":
        """Create a greater than predicate."""
        return Predicate(_operator=">", _left=self, _right=_to_sql_node(other))

    def __ge__(self, other: Any) -> "Predicate":
        """Create a greater than or equal predicate."""
        return Predicate(_operator=">=", _left=self, _right=_to_sql_node(other))


@dataclass(frozen=True)
class RawSQL(interfaces.IRawSQL):
    """Represents raw SQL for direct injection."""

    _sql: str

    @property
    def sql(self) -> str:
        """Get raw SQL string."""
        return self._sql

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        return visitor.visit_raw_sql(self)


@dataclass(frozen=True)
class Literal(interfaces.ISQLNode):
    """Represents a literal value."""

    _value: Any

    @property
    def value(self) -> Any:
        """Get literal value."""
        return self._value

    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        # Literals are handled inline, format based on type
        if isinstance(self._value, str):
            return f"'{self._value}'"
        elif self._value is None:
            return "NULL"
        else:
            return str(self._value)


def _to_sql_node(value: Any) -> interfaces.ISQLNode:
    """Convert a value to a SQL node."""
    if isinstance(value, interfaces.ISQLNode):
        return value
    elif isinstance(value, str):
        # Check if it's a wildcard or identifier
        if value == "*":
            return RawSQL(_sql="*")
        return Identifier(_name=value)
    else:
        return Literal(_value=value)
