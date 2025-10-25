"""SQL operators and functions."""

from smolql.domain import interfaces
from smolql.domain.entities import Operator, RawSQL, _to_sql_node


def count(
    field: interfaces.ISQLNode | str | None = None, alias: str | None = None
) -> Operator:
    """Create a COUNT operator."""
    if field is None:
        args = [RawSQL(_sql="*")]
    else:
        args = [_to_sql_node(field)]
    return Operator(_operator_name="COUNT", _arguments=args, _alias=alias)


def sum_(field: interfaces.ISQLNode | str, alias: str | None = None) -> Operator:
    """Create a SUM operator."""
    return Operator(
        _operator_name="SUM", _arguments=[_to_sql_node(field)], _alias=alias
    )


def avg(field: interfaces.ISQLNode | str, alias: str | None = None) -> Operator:
    """Create an AVG operator."""
    return Operator(
        _operator_name="AVG", _arguments=[_to_sql_node(field)], _alias=alias
    )


def min_(field: interfaces.ISQLNode | str, alias: str | None = None) -> Operator:
    """Create a MIN operator."""
    return Operator(
        _operator_name="MIN", _arguments=[_to_sql_node(field)], _alias=alias
    )


def max_(field: interfaces.ISQLNode | str, alias: str | None = None) -> Operator:
    """Create a MAX operator."""
    return Operator(
        _operator_name="MAX", _arguments=[_to_sql_node(field)], _alias=alias
    )


def lower(field: interfaces.ISQLNode | str, alias: str | None = None) -> Operator:
    """Create a LOWER operator."""
    return Operator(
        _operator_name="LOWER", _arguments=[_to_sql_node(field)], _alias=alias
    )


def upper(field: interfaces.ISQLNode | str, alias: str | None = None) -> Operator:
    """Create an UPPER operator."""
    return Operator(
        _operator_name="UPPER", _arguments=[_to_sql_node(field)], _alias=alias
    )


def concat(*fields: interfaces.ISQLNode | str, alias: str | None = None) -> Operator:
    """Create a CONCAT operator."""
    args = [_to_sql_node(f) for f in fields]
    return Operator(_operator_name="CONCAT", _arguments=args, _alias=alias)


def coalesce(
    *fields: interfaces.ISQLNode | str | None, alias: str | None = None
) -> Operator:
    """Create a COALESCE operator."""
    args = [_to_sql_node(f) for f in fields]
    return Operator(_operator_name="COALESCE", _arguments=args, _alias=alias)


def cast(
    field: interfaces.ISQLNode | str, type_name: str, alias: str | None = None
) -> Operator:
    """Create a CAST operator."""
    return Operator(
        _operator_name="CAST",
        _arguments=[_to_sql_node(field), RawSQL(_sql=f"AS {type_name}")],
        _alias=alias,
    )


def now(alias: str | None = None) -> Operator:
    """Create a NOW operator."""
    return Operator(_operator_name="NOW", _arguments=[], _alias=alias)


def current_date(alias: str | None = None) -> Operator:
    """Create a CURRENT_DATE operator."""
    return Operator(_operator_name="CURRENT_DATE", _arguments=[], _alias=alias)


def current_timestamp(alias: str | None = None) -> Operator:
    """Create a CURRENT_TIMESTAMP operator."""
    return Operator(_operator_name="CURRENT_TIMESTAMP", _arguments=[], _alias=alias)


def date_trunc(
    precision: str, field: interfaces.ISQLNode | str, alias: str | None = None
) -> Operator:
    """Create a DATE_TRUNC operator."""
    return Operator(
        _operator_name="DATE_TRUNC",
        _arguments=[RawSQL(_sql=f"'{precision}'"), _to_sql_node(field)],
        _alias=alias,
    )


def extract(
    part: str, field: interfaces.ISQLNode | str, alias: str | None = None
) -> Operator:
    """Create an EXTRACT operator."""
    return Operator(
        _operator_name="EXTRACT",
        _arguments=[RawSQL(_sql=f"{part} FROM"), _to_sql_node(field)],
        _alias=alias,
    )


def distinct(field: interfaces.ISQLNode | str, alias: str | None = None) -> Operator:
    """Create a DISTINCT operator."""
    return Operator(
        _operator_name="DISTINCT", _arguments=[_to_sql_node(field)], _alias=alias
    )


def row_number(alias: str | None = None) -> Operator:
    """Create a ROW_NUMBER window function."""
    return Operator(_operator_name="ROW_NUMBER", _arguments=[], _alias=alias)


def rank(alias: str | None = None) -> Operator:
    """Create a RANK window function."""
    return Operator(_operator_name="RANK", _arguments=[], _alias=alias)


def dense_rank(alias: str | None = None) -> Operator:
    """Create a DENSE_RANK window function."""
    return Operator(_operator_name="DENSE_RANK", _arguments=[], _alias=alias)


def lag(
    field: interfaces.ISQLNode | str, offset: int = 1, alias: str | None = None
) -> Operator:
    """Create a LAG window function."""
    return Operator(
        _operator_name="LAG",
        _arguments=[_to_sql_node(field), _to_sql_node(offset)],
        _alias=alias,
    )


def lead(
    field: interfaces.ISQLNode | str, offset: int = 1, alias: str | None = None
) -> Operator:
    """Create a LEAD window function."""
    return Operator(
        _operator_name="LEAD",
        _arguments=[_to_sql_node(field), _to_sql_node(offset)],
        _alias=alias,
    )
