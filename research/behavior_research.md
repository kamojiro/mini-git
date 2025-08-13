# Research of Behavior

## samples

```bash
echo "hello" > hello.txt
git init # samples/git_init
git add hello.txt # samples/git_add_0
git commit "first commit" # samples/git_commit_0
echo "goodbye" > hello.txt
git add hello.txt # samples/git_add_1
git commit "second commit" # samples/git_commit_1
```

```bash
$ diff <(tree -a git_add_0) <(tree -a git_commit_0)
1c1,2
< git_add_0
---
> git_commit_0
> ├── COMMIT_EDITMSG
22a24,28
> ├── logs
> │   ├── HEAD
> │   └── refs
> │       └── heads
> │           └── main
23a30,33
> │   ├── 82
> │   │   └── ea1960dc12cc9dd344e55ba334e4af48570327
> │   ├── aa
> │   │   └── a96ced2d9a1c8e72c56b253a0e2fe78393feb7
29a40
>     │   └── main
32c43
< 11 directories, 19 files
---
> 16 directories, 25 files
```