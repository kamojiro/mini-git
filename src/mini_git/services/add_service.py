from mini_git.storage import ObjectStore
from pathlib import Path
from mini_git.types import ObjectType


class AddService:
    def __init__(self, object_store: ObjectStore):
        self.object_store = object_store

    def add_object(self, path: Path):
        data = path.read_bytes()
        self.object_store.write(ObjectType.BLOB, data)
