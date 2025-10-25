"""Domain interfaces for smolql query builder."""

from abc import ABC, abstractmethod


class ISQLNode(ABC):
    """Interface for all SQL expression nodes."""

    @abstractmethod
    def accept(self, visitor: "IVisitor") -> str:
        """Accept a visitor for compilation."""
        pass


class IVisitor(ABC):
    """Interface for SQL dialect visitors."""

    @abstractmethod
    def visit_table(self, table: "ITable") -> str:
        """Visit a table node."""
        pass

    @abstractmethod
    def visit_identifier(self, identifier: "IIdentifier") -> str:
        """Visit an identifier node."""
        pass

    @abstractmethod
    def visit_predicate(self, predicate: "IPredicate") -> str:
        """Visit a predicate node."""
        pass

    @abstractmethod
    def visit_placeholder(self, placeholder: "IPlaceholder") -> str:
        """Visit a placeholder node."""
        pass

    @abstractmethod
    def visit_query(self, query: "IQuery") -> str:
        """Visit a query node."""
        pass

    @abstractmethod
    def visit_join(self, join: "IJoin") -> str:
        """Visit a join node."""
        pass

    @abstractmethod
    def visit_operator(self, operator: "IOperator") -> str:
        """Visit an operator node."""
        pass

    @abstractmethod
    def visit_raw_sql(self, raw_sql: "IRawSQL") -> str:
        """Visit a raw SQL node."""
        pass


class ITable(ISQLNode):
    """Interface for table representation."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get table name."""
        pass

    @property
    @abstractmethod
    def schema(self) -> str | None:
        """Get schema name."""
        pass

    @property
    @abstractmethod
    def alias(self) -> str | None:
        """Get table alias."""
        pass


class IIdentifier(ISQLNode):
    """Interface for column/field identifiers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get identifier name."""
        pass

    @property
    @abstractmethod
    def table(self) -> ITable | None:
        """Get associated table."""
        pass

    @property
    @abstractmethod
    def alias(self) -> str | None:
        """Get identifier alias."""
        pass


class IPredicate(ISQLNode):
    """Interface for WHERE/ON predicates."""

    @property
    @abstractmethod
    def operator(self) -> str:
        """Get operator (=, >, <, etc.)."""
        pass

    @property
    @abstractmethod
    def left(self) -> ISQLNode:
        """Get left operand."""
        pass

    @property
    @abstractmethod
    def right(self) -> ISQLNode:
        """Get right operand."""
        pass


class IPlaceholder(ISQLNode):
    """Interface for parameter placeholders."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get placeholder name."""
        pass


class IJoin(ISQLNode):
    """Interface for JOIN clauses."""

    @property
    @abstractmethod
    def table(self) -> ITable:
        """Get table to join."""
        pass

    @property
    @abstractmethod
    def join_type(self) -> str:
        """Get join type (INNER, LEFT, RIGHT, etc.)."""
        pass

    @property
    @abstractmethod
    def on_condition(self) -> IPredicate | None:
        """Get ON condition."""
        pass


class IQuery(ISQLNode):
    """Interface for SQL queries."""

    @property
    @abstractmethod
    def select_fields(self) -> list[ISQLNode]:
        """Get selected fields."""
        pass

    @property
    @abstractmethod
    def from_table(self) -> ITable | None:
        """Get FROM table."""
        pass

    @property
    @abstractmethod
    def joins(self) -> list[IJoin]:
        """Get JOIN clauses."""
        pass

    @property
    @abstractmethod
    def where_conditions(self) -> list[IPredicate]:
        """Get WHERE conditions."""
        pass

    @property
    @abstractmethod
    def group_by_fields(self) -> list[ISQLNode]:
        """Get GROUP BY fields."""
        pass

    @property
    @abstractmethod
    def having_conditions(self) -> list[IPredicate]:
        """Get HAVING conditions."""
        pass

    @property
    @abstractmethod
    def order_by_fields(self) -> list[tuple[ISQLNode, str]]:
        """Get ORDER BY fields with direction."""
        pass

    @property
    @abstractmethod
    def limit_value(self) -> int | None:
        """Get LIMIT value."""
        pass

    @property
    @abstractmethod
    def offset_value(self) -> int | None:
        """Get OFFSET value."""
        pass


class IOperator(ISQLNode):
    """Interface for SQL operators (COUNT, SUM, etc.)."""

    @property
    @abstractmethod
    def operator_name(self) -> str:
        """Get operator name."""
        pass

    @property
    @abstractmethod
    def arguments(self) -> list[ISQLNode]:
        """Get operator arguments."""
        pass

    @property
    @abstractmethod
    def alias(self) -> str | None:
        """Get operator alias."""
        pass


class IRawSQL(ISQLNode):
    """Interface for raw SQL injection."""

    @property
    @abstractmethod
    def sql(self) -> str:
        """Get raw SQL string."""
        pass
