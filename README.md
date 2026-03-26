# EAI-Dev-Setup

[![ClawHub](https://img.shields.io/badge/ClawHub-eai--dev--setup-blue)](https://clawhub.ai/skills/eai-dev-setup)
[![GitHub](https://img.shields.io/badge/GitHub-Embodied__ubuntu--dev--setup-black)](https://github.com/Jessy-Huang/Embodied_ubuntu-dev-setup)
[![License](https://img.shields.io/badge/License-MIT--0-green)](LICENSE)

**EAI-Dev-Setup** 是一个自动化配置 Ubuntu 算法开发环境的 Skill，针对中国网络环境进行了深度优化。

## ✨ 功能特性

### 🌐 国内网络优化
- **GitHub 代理**：使用 gh-proxy.org 加速所有 GitHub 访问
- **HuggingFace 镜像**：使用 hf-mirror.com 加速模型下载
- **Docker 镜像**：使用阿里云镜像安装和加速
- **pip/conda 镜像**：配置清华、阿里云镜像源
- **oh-my-zsh 镜像**：使用 Gitee 镜像安装

### 🛠️ 自动化安装
- **基础工具**：Chrome、Edge、VSCode、Cursor、飞书等
- **开发环境**：Docker、Conda、CUDA、cuDNN、ROS
- **终端工具**：Terminator、Zsh + Oh-My-Zsh
- **其他工具**：Kazam、GParted、ToDesk 等

### 📊 用户友好
- 分步引导安装流程
- 每步询问用户确认
- 进度提示和时间预估
- 下载进度条显示
- sudo 操作需用户明确同意

## 📋 支持的工具

| 分类 | 工具 |
|------|------|
| 浏览器 | Chrome、Edge、Firefox |
| 编辑器 | VSCode、Cursor |
| 办公通讯 | 飞书、ToDesk、腾讯会议、WPS、搜狗输入法 |
| 开发环境 | Docker、Conda/Anaconda、CUDA、cuDNN、ROS |
| 终端工具 | Terminator、Zsh、Oh-My-Zsh |
| 其他工具 | Kazam、GParted、Clash Verge |

## 🚀 安装方式

### 方式一：通过 ClawHub 安装（推荐）

```bash
npx clawhub@latest install eai-dev-setup
```

### 方式二：手动下载

```bash
# 克隆仓库
git clone https://github.com/Jessy-Huang/Embodied_ubuntu-dev-setup.git

# 或下载 .skill 文件
wget https://clawhub.ai/skills/eai-dev-setup/download
```

## 📖 快速上手

### 第一步：系统检测

```bash
python scripts/system_check.py
```

检测内容包括：
- Ubuntu 版本和内核
- 已安装的开发工具
- GPU 信息（如有）
- 可用磁盘空间

### 第二步：配置网络代理

```bash
# 配置 GitHub 代理（加速所有 git 操作）
git config --global url."https://gh-proxy.org/https://github.com/".insteadOf "https://github.com/"

# 配置 HuggingFace 镜像（加速模型下载）
echo "export HF_ENDPOINT=https://hf-mirror.com" >> ~/.bashrc
source ~/.bashrc
```

### 第三步：安装 Docker

```bash
python scripts/install_docker.py --install
```

### 第四步：安装 Zsh

```bash
python scripts/setup_zsh.py --use-sudo --install-oh-my-zsh --china-mirror \
    --plugins "git zsh-autosuggestions zsh-syntax-highlighting"
```

### 第五步：安装基础工具

```bash
# 安装 Chrome
python scripts/install_package.py --package-name google-chrome-stable \
    --install-type url \
    --deb-url "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" \
    --use-sudo

# 安装 VSCode
python scripts/install_package.py --package-name code \
    --install-type url \
    --deb-url "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64" \
    --use-sudo
```

## 📚 文档

- [工具清单](eai-dev-setup/references/tools_guide.md) - 完整的工具列表和安装说明
- [CUDA 指南](eai-dev-setup/references/cuda_guide.md) - CUDA/cuDNN 详细配置步骤
- [配置模板](eai-dev-setup/references/config_templates.md) - 配置文件模板和镜像源配置

## 🔧 脚本说明

| 脚本 | 功能 |
|------|------|
| `system_check.py` | 检测 Ubuntu 系统信息 |
| `install_package.py` | 统一的软件包安装工具 |
| `install_docker.py` | Docker 安装（阿里云镜像） |
| `config_env.py` | 配置文件和环境变量管理 |
| `setup_zsh.py` | Zsh 和 Oh-My-Zsh 配置 |

## 🌍 国内镜像源汇总

| 类型 | 镜像源 | 地址 |
|------|--------|------|
| GitHub | gh-proxy | `https://gh-proxy.org/https://github.com/` |
| HuggingFace | hf-mirror | `https://hf-mirror.com` |
| pip | 清华 | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| conda | 清华 | `https://mirrors.tuna.tsinghua.edu.cn/anaconda/` |
| Docker | 阿里云 | `https://mirrors.aliyun.com/docker-ce/` |
| oh-my-zsh | Gitee | `https://gitee.com/shmhlsy/oh-my-zsh-install.sh` |
| apt | 清华 | `https://mirrors.tuna.tsinghua.edu.cn/ubuntu/` |

## 📦 发布平台

本 Skill 已发布到以下平台：

| 平台 | 地址 |
|------|------|
| **ClawHub** | https://clawhub.ai/skills/eai-dev-setup |
| **GitHub** | https://github.com/Jessy-Huang/Embodied_ubuntu-dev-setup |

## ⚠️ 注意事项

1. **权限要求**：涉及 sudo 权限的操作会提示用户确认
2. **禁止删除**：不会删除任何已有文件或配置
3. **重启提示**：安装 NVIDIA 驱动或 CUDA 后需要重启系统
4. **网络问题**：建议先配置 GitHub 代理再执行其他安装

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT-0](LICENSE) - 自由使用、修改和分发，无需署名。

---

**作者**: [@Jessy-Huang](https://github.com/Jessy-Huang)
