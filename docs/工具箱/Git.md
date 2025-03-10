## HELLO, GIT!

Git是目前世界上最为广泛应用的分布式版本控制系统，学习git能很好地提高项目开发、团队协作的效率。

在Windows上使用Git，可以从Git官网直接[下载安装程序](https://git-scm.com/downloads)，然后按默认选项安装即可。

同步可以使用[sourcetree](https://www.sourcetreeapp.com/)进行图形化的git使用

使用git最好结合github等仓库托管平台。

以下的学习参考了官方文档和多个博客，尤其感谢[@廖雪峰](https://www.liaoxuefeng.com/wiki/896043488029600)的相关教程

## GIT本当上手

我们以下采用git的命令界面进行开发工作，打开git bash。

### 绑定github：

输入`  ssh-keygen -t rsa`创造密钥，并在文件中找到对应的公钥（一般在C:/Users/<username>/.ssh），一般形如id_rsa.pub，粘贴。

打开github主页，点击**settings**，点击**SSH and GPG keys，**再点击 **New SSH key**，**Add SSH key**，复制你的密钥



![v2-0b61abaf4069dc04003e85e7499d42b0_720w](/post_content/Git/v2-0b61abaf4069dc04003e85e7499d42b0_720w.png)

在github上输入`ssh -T git@github.com `登陆github

![Snipaste_2024-04-02_14-22-26](/post_content/Git/Snipaste_2024-04-02_14-22-26.png)

### 链接仓库与开发：

##### 链接仓库：

首先，在github上，在右上角“+”处，创建新的仓库（或者选取已有仓库），复制仓库地址。

在git使用`cd`命令切换到目标目录，并输入`git clone <仓库地址>` ，即可。

也可以使用` git remote add origin <仓库地址>`链接空仓库。

（注意，可以将地址的https改为git，使用<u>ssh</u>协议提高速度）

##### 暂存与提交：

对仓库内代码进行修改以后，可以执行以下操作：

- (optional)在根目录下建立.gitignore文件，忽略不需暂存的文件。

  可参考官方的[.gitignore配置文档](https://github.com/github/gitignore)

- (optional)`git remote add <仓库地址>`链接远程仓库

- (optional)`git branch -m <newname>` 改变分支名。

- `add <filename>`将需要提交的文件放入暂存区，或者：

  - `git add.` 暂存所有的文件
  - `git -f` 强制暂存目标文件
  - `git add -u.` 暂存修改的文件，不包括新文件

- `git commit -m "<信息>"`提交内容并附加提交信息，第一次提交需要设定名字和邮箱

  ```
  git config --global user.name "<yourname>"
  git config --global user.email "***@***.com"
  ```

- `git push origin <branchname>`提交你的分支。

**删除文件**：

1. `rm <filename>`： 删除本地文件
2. `git rm <filename>`： 暂存删除请求。
3. `git commit -m "<删除信息>"`：提交删除修改。



### 换行的报错：

在使用add指令暂存的时候，我们可能遇到如下的报错。

#### ![Snipaste_2024-04-02_15-07-00](/post_content/Git/Snipaste_2024-04-02_15-07-00.png)

这是因为换行符的在不同平台并不统一的原因。

- Dos和Windows平台： 使用回车（CR）和换行（LF）两个字符来结束一行，回车+换行(CR+LF)，即“\r\n”；
- Mac 和 Linux平台：只使用换行（LF）一个字符来结束一行，即“\n”；

可以采用以下的解决方案：

- 对于windows平台，输入`git config --global core.autocrlf true`，打开git 的自动转化，提交时转换为LF，检出时转换为CRLF。
- 对于Mac或者Linux，输入`git config --global core.autocrlf input`提交时候把CRLF转化为LF
- 或者设置`git config --global core.autocrlf false`，再修改文件编辑器的.editorconfig 来保证文件都是 LF 结尾。



## 时光机穿梭：

### 查询与记录：

**检查与对比**：

运行`git status`命令可以看查结果，而`git diff`可以看出具体内容。

**记录查询**：

- `git reflog`: 	可以看到所有的操作指令和版本编号
- `git log`:	可以看到详细的修改日志，有以下参数可选：
  - `-p`：	事无巨细地显示每次修改以及详细内容。
  - `--stat`：	显示每次修改的统计信息，如修改文件、行数增减
  - `--online`:	以列表形式看查版本记录。
  - `--graph`：  以图表形式展现，可以看查分支的演化。
  - `-n <num>`:  显示对应数量的log。
  - `--author=<name>`： 显示对应作者提交的记录。
  - `--branches=<branchname>`： 显示对应分支日志。 
  - `... <filename>`：  对应文件的修改日志。

##### 绑定标签：

- `git tag -a <tagname> -m "<massage>" 1094a...(<提交特征号>)`：为某次提交记录标签。
- `git push origin <tagname>`：推送某个标签。
- `git tag -d <tagname>`:  删除某个标签。
- `git push origin :refs/tags/<tagname>` ：在上一步后，删除另一个标签



### 版本退回：

**版本回退**：

采用`git reset --<模式参数> <版本参数>`

- 模式参数：

  - `hard`:  删除所有的修改，并回到指定的提交。适用于回退到历史版本、撤销错误提交。

  - `soft`:  不会修改工作区和暂存区，只是指针退回指定版本。适合修改提交信息。

    （但也可以用`git commit --amend -m <新信息>`来修改)

  - `mixed`:  默认参数，只是修改暂存区，适合取消部分提交。

- 版本参数：
  - `HEAD^`： 回退到上个版本，多一个^多回退一个。
  - `HEAD~n`： 回退到上n个版本。
  - `1094a...`:  回退到制定的版本号。

**撤销修改**：

- `git revert HEAD`：  提交一个与指定提交相反的操作。

- `git checkout -- <filename>`： 将文件复原到最近一次add/commit的状态。

  （注意不能删去--！否则是分支切换）

- `git reset HEAD <filename>`：  将文件从暂存区退回到工作区。



## 多元仓库宇宙

### 分支操作：

##### 分支本质——<u>指针的切换</u>：

<img src="/post_content/Git/Snipaste_2024-04-02_20-53-58.png"
style="float: left;"
alt="Snipaste_2024-04-02_20-53-58"  />

新的分支会产生新的指针，之后最简单的合并方式就是将dev指针用master覆盖。

**分支基础操作**：

- `git checkout -b <branchname>`:  创建新分支，并切换
- `git branch`:  查看所有分支以及当前分支
- `git checkout <branchname>`：  切换到指定分支
- `git merge <A>`：  合并A到当前分支，如无冲突即快进模式（切换指针）
  - `--no-ff -m "<合并描述>"`:  (optional)保留分支合并过程的提交信息
- `git branch -d <branchname>`:   删除对应分支
- `git cherry-pick <提交特征号>`： 复制其他分支的改动操作

因为创建、合并和删除分支非常快，所以Git鼓励你使用分支完成某个任务，合并后再删掉分支，这和直接在`master`分支上工作效果是一样的，但过程更安全。

**分支冲突处理**：

在存在分支文件不同的情况下，使用`merge`会出现冲突报错。

此时，对冲突文件进行修改并提交，就能实现合并。

**工作区储存**：

当需要切换到别的分支工作，当前工作又进行到一半时，可以先储存工作区。

- `git stash`:  储存当前工作区的修改内容并回到现版本。

- `git stash list`:  展示储存区内容

- `git stash apply stash@{n}` ： 回到第n个储存内容。

  注意，越早的储存，n越大。并且stash的恢复无法覆盖冲突文件。

- `git stash drop`： 可以删除无用的储存

- `git stash pop`:  可以回到存储内容并自动删除存储。



### 团队协作：

**团队协作概述**：

在实际开发中，我们应该按照几个基本原则进行分支管理：

`master`分支应该是非常稳定的，也就是仅用来发布新版本。

`dev`分支上，进行开发工作的合并，发布时再把`dev`分支合并到`master`上。

`<other>`其他分支上，团队人员分别在自己领域开发，并将成果合并到dev上。



<img src="/post_content/Git/Snipaste_2024-04-02_21-22-01-17120684018941.png" alt="Snipaste_2024-04-02_21-22-01" style="float: left;" />



**团队合作步骤**：

1. 尝试推送，若推送失败，先新建并抓取远程到对应分支

   代码实现：`git branch --set-upstream-to <branch-name> origin/<branch-name>`

2. 本地合并拉取的分支和尝试推送的分支，解决冲突。

3. 再次尝试推送。

#### 版本号编辑

受广泛认可的格式是这样的：主版本号.次版本号.补丁号。相关规则有：

- 如果新的版本没有改变 API，请将补丁号递增；
- 如果您添加了 API 并且该改动是向后兼容的，请将次版本号递增；
- 如果您修改了 API 但是它并不向后兼容，请将主版本号递增。
