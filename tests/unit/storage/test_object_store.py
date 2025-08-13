# tests/test_object_store.py
from pathlib import Path
import pytest

from mini_git.storage.object_store import ObjectStore
from mini_git.types import ObjectType

# --- 期待値（zlib level=1 前提）------------------------------------------
BLOB_RAW = b"hello\n"
BLOB_HEADER_PLUS_RAW = b"blob 6\x00hello\n"
BLOB_COMPRESSED_L1 = b"x\x01K\xca\xc9OR0c\xc8H\xcd\xc9\xc9\xe7\x02\x00\x1d\xc5\x04\x14"
BLOB_OID = "ce013625030ba8dba906f756967f9e9ca394464a"
# -------------------------------------------------------------------------


def test_write_blob_creates_object_and_returns_oid(tmp_path: Path):
    git_dir = tmp_path / ".git"
    store = ObjectStore(git_dir)

    oid = store.write(ObjectType.BLOB, BLOB_RAW)
    assert oid == BLOB_OID

    obj_path = git_dir / "objects" / oid[:2] / oid[2:]
    assert obj_path.is_file(), "loose object が作成されていること"
    # 圧縮済みバイト列の厳密一致（zlib level=1 を前提）
    assert obj_path.read_bytes() == BLOB_COMPRESSED_L1


def test_read_returns_type_and_raw(tmp_path: Path):
    store = ObjectStore(tmp_path / ".git")
    # 事前に1度書き込む
    assert store.write(ObjectType.BLOB, BLOB_RAW) == BLOB_OID

    typ, raw = store.read(BLOB_OID)
    assert typ == "blob"
    assert raw == BLOB_RAW


def test_stat_returns_type_and_size(tmp_path: Path):
    store = ObjectStore(tmp_path / ".git")
    store.write(ObjectType.BLOB, BLOB_RAW)

    typ, size = store.stat(BLOB_OID)
    assert typ == "blob"
    assert size == len(BLOB_RAW)


def test_same_content_produces_same_oid(tmp_path: Path):
    store = ObjectStore(tmp_path / ".git")
    a = store.write(ObjectType.BLOB, BLOB_RAW)
    b = store.write(ObjectType.BLOB, BLOB_RAW)
    assert a == b, "同一内容は同一OID（コンテンツアドレス化）になること"


def test_read_missing_object_raises(tmp_path: Path):
    store = ObjectStore(tmp_path / ".git")
    with pytest.raises(FileNotFoundError):
        store.read("0" * 40)
