# 配置文件模板

本文档提供各类配置文件的模板，包括环境变量、conda 配置、shell 配置等。

## 目录
- [Shell 环境变量配置](#shell-环境变量配置)
- [Conda 配置](#conda-配置)
- [Zsh 配置](#zsh-配置)
- [桌面快捷方式](#桌面快捷方式)

---

## Shell 环境变量配置

### .bashrc 完整模板

将以下内容追加到 `~/.bashrc` 文件末尾：

```bash
# ==============================================================================
# Ubuntu Dev Setup - 环境变量配置
# 由 ubuntu-dev-setup 自动添加
# ==============================================================================

# ------------------------------------------------------------------------------
# CUDA 环境变量 (根据实际安装版本调整)
# ------------------------------------------------------------------------------
export CUDA_PATH=/usr/local/cuda-12.6
export PATH=$CUDA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH
export CUDADIR=$CUDA_PATH

# cuDNN 环境变量
export CUDNN_INCLUDE_DIR=$CUDA_PATH/include
export CUDNN_LIB_DIR=$CUDA_PATH/lib64

# ------------------------------------------------------------------------------
# Conda 环境变量 (如果使用 bash)
# ------------------------------------------------------------------------------
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/YOUR_USERNAME/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/YOUR_USERNAME/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/YOUR_USERNAME/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/YOUR_USERNAME/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# ------------------------------------------------------------------------------
# 自定义环境变量
# ------------------------------------------------------------------------------
# Python 编码
export PYTHONIOENCODING=utf-8

# CUDA 可见设备（可选，用于指定使用哪些 GPU）
# export CUDA_VISIBLE_DEVICES=0,1

# ------------------------------------------------------------------------------
# 别名设置
# ------------------------------------------------------------------------------
# 常用命令别名
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Git 别名
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph'

# Conda 别名
alias cenv='conda env list'
alias cact='conda activate'
alias cdeact='conda deactivate'

# ------------------------------------------------------------------------------
# PATH 扩展
# ------------------------------------------------------------------------------
# 添加用户 bin 目录
export PATH=$HOME/.local/bin:$PATH

# 添加 CUDA 路径（确保在最前面）
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

### CUDA 环境变量（独立）

仅 CUDA/cuDNN 相关配置：

```bash
# CUDA 12.6 环境变量
export CUDA_PATH=/usr/local/cuda-12.6
export PATH=$CUDA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH
export CUDADIR=$CUDA_PATH

# cuDNN 路径
export CUDNN_INCLUDE_DIR=$CUDA_PATH/include
export CUDNN_LIB_DIR=$CUDA_PATH/lib64
```

### CUDA 12.1 环境变量

```bash
# CUDA 12.1 环境变量
export CUDA_PATH=/usr/local/cuda-12.1
export PATH=$CUDA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH
export CUDADIR=$CUDA_PATH
```

---

## Conda 配置

### .condarc 基础模板

创建 `~/.condarc` 文件：

```yaml
# Conda 配置文件
# 将环境存储在指定路径（避免占用主目录空间）
envs_dirs:
  - ~/workspace/anaconda3/envs
  - ~/.conda/envs

# 包缓存路径
pkgs_dirs:
  - ~/workspace/anaconda3/pkgs
  - ~/.conda/pkgs

# 频道配置
channels:
  - defaults
  - conda-forge

# 显示频道 URL
show_channel_urls: true

# 默认 Python 版本（可选）
# default_python: 3.10

# 自动激活 base 环境（可选，默认 true）
# auto_activate_base: false
```

### .condarc 自定义环境路径

将 conda 环境存储在大容量磁盘：

```yaml
envs_dirs:
  - /media/your_disk/workspace/anaconda3/envs
  - ~/anaconda3/envs

pkgs_dirs:
  - /media/your_disk/workspace/anaconda3/pkgs
  - ~/anaconda3/pkgs

channels:
  - defaults
  - conda-forge

show_channel_urls: true
```

### 国内镜像源配置

```yaml
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - defaults

show_channel_urls: true
```

---

## Zsh 配置

### .zshrc 基础模板

```bash
# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# 主题设置
ZSH_THEME="robbyrussell"
# ZSH_THEME="agnoster"  # 更美观的主题

# 插件配置
plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
    sudo
    copypath
    copyfile
    history
    python
)

source $ZSH/oh-my-zsh.sh

# 用户配置
# ------------------------------------------------------------------------------

# 环境变量
export PATH=$HOME/bin:$HOME/.local/bin:$PATH
export LANG=en_US.UTF-8

# CUDA 环境变量
export CUDA_PATH=/usr/local/cuda-12.6
export PATH=$CUDA_PATH/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH

# Conda 初始化
# >>> conda initialize >>>
__conda_setup="$('/home/YOUR_USERNAME/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/YOUR_USERNAME/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/YOUR_USERNAME/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/YOUR_USERNAME/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# 别名
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias cls='clear'
alias ..='cd ..'
alias ...='cd ../..'

# Git 别名
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'

# Python 别名
alias python='python3'
alias pip='pip3'
alias pipi='pip install -i https://pypi.tuna.tsinghua.edu.cn/simple'

# Conda 别名
alias cenv='conda env list'
alias cact='conda activate'
alias cdeact='conda deactivate'
alias ccreate='conda create -n'
alias cremove='conda env remove -n'

# 历史记录配置
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
```

### .zshrc 插件推荐

```bash
# 推荐插件组合
plugins=(
    # Git 相关
    git                    # Git 快捷命令
    gitignore             # 生成 .gitignore

    # 自动补全和建议
    zsh-autosuggestions   # 命令自动建议
    zsh-syntax-highlighting # 语法高亮

    # 系统工具
    sudo                  # 双击 ESC 在命令前加 sudo
    copypath              # 复制当前路径
    copyfile              # 复制文件内容
    extract               # 一键解压

    # 开发工具
    python                # Python 别名
    pip                   # pip 补全
    conda                 # conda 补全

    # 其他
    history               # 历史命令
    colored-man-pages     # 彩色 man 手册
    command-not-found     # 未找到命令建议
)
```

---

## 桌面快捷方式

### 创建桌面快捷方式的方法

#### 方法一：手动创建

1. 创建 `.desktop` 文件：
```bash
nano ~/.local/share/applications/appname.desktop
```

2. 写入内容：
```desktop
[Desktop Entry]
Version=1.0
Name=应用名称
Comment=应用描述
Exec=/path/to/executable
Icon=/path/to/icon.png
Terminal=false
Type=Application
Categories=Development;
```

3. 设置权限：
```bash
chmod +x ~/.local/share/applications/appname.desktop
```

#### 方法二：从已有快捷方式复制

```bash
# 查找已安装应用的快捷方式
ls /usr/share/applications/

# 复制到桌面
cp /usr/share/applications/code.desktop ~/Desktop/
chmod +x ~/Desktop/code.desktop
```

### Chrome 桌面快捷方式

```desktop
[Desktop Entry]
Version=1.0
Name=Google Chrome
GenericName=Web Browser
Comment=Access the Internet
Exec=/usr/bin/google-chrome-stable %U
StartupNotify=true
Terminal=false
Icon=google-chrome
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
Actions=new-window;new-private-window;

[Desktop Action new-window]
Name=New Window
Exec=/usr/bin/google-chrome-stable

[Desktop Action new-private-window]
Name=New Incognito Window
Exec=/usr/bin/google-chrome-stable --incognito
```

### VSCode 桌面快捷方式

```desktop
[Desktop Entry]
Name=Visual Studio Code
Comment=Code Editing. Redefined.
GenericName=Text Editor
Exec=/usr/share/code/code --unity-launch %F
Icon=vscode
Type=Application
StartupNotify=false
StartupWMClass=Code
Categories=TextEditor;Development;IDE;
MimeType=text/plain;inode/directory;
Actions=new-empty-window;
Keywords=vscode;

[Desktop Action new-empty-window]
Name=New Empty Window
Exec=/usr/share/code/code --new-window %F
Icon=vscode
```

### Cursor 桌面快捷方式

```desktop
[Desktop Entry]
Name=Cursor
Comment=AI-powered code editor
Exec=/opt/Cursor/cursor %F
Icon=cursor
Type=Application
Categories=Development;IDE;
StartupNotify=true
MimeType=text/plain;
```

### Anaconda Navigator 桌面快捷方式

```desktop
[Desktop Entry]
Name=Anaconda Navigator
GenericName=Anaconda Navigator
Exec=/home/YOUR_USERNAME/anaconda3/bin/anaconda-navigator
Icon=/home/YOUR_USERNAME/anaconda3/lib/python3.11/site-packages/anaconda_navigator/static/images/anaconda-icon-256x256.png
Terminal=false
Type=Application
Categories=Development;
```

### 自定义脚本桌面快捷方式

```desktop
[Desktop Entry]
Version=1.0
Name=My Script
Comment=运行自定义脚本
Exec=/home/username/scripts/myscript.sh
Icon=application-x-executable
Terminal=true
Type=Application
Categories=Utility;
```

---

## Git 配置

### .gitconfig 模板

```ini
[user]
    name = Your Name
    email = your.email@example.com

[core]
    editor = code --wait
    autocrlf = input
    quotepath = false

[color]
    ui = auto

[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --oneline --graph --decorate --all
    amend = commit --amend --no-edit

[push]
    default = simple

[pull]
    rebase = false

[init]
    defaultBranch = main
```

---

## 使用脚本配置

### 自动配置环境变量

```bash
# 配置 CUDA 环境
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --setup-cuda --cuda-version 12.6

# 配置 cuDNN 环境
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --setup-cudnn --cuda-version 12.6

# 配置 conda 环境
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --setup-conda --conda-path ~/anaconda3

# 创建 .condarc
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --create-condarc \
  --envs-dirs '["~/workspace/anaconda3/envs"]'
```

### 自定义环境变量

```bash
# 添加自定义环境变量到 .bashrc
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --config-file ~/.bashrc \
  --env-vars '{
    "MY_PROJECT_HOME": "/home/user/projects",
    "JAVA_HOME": "/usr/lib/jvm/java-11-openjdk-amd64"
  }'
```
