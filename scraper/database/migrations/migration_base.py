from abc import ABC, abstractmethod

from sqlalchemy.engine import Connection


class BaseMigration(ABC):
    """
    Base contract for an ordered database migration.

    Migration versions must be unique and sortable. Use the project version
    converted to an integer, for example:

        v0.64.14 -> 6414
    """

    version: int
    name: str

    @abstractmethod
    def upgrade(
        self,
        connection: Connection,
    ) -> None:
        """
        Apply the migration using the provided transaction-bound connection.
        """
        raise NotImplementedError
