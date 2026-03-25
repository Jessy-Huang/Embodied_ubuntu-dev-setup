---
name: ubuntu-dev-setup
description: 自动化配置 Ubuntu 开发环境；当用户需要初始化新系统、配置算法开发环境、批量安装开发工具时使用
dependency:
  python:
    - requests==2.31.0
---

# Ubuntu 开发环境自动配置

## 任务目标

- 本 Skill 用于：自动化配置 Ubuntu 系统的算法开发环境
- 能力包含：系统检测、工具安装、环境配置、GPU 驱动安装
- 触发条件：新系统初始化、环境重置、批量安装开发工具

## 前置准备

### 依赖说明
```txt
requests==2.31.0
```

### 重要约束
1. **涉及 sudo 权限的操作会提示用户确认，不会自动执行**
2. **涉及重启的操作会收集到最后统一提示**
3. **禁止删除任何已有文件，所有配置操作均为追加或新建**

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
python /workspace/projects/ubuntu-dev-setup/scripts/system_check.py
```

#### 2. 选择配置项
- 参考 [references/tools_guide.md](references/tools_guide.md) 查看可用工具
- 根据用户需求选择要安装的工具分类：
  - **基础工具**：Chrome、Edge、vscode、Cursor、飞书、搜狗输入法等
  - **开发环境**：conda、CUDA、cuDNN、ROS
  - **终端工具**：terminator、zsh、oh-my-zsh
  - **其他工具**：kazam、gparted、todesk、腾讯会议

#### 3. 工具安装
- **apt 安装的工具**：
  - terminator、gparted、kazam、zsh
  - 调用 `scripts/install_package.py`
  - **需要用户确认 sudo 权限**

**示例**：
```bash
# 安装 terminator（需要 sudo）
python /workspace/projects/ubuntu-dev-setup/scripts/install_package.py \
  --package-name terminator \
  --install-type apt \
  --use-sudo
```

- **deb 包安装的工具**：
  - Chrome、Edge、vscode、Cursor、飞书、搜狗输入法等
  - 调用 `scripts/install_package.py` 自动下载安装
  - **需要用户确认 sudo 权限**

**示例**：
```bash
# 安装 Chrome（需要 sudo）
python /workspace/projects/ubuntu-dev-setup/scripts/install_package.py \
  --package-name google-chrome-stable \
  --install-type url \
  --deb-url "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" \
  --use-sudo
```

#### 4. 开发环境配置

##### 4.1 conda 安装与配置
- 下载 Anaconda 安装脚本
- 执行安装（用户确认）
- 配置环境变量
- 配置 conda 环境路径（可选）

**配置环境变量示例**：
```bash
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --config-file ~/.bashrc \
  --env-vars '{"CONDA_PATH": "/home/user/anaconda3/bin"}'
```

##### 4.2 CUDA/cuDNN 安装
- 参考 [references/cuda_guide.md](references/cuda_guide.md) 查看详细步骤
- **强烈建议按顺序执行**：
  1. 安装 NVIDIA 驱动 → **需要重启**
  2. 安装 CUDA Toolkit
  3. 安装 cuDNN
  4. 配置环境变量

**环境变量配置模板**：
```bash
# CUDA 环境变量（根据实际安装版本调整）
python /workspace/projects/ubuntu-dev-setup/scripts/config_env.py \
  --config-file ~/.bashrc \
  --env-vars '{
    "CUDA_PATH": "/usr/local/cuda-12.6",
    "LD_LIBRARY_PATH": "/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH"
  }'
```

##### 4.3 ROS 安装
- 使用 fishros 一键安装
- **需要用户确认 sudo 权限**

```bash
# 下载并执行 fishros
wget http://fishros.com/install -O fishros
chmod +x fishros
sudo ./fishros
```

#### 5. 终端配置（可选）
- 安装 zsh 和 oh-my-zsh
- 配置主题和插件
- 调用 `scripts/setup_zsh.py`

**示例**：
```bash
python /workspace/projects/ubuntu-dev-setup/scripts/setup_zsh.py \
  --plugins "git zsh-autosuggestions zsh-syntax-highlighting" \
  --theme agnoster \
  --use-sudo
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
- **环境配置**：[scripts/config_env.py](scripts/config_env.py) - 配置文件和环境变量管理
- **终端配置**：[scripts/setup_zsh.py](scripts/setup_zsh.py) - zsh 和 oh-my-zsh 配置

### 领域参考
- **工具清单**：[references/tools_guide.md](references/tools_guide.md) - 完整的工具列表和安装说明
- **CUDA 指南**：[references/cuda_guide.md](references/cuda_guide.md) - CUDA/cuDNN 详细配置步骤
- **配置模板**：[references/config_templates.md](references/config_templates.md) - 配置文件模板和环境变量示例

## 注意事项

### 安全与权限
1. **所有 sudo 操作均需用户明确确认**
2. **不会删除任何已有文件或配置**
3. **环境变量配置采用追加方式，不覆盖原有内容**
4. **配置文件修改前会自动备份**

### 安装顺序建议
1. 先安装基础工具（Chrome、vscode 等）
2. 再安装开发环境（conda、CUDA）
3. 最后安装可选工具（zsh、terminator）
4. NVIDIA 驱动安装后必须重启

### 错误处理
- 如果安装失败，脚本会返回详细错误信息
- 智能体会提供常见问题的解决方案
- 用户可以查看日志排查问题

### 典型使用场景

**场景一：全新系统初始化**
```bash
# 1. 检测系统
python scripts/system_check.py

# 2. 安装基础工具（用户选择后逐个确认）
python scripts/install_package.py --package-name google-chrome-stable --install-type url --deb-url "https://..." --use-sudo

# 3. 安装开发环境
# conda（手动下载安装更可靠）
# CUDA/cuDNN（参考 cuda_guide.md）

# 4. 配置终端
python scripts/setup_zsh.py --use-sudo

# 5. 重启系统（如有驱动安装）
```

**场景二：仅安装开发工具**
```bash
# 直接选择需要的工具安装
python scripts/install_package.py --package-name terminator --install-type apt --use-sudo
```

**场景三：配置 CUDA 环境**
```bash
# 参考 cuda_guide.md 的详细步骤
# 安装驱动 → 重启 → 安装 CUDA → 配置环境变量
```

## 使用建议

1. **首次使用**：建议先运行系统检测，了解当前状态
2. **批量安装**：可以准备一个安装列表，逐个确认安装
3. **网络问题**：如下载失败，可手动下载 deb 包后使用本地安装
4. **版本选择**：CUDA 和 cuDNN 版本需根据实际需求选择
5. **环境隔离**：推荐使用 conda 管理不同项目的 Python 环境
