from typing import Final, List, Iterable, Optional, Any
from pymongo import MongoClient

from ..builtins.builtins import KWARGS
from ..trace.Trace import Trace
from ..data.DictList import DictList


_TRACE: Final = Trace("MongoDB", group="Library")

_SYSTEM_DATABASES: Final[List] = ["admin", "config", "local"]


class MongoDB:
    def __init__(self):
        self._client = MongoClient(serverSelectionTimeoutMS=500, connectTimeoutMS=500)

    def databases(self) -> List[str]:
        return [d for d in self._client.list_database_names() if d not in _SYSTEM_DATABASES]

    def collections(self, database: str) -> List[str]:
        return [c for c in self._client[database].list_collection_names()]

    def drop_database(self, database: str) -> None:
        self._client.drop_database(database)

    def drop_collection(self, database: str, collection: str) -> None:
        self._client[database].drop_collection(collection)

    def insert(self, database: str, collection: str, data: Iterable) -> None:
        try:
            self._client[database][collection].insert_many(data)

        except TypeError:  # error: exception TypeError, documents must be a non-empty list
            pass

    def select(
        self,
        database: str,
        collection: str,
        *,
        key: Optional[str] = None,
        value: Optional[Any] = None,
        start: Optional[Any] = None,
        end: Optional[Any] = None,
        count: Optional[int] = None,
    ) -> DictList:
        not (filter := None) and key and (
            filter := (
                {key: KWARGS(**{"$gte": start, "$lte": end})} if value is None else {key: value}
            )
        )
        cursor = self._client[database][collection].find(projection={"_id": False}, filter=filter)
        return DictList(
            cursor
            if not count
            else cursor.skip(
                self._client[database][collection].count_documents(filter if filter else {}) - count
            ),
            name=f"MongoDB.{database}.{collection}"
            + (f".key.{key}" if key else "")
            + (f".value.{value}" if value else "")
            + (f".start.{start}" if value is None and start else "")
            + (f".end.{end}" if value is None and end else "")
            + (f".count.{count}" if count else ""),
        )
