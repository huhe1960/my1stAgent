# Git 更新流程（现有项目目录从 Gitee 拉取最新代码）

适用场景：你已经有一个本地目录（例如 `~/hpc-agent-system`），并且它是一个 Git 仓库；现在要从远程仓库 `https://gitee.com/mawanting/hpc-agent-system` 更新到最新代码。

---

## 1. 进入项目目录并确认仓库状态

```bash
cd ~/hpc-agent-system
git status
```

- 如果能正常输出分支、改动信息：说明这是 Git 仓库，继续下一步。
- 如果提示不是 git 仓库：说明你当前目录不对，或者这个目录不是通过 git clone 得到的。

---

## 2. 确认远程地址（origin）是否指向正确的 Gitee 仓库

```bash
git remote -v
```

理想情况：`origin` 指向 `https://gitee.com/mawanting/hpc-agent-system.git`

如果不是，改成正确地址：

```bash
git remote set-url origin https://gitee.com/mawanting/hpc-agent-system.git
git remote -v
```

---

## 3. 更新代码（推荐：fetch + pull --rebase）

### 3.1 推荐做法（更干净的提交历史）

```bash
git fetch --all --prune
git pull --rebase
```

### 3.2 简单做法（不使用 rebase）

```bash
git pull
```

---

## 4. 如果你本地改过文件导致无法更新

先查看当前状态：

```bash
git status
```

### 4.1 保留本地改动（推荐）

```bash
git stash -u
git pull --rebase
git stash pop
```

如果 `stash pop` 出现冲突，按 `git status` 的提示逐个解决冲突文件，然后：

```bash
git add -A
git rebase --continue   # 如果是 rebase 场景
```

### 4.2 放弃本地改动，强制与远程一致（谨慎，会丢本地改动）

先确认远程主分支叫 `main` 还是 `master`（二选一）：

```bash
git branch -vv
```

然后二选一执行：

```bash
git fetch --all --prune
git reset --hard origin/main
```

或

```bash
git fetch --all --prune
git reset --hard origin/master
```

---

## 5. 常用检查命令

- 查看当前使用的远程地址：

```bash
git remote -v
```

- 查看当前分支与远程跟踪关系：

```bash
git branch -vv
```

- 查看最近提交：

```bash
git log --oneline -n 10
```


