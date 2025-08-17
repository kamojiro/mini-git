from pydantic import BaseModel, ConfigDict
from pathlib import Path


class IndexEntry(BaseModel):
    path: Path
    mode: int
    oid: str

    model_config = ConfigDict(
        frozen=True,
    )
