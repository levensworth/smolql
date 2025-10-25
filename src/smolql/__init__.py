"""smolql - A micro SQL statement builder library."""

from smolql.api import (
    compile_to_sql,
    identifier,
    placeholder,
    predicate,
    query,
    raw,
    table,
)
from smolql.domain.value_objects import Dialect
from smolql.operators import (
    avg,
    cast,
    coalesce,
    concat,
    count,
    current_date,
    current_timestamp,
    date_trunc,
    dense_rank,
    distinct,
    extract,
    lag,
    lead,
    lower,
    max_,
    min_,
    now,
    rank,
    row_number,
    sum_,
    upper,
)

__version__ = "0.1.0"

__all__ = [
    # API functions
    "table",
    "identifier",
    "placeholder",
    "predicate",
    "query",
    "raw",
    "compile_to_sql",
    # Value objects
    "Dialect",
    # Operators
    "count",
    "sum_",
    "avg",
    "min_",
    "max_",
    "lower",
    "upper",
    "concat",
    "coalesce",
    "cast",
    "now",
    "current_date",
    "current_timestamp",
    "date_trunc",
    "extract",
    "distinct",
    "row_number",
    "rank",
    "dense_rank",
    "lag",
    "lead",
]
