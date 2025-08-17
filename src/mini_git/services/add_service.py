from mini_git.storage import ObjectStore
from pathlib import Path
from mini_git.types import ObjectType


class AddService:
    def __init__(self, object_store: ObjectStore):
        self.object_store = object_store

    def add_object(self, path: Path) -> str:
        data = path.read_bytes()
        object_id = self.object_store.write(ObjectType.BLOB, data)
        return object_id