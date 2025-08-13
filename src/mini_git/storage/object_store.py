import hashlib
import zlib
from pathlib import Path
from typing import Tuple
from mini_git.types import ObjectType


class ObjectStore:
    def __init__(self, git_dir: Path) -> None:
        self.object_dir = git_dir / "objects"

    def write(self, type: ObjectType, raw: bytes) -> str:
        header = f"{type.value} {len(raw)}\0".encode()
        data = header + raw
        print(f"add data {data=}")
        object_id = hashlib.sha1(data).hexdigest()
        (self.object_dir / object_id[:2]).mkdir(parents=True, exist_ok=True)
        (self.object_dir / object_id[:2] / object_id[2:]).write_bytes(
            zlib.compress(data, level=1)
        )
        return object_id

    def read(self, oid: str) -> Tuple[str, bytes]:
        data = zlib.decompress((self.object_dir / oid[:2] / oid[2:]).read_bytes())
        i = data.index(b"\0")
        type_len = data[:i].decode()  # "blob 1234"
        type, _ = type_len.split(" ", 1)
        return type, data[i + 1 :]  # (type, raw-bytes)

    def stat(self, oid: str) -> Tuple[str, int]:
        typ, raw = self.read(oid)
        return typ, len(raw)  # cat-file -t / -s 相当
