---
name: ubuntu-dev-setup
description: 自动化配置 Ubuntu 开发环境（中国网络优化版）；当用户需要初始化新系统、配置算法开发环境、批量安装开发工具时使用
dependency:
  python:
    - requests==2.31.0
---

# Ubuntu 开发环境自动配置

## 任务目标

- 本 Skill 用于：自动化配置 Ubuntu 系统的算法开发环境
- 能力包含：系统检测、工具安装、环境配置、GPU 驱动安装
- 触发条件：新系统初始化、环境重置、批量安装开发工具
- **特色**：针对中国网络环境优化，使用国内镜像源

## 前置准备

### 依赖说明
```txt
requests==2.31.0
```

### 重要约束
1. **涉及 sudo 权限的操作会提示用户确认，不会自动执行**
2. **涉及重启的操作会收集到最后统一提示**
3. **禁止删除任何已有文件，所有配置操作均为追加或新建**

### 国内网络优化
- oh-my-zsh：使用 Gitee 镜像安装
- zsh 插件：使用 Gitee 镜像克隆
- Docker：使用阿里云镜像安装和加速
- conda/pip：配置清华、阿里云镜像源
- VSCode：提供华为云镜像下载

## 操作步骤

### 标准流程

#### 1. 系统检测（必需）
- 调用 `scripts/system_check.py` 检测系统信息
- 展示当前系统状态：
  - Ubuntu 版本和内核
  - 已安装的开发工具
  - GPU 信息（如有）
  - 可用磁盘空间

**示例**：
```bash
python scripts/system_check.py
```

#### 2. 选择配置项
- 参考 [references/tools_guide.md](references/tools_guide.md) 查看可用工具
- 根据用户需求选择要安装的工具分类：
  - **基础工具**：Chrome、Edge、vscode、Cursor、飞书、搜狗输入法等
  - **代理工具**：Clash Verge（推荐优先安装）
  - **开发环境**：conda、Docker、CUDA、cuDNN、ROS
  - **终端工具**：terminator、zsh、oh-my-zsh
  - **其他工具**：kazam、gparted、todesk、腾讯会议

#### 3. 工具安装

##### apt 安装的工具
- terminator、gparted、kazam、zsh
- 调用 `scripts/install_package.py`
- **需要用户确认 sudo 权限**

**示例**：
```bash
# 安装 terminator（需要 sudo）
python scripts/install_package.py --package-name terminator --install-type apt --use-sudo
```

##### deb 包安装的工具
- Chrome、Edge、vscode、Cursor、飞书、搜狗输入法等
- 调用 `scripts/install_package.py` 自动下载安装
- **需要用户确认 sudo 权限**

**示例**：
```bash
# 安装 Chrome（需要 sudo）
python scripts/install_package.py --package-name google-chrome-stable --install-type url \
    --deb-url "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" --use-sudo
```

#### 4. 开发环境配置

##### 4.1 Docker 安装（推荐）
- **使用阿里云镜像安装**，无需访问 Docker Hub
- 自动配置国内镜像加速器
- 调用 `scripts/install_docker.py`

**示例**：
```bash
# 完整安装 Docker（使用阿里云镜像）
python scripts/install_docker.py --install

# 仅配置镜像加速器
python scripts/install_docker.py --config-mirror
```

##### 4.2 conda 安装与配置
- 下载 Anaconda/Miniconda 安装脚本
- **推荐使用清华镜像下载**：`https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/`
- 执行安装（用户确认）
- 配置清华镜像源

**配置镜像源**：
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --set show_channel_urls yes
```

##### 4.3 CUDA/cuDNN 安装
- 参考 [references/cuda_guide.md](references/cuda_guide.md) 查看详细步骤
- **强烈建议按顺序执行**：
  1. 安装 NVIDIA 驱动 → **需要重启**
  2. 安装 CUDA Toolkit
  3. 安装 cuDNN
  4. 配置环境变量

##### 4.4 ROS 安装
- 使用 fishros 一键安装
- **需要用户确认 sudo 权限**

```bash
wget http://fishros.com/install -O fishros
chmod +x fishros
sudo ./fishros
```

#### 5. 终端配置（可选）
- 安装 zsh 和 oh-my-zsh
- **使用 Gitee 镜像安装**，无需访问 GitHub
- 配置主题和插件
- 调用 `scripts/setup_zsh.py`

**示例**：
```bash
# 完整安装（使用国内镜像）
python scripts/setup_zsh.py --use-sudo --install-oh-my-zsh --china-mirror \
    --plugins "git zsh-autosuggestions zsh-syntax-highlighting"
```

#### 6. 重启提示（如有需要）
- 收集所有需要重启的操作
- 提示用户保存工作后重启
- 列出待重启项：
  - NVIDIA 驱动安装
  - CUDA 安装
  - 系统级配置更改

## 资源索引

### 必要脚本
- **系统检测**：[scripts/system_check.py](scripts/system_check.py) - 检测 Ubuntu 系统信息
- **工具安装**：[scripts/install_package.py](scripts/install_package.py) - 统一的安装工具（支持 apt/deb/url）
- **Docker 安装**：[scripts/install_docker.py](scripts/install_docker.py) - Docker 安装（阿里云镜像）
- **环境配置**：[scripts/config_env.py](scripts/config_env.py) - 配置文件和环境变量管理
- **终端配置**：[scripts/setup_zsh.py](scripts/setup_zsh.py) - zsh 和 oh-my-zsh 配置（Gitee 镜像）

### 领域参考
- **工具清单**：[references/tools_guide.md](references/tools_guide.md) - 完整的工具列表和国内镜像说明
- **CUDA 指南**：[references/cuda_guide.md](references/cuda_guide.md) - CUDA/cuDNN 详细配置步骤
- **配置模板**：[references/config_templates.md](references/config_templates.md) - 配置文件模板和国内镜像配置

## 注意事项

### 安全与权限
1. **所有 sudo 操作均需用户明确确认**
2. **不会删除任何已有文件或配置**
3. **环境变量配置采用追加方式，不覆盖原有内容**
4. **配置文件修改前会自动备份**

### 国内网络优化
1. **优先使用国内镜像源**：清华、阿里云、Gitee
2. **GitHub 相关**：oh-my-zsh、zsh 插件使用 Gitee 镜像
3. **Docker**：使用阿里云镜像安装和加速
4. **代理工具**：推荐先安装 Clash Verge

### 安装顺序建议
1. 先安装代理工具（Clash Verge）- 便于后续访问 GitHub
2. 再安装基础工具（Chrome、vscode 等）
3. 然后安装开发环境（Docker、conda、CUDA）
4. 最后安装可选工具（zsh、terminator）
5. NVIDIA 驱动安装后必须重启

### 错误处理
- 如果安装失败，脚本会返回详细错误信息
- 智能体会提供常见问题的解决方案
- 用户可以查看日志排查问题

### 典型使用场景

**场景一：全新系统初始化**
```bash
# 1. 检测系统
python scripts/system_check.py

# 2. 安装代理工具（优先）
# 手动下载 Clash Verge 或使用代理

# 3. 安装 Docker（使用阿里云镜像）
python scripts/install_docker.py --install

# 4. 安装 zsh（使用 Gitee 镜像）
python scripts/setup_zsh.py --use-sudo --install-oh-my-zsh --china-mirror \
    --plugins "git zsh-autosuggestions zsh-syntax-highlighting"

# 5. 安装基础工具
python scripts/install_package.py --package-name google-chrome-stable --install-type url \
    --deb-url "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" --use-sudo

# 6. CUDA/cuDNN 安装（参考 cuda_guide.md）
# ...

# 7. 重启系统（如有驱动安装）
```

**场景二：仅安装 Docker**
```bash
python scripts/install_docker.py --install
```

**场景三：配置国内镜像源**
```bash
# pip 镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# conda 镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --set show_channel_urls yes

# Docker 镜像
python scripts/install_docker.py --config-mirror
```

## 使用建议

1. **首次使用**：建议先运行系统检测，了解当前状态
2. **网络问题**：优先安装 Clash Verge，配置代理后再安装其他工具
3. **批量安装**：可以准备一个安装列表，逐个确认安装
4. **版本选择**：CUDA 和 cuDNN 版本需根据实际需求选择
5. **环境隔离**：推荐使用 conda 管理不同项目的 Python 环境

## 国内镜像源汇总

| 类型 | 镜像源 | 地址 |
|------|--------|------|
| pip | 清华 | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| pip | 阿里云 | `https://mirrors.aliyun.com/pypi/simple/` |
| conda | 清华 | `https://mirrors.tuna.tsinghua.edu.cn/anaconda/` |
| Docker | 阿里云 | `https://mirrors.aliyun.com/docker-ce/` |
| oh-my-zsh | Gitee | `https://gitee.com/shmhlsy/oh-my-zsh-install.sh` |
| VSCode | 华为云 | `https://mirrors.huaweicloud.com/vscode/` |
| apt | 清华 | `https://mirrors.tuna.tsinghua.edu.cn/ubuntu/` |
