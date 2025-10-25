"""Value objects for smolql."""

from enum import Enum


class Dialect(Enum):
    """Supported SQL dialects."""

    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"
