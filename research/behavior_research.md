# Research of Behavior

## index

```bash
ochir@cygni:~/experiment/expgit$ git ls-files -s
100644 ce013625030ba8dba906f756967f9e9ca394464a 0       hello.txt
ochir@cygni:~/experiment/expgit$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   hello.txt

ochir@cygni:~/experiment/expgit$ git commit -m "first"
[main (root-commit) 4f9c8e0] first
 1 file changed, 1 insertion(+)
 create mode 100644 hello.txt
ochir@cygni:~/experiment/expgit$ git ls-files -s
100644 ce013625030ba8dba906f756967f9e9ca394464a 0       hello.txt
ochir@cygni:~/experiment/expgit$ echo goodbye > hello.txt
ochir@cygni:~/experiment/expgit$ git add hello.txt 
ochir@cygni:~/experiment/expgit$ git ls-files -s
100644 dd7e1c6f0fefe118f0b63d9f10908c460aa317a6 0       hello.txt
ochir@cygni:~/experiment/expgit$ git commit -m "second"
[main 9b787d1] second
 1 file changed, 1 insertion(+), 1 deletion(-)
ochir@cygni:~/experiment/expgit$ git ls-files -s
100644 dd7e1c6f0fefe118f0b63d9f10908c460aa317a6 0       hello.txt
```

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