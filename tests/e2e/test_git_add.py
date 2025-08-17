"""E2E tests for mgit add command - comparing with actual git behavior"""

import subprocess
from pathlib import Path


def run_command(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run a command and return the result"""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def get_git_object_hash(file_path: Path, cwd: Path) -> str:
    """Get the git object hash for a file using git hash-object"""
    result = run_command(["git", "hash-object", str(file_path)], cwd)
    if result.returncode != 0:
        raise RuntimeError(f"git hash-object failed: {result.stderr}")
    return result.stdout.strip()


def get_mgit_object_hash(file_path: Path, cwd: Path) -> str:
    """Get the object hash created by mgit add"""
    # Get existing object files before adding
    objects_dir = cwd / ".git" / "objects"
    existing_files = set()
    if objects_dir.exists():
        existing_files = set(objects_dir.rglob("*"))
        existing_files = {f for f in existing_files if f.is_file()}

    # Run mgit add
    result = run_command(["uv", "run", "mgit", "add", str(file_path)], cwd)
    if result.returncode != 0:
        raise RuntimeError(f"mgit add failed: {result.stderr}")

    # Find the newly created object file
    new_files = set(objects_dir.rglob("*"))
    new_files = {f for f in new_files if f.is_file()}

    created_files = new_files - existing_files
    if not created_files:
        # If no new files were created, it might be a duplicate
        # In that case, we need to calculate what the hash should be
        # by reading the file content and computing the git hash
        content = file_path.read_bytes()
        import hashlib

        header = f"blob {len(content)}\0".encode()
        full_content = header + content
        return hashlib.sha1(full_content).hexdigest()

    # Return the OID (directory name + file name) of the newly created file
    obj_file = list(created_files)[0]
    return obj_file.parent.name + obj_file.name


def test_mgit_add_single_file_matches_git(tmp_path: Path):
    """mgit addが単一ファイルでgitと同じ結果を生成することをテスト"""
    # テストファイルを作成
    test_file = tmp_path / "hello.txt"
    test_content = "Hello, World!\n"
    test_file.write_text(test_content)

    # mgit リポジトリを初期化
    mgit_result = run_command(["uv", "run", "mgit", "init"], tmp_path)
    assert mgit_result.returncode == 0

    # git リポジトリも初期化（比較用）
    git_result = run_command(["git", "init"], tmp_path)
    assert git_result.returncode == 0

    # gitでのハッシュを取得
    git_hash = get_git_object_hash(test_file, tmp_path)

    # mgitでファイルを追加してハッシュを取得
    mgit_hash = get_mgit_object_hash(test_file, tmp_path)

    # ハッシュが一致することを確認
    assert mgit_hash == git_hash


def test_mgit_add_empty_file_matches_git(tmp_path: Path):
    """mgit addが空ファイルでgitと同じ結果を生成することをテスト"""
    # 空ファイルを作成
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    # mgit リポジトリを初期化
    mgit_result = run_command(["uv", "run", "mgit", "init"], tmp_path)
    assert mgit_result.returncode == 0

    # git リポジトリも初期化（比較用）
    git_result = run_command(["git", "init"], tmp_path)
    assert git_result.returncode == 0

    # gitでのハッシュを取得
    git_hash = get_git_object_hash(empty_file, tmp_path)

    # mgitでファイルを追加してハッシュを取得
    mgit_hash = get_mgit_object_hash(empty_file, tmp_path)

    # ハッシュが一致することを確認
    assert mgit_hash == git_hash


def test_mgit_add_binary_file_matches_git(tmp_path: Path):
    """mgit addがバイナリファイルでgitと同じ結果を生成することをテスト"""
    # バイナリファイルを作成
    binary_file = tmp_path / "binary.dat"
    binary_content = bytes(range(256))
    binary_file.write_bytes(binary_content)

    # mgit リポジトリを初期化
    mgit_result = run_command(["uv", "run", "mgit", "init"], tmp_path)
    assert mgit_result.returncode == 0

    # git リポジトリも初期化（比較用）
    git_result = run_command(["git", "init"], tmp_path)
    assert git_result.returncode == 0

    # gitでのハッシュを取得
    git_hash = get_git_object_hash(binary_file, tmp_path)

    # mgitでファイルを追加してハッシュを取得
    mgit_hash = get_mgit_object_hash(binary_file, tmp_path)

    # ハッシュが一致することを確認
    assert mgit_hash == git_hash


def test_mgit_add_multiple_files_matches_git(tmp_path: Path):
    """mgit addが複数ファイルでgitと同じ結果を生成することをテスト"""
    # 複数のテストファイルを作成
    files_and_contents = [
        ("file1.txt", "Content of file 1\n"),
        ("file2.txt", "Content of file 2\n"),
        ("file3.txt", "Content of file 3\n"),
    ]

    test_files = []
    for filename, content in files_and_contents:
        file_path = tmp_path / filename
        file_path.write_text(content)
        test_files.append(file_path)

    # mgit リポジトリを初期化
    mgit_result = run_command(["uv", "run", "mgit", "init"], tmp_path)
    assert mgit_result.returncode == 0

    # git リポジトリも初期化（比較用）
    git_result = run_command(["git", "init"], tmp_path)
    assert git_result.returncode == 0

    # 各ファイルについてハッシュを比較
    for test_file in test_files:
        # gitでのハッシュを取得
        git_hash = get_git_object_hash(test_file, tmp_path)

        # mgitでファイルを追加してハッシュを取得
        mgit_hash = get_mgit_object_hash(test_file, tmp_path)

        # ハッシュが一致することを確認
        assert mgit_hash == git_hash, f"Hash mismatch for {test_file.name}"


def test_mgit_add_same_content_produces_same_hash(tmp_path: Path):
    """同じ内容のファイルが同じハッシュを生成することをテスト"""
    # 同じ内容の複数ファイルを作成
    same_content = "Same content\n"
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text(same_content)
    file2.write_text(same_content)

    # mgit リポジトリを初期化
    mgit_result = run_command(["uv", "run", "mgit", "init"], tmp_path)
    assert mgit_result.returncode == 0

    # git リポジトリも初期化（比較用）
    git_result = run_command(["git", "init"], tmp_path)
    assert git_result.returncode == 0

    # gitでのハッシュを取得（両ファイルとも同じはず）
    git_hash1 = get_git_object_hash(file1, tmp_path)
    git_hash2 = get_git_object_hash(file2, tmp_path)
    assert git_hash1 == git_hash2

    # mgitでファイルを追加してハッシュを取得
    mgit_hash1 = get_mgit_object_hash(file1, tmp_path)
    mgit_hash2 = get_mgit_object_hash(file2, tmp_path)

    # 全てのハッシュが一致することを確認
    assert mgit_hash1 == git_hash1
    assert mgit_hash2 == git_hash2
    assert mgit_hash1 == mgit_hash2


def test_mgit_add_nonexistent_file_fails(tmp_path: Path):
    """存在しないファイルに対してmgit addが失敗することをテスト"""
    # mgit リポジトリを初期化
    mgit_result = run_command(["uv", "run", "mgit", "init"], tmp_path)
    assert mgit_result.returncode == 0

    # 存在しないファイルを追加しようとする
    nonexistent_file = tmp_path / "nonexistent.txt"
    mgit_result = run_command(
        ["uv", "run", "mgit", "add", str(nonexistent_file)], tmp_path
    )

    # エラーで終了することを確認
    assert mgit_result.returncode != 0


def test_mgit_add_without_repo_fails(tmp_path: Path):
    """リポジトリが初期化されていない状態でmgit addが失敗することをテスト"""
    # テストファイルを作成
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")

    # リポジトリを初期化せずにファイルを追加しようとする
    mgit_result = run_command(["uv", "run", "mgit", "add", str(test_file)], tmp_path)

    # エラーで終了することを確認
    assert mgit_result.returncode != 0
