import json
import os
from pathlib import Path
from typing import Iterable
from mini_git.models import IndexEntry


class IndexStore:
    def __init__(self, git_dir: Path, filename: str = "index.json") -> None:
        self.git_dir = git_dir
        self.index_path = git_dir / filename
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

    # --- 読み書き（原子的更新） ---
    def _load(self) -> dict[str, dict]:
        if not self.index_path.exists():
            return {}
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def _save(self, data: dict[str, dict]) -> None:
        tmp = self.index_path.with_suffix(self.index_path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.index_path)  # atomic

    # --- パブリックAPI ---
    def add_or_update(self, e: IndexEntry) -> None:
        data = self._load()
        data[str(e.path)] = {"mode": e.mode, "oid": e.oid}
        self._save(data)

    def remove(self, path: str) -> None:
        data = self._load()
        if path in data:
            del data[path]
            self._save(data)

    def clear(self) -> None:
        self._save({})

    def all(self) -> Iterable[IndexEntry]:
        data = self._load()
        for p, v in data.items():
            yield IndexEntry(path=Path(p), mode=int(v["mode"]), oid=v["oid"])
