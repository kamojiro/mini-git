from pathlib import Path
from mini_git.models import Object


def test_object(tmp_path: Path):
    hello_text_path = tmp_path / "hello.txt"
    hello_text_path.write_text("hello\n")
    object = Object.from_path(hello_text_path)
    assert object.git_data == b"blob 6\x00hello\n"
    compressed_data = object.get_compressed_data()
    assert compressed_data == b"x\x01K\xca\xc9OR0c\xc8H\xcd\xc9\xc9\xe7\x02\x00\x1d\xc5\x04\x14"  # fmt: skip  # noqa: E501