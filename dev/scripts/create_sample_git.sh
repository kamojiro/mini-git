#!/usr/bin/env bash
set -e

BASE="${1:-samples}"                 # 生成先（既定: samples）
mkdir -p "$BASE"
# 既存があれば上書きしやすいように消す
rm -rf "$BASE"/{git_init,git_add_0,git_commit_0,git_add_1,git_commit_1} 2>/dev/null || true

# 作業用ワークツリー（/tmp）
WORK="$(mktemp -d /tmp/git_work.XXXXXX)"
cd "$WORK"

# 1) ファイル作成
echo "hello" > hello.txt

# 2) git init -> samples/git_init
git -c init.defaultBranch=main init -q
git config user.email "you@example.com"
git config user.name  "Your Name"
cp -r .git "$BASE/git_init"

# 3) git add hello.txt -> samples/git_add_0
git add hello.txt
cp -r .git "$BASE/git_add_0"

# 4) git commit "first commit" -> samples/git_commit_0
git commit -q -m "first commit"
cp -r .git "$BASE/git_commit_0"

# 5) 変更して add -> samples/git_add_1
echo "goodbye" > hello.txt
git add hello.txt
cp -r .git "$BASE/git_add_1"

# 6) 2回目の commit -> samples/git_commit_1
git commit -q -m "second commit"
cp -r .git "$BASE/git_commit_1"

# お片付け
cd /
rm -rf "$WORK"

echo "Done. Snapshots are under: $BASE"