#!/usr/bin/env bash
# create_sample_git.sh
set -euo pipefail

DEBUG="${DEBUG:-0}"
if [[ "$DEBUG" -eq 1 ]]; then
  PS4='+(${BASH_SOURCE}:${LINENO}): '
  set -x
fi

BASE="${1:-samples/git_samples}"   # 生成先ベース（既定: samples/git_samples）

# 1) 生成先を用意し、絶対パスに正規化
mkdir -p -- "$BASE"
BASE="$(cd "$BASE" && pwd -P)"
echo "[info] BASE=$BASE"

# 既存の同名ディレクトリは掃除（あれば）
rm -rf -- "$BASE"/{git_init,git_add_0,git_commit_0,git_add_1,git_commit_1} 2>/dev/null || true

# 2) 作業用ワークツリー（tmp）
WORK="$(mktemp -d /tmp/git_work.XXXXXX)"
trap 'rm -rf -- "$WORK"' EXIT
echo "[info] WORK=$WORK"
cd "$WORK"
echo "[info] PWD=$PWD"

# 3) シナリオ実行しながら .git をスナップショット
echo "hello" > hello.txt

git -c init.defaultBranch=main init -q
git config user.email "you@example.com"
git config user.name  "Your Name"
cp -r .git "$BASE/git_init"

git add hello.txt
cp -r .git "$BASE/git_add_0"

git commit -q -m "first commit"
cp -r .git "$BASE/git_commit_0"

echo "goodbye" > hello.txt
git add hello.txt
cp -r .git "$BASE/git_add_1"

git commit -q -m "second commit"
cp -r .git "$BASE/git_commit_1"

echo "Done. Snapshots -> $BASE" 