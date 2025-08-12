from pydantic import BaseModel, Field
from pathlib import Path
import hashlib
import zlib


class Object(BaseModel):
    git_data: bytes = Field(..., description="The content of the object")

    @classmethod
    def from_path(cls, path: Path, **kwargs) -> "Object":
        data = path.read_bytes()
        header = f"blob {len(data)}\0".encode("utf-8")
        git_data = header + data
        return cls(git_data=git_data, **kwargs)

    @property
    def object_id(self) -> str:
        return hashlib.sha1(self.git_data).hexdigest()

    @property
    def object_directory(self) -> Path:
        return Path(self.object_id[:2])

    @property
    def object_filename(self) -> Path:
        return Path(self.object_id[2:])

    @property
    def object_path(self) -> Path:
        return self.object_directory / self.object_filename

    def get_compressed_data(self) -> bytes:
        return zlib.compress(self.git_data)
