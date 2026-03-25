# Ubuntu 开发工具清单

本文档列出所有可自动安装的工具，包括安装方式、权限要求和注意事项。

## 目录
- [基础工具](#基础工具)
- [开发环境](#开发环境)
- [终端工具](#终端工具)
- [其他工具](#其他工具)

---

## 基础工具

### 浏览器类

#### Google Chrome
- **作用**：主流浏览器，比 Firefox 更流畅
- **安装方式**：deb 包下载安装
- **下载地址**：`https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`google-chrome-stable`

#### Microsoft Edge
- **作用**：微软浏览器，兼容性好
- **安装方式**：deb 包下载安装
- **下载地址**：`https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/microsoft-edge-stable_120.0.2210.121-1_amd64.deb` (需更新)
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`microsoft-edge-stable`

### 编辑器类

#### Visual Studio Code
- **作用**：必装的代码编辑器
- **安装方式**：deb 包下载安装
- **下载地址**：`https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`code`

#### Cursor
- **作用**：AI 代码编辑器，类似 VSCode 但集成 AI 功能
- **安装方式**：deb 包下载安装
- **下载地址**：`https://www.cursor.com/api/download?platform=linux&arch=x64&releaseTrack=stable`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`cursor`

### 办公通讯类

#### 飞书
- **作用**：企业协作工具
- **安装方式**：deb 包下载安装
- **下载地址**：`https://www.feishu.cn/api/download?platform=linux&arch=x64`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`feishu`

#### ToDesk
- **作用**：远程桌面工具
- **安装方式**：deb 包下载安装
- **下载地址**：`https://dl.todesk.com/linux/todesk_4.7.2.0_amd64.deb` (需更新)
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`todesk`

#### 腾讯会议
- **作用**：视频会议工具
- **安装方式**：deb 包下载安装
- **下载地址**：需从官网获取最新链接
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`tencent-meeting`

#### WPS Office
- **作用**：办公文档套件
- **安装方式**：deb 包下载安装
- **下载地址**：
  - 官网：`https://www.wps.cn/product/wpslinux`
  - 教育版：`https://inforcenter.dhu.edu.cn/2024/1120/c21332a353377/page.htm`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`wps-office`

#### 搜狗输入法
- **作用**：中文输入法
- **安装方式**：deb 包安装 + fcitx 配置
- **下载地址**：`https://shurufa.sogou.com/linux`
- **需要 sudo**：是
- **需要重启**：是（配置后需重启）
- **包名**：`sogoupinyin`
- **注意事项**：
  - 需要先安装 fcitx 框架：`sudo apt install fcitx fcitx-bin fcitx-table-all fcitx-config-gtk`
  - 安装后在系统设置中配置输入法

---

## 开发环境

### Conda (Anaconda/Miniconda)
- **作用**：Python 环境管理工具，深度学习必备
- **安装方式**：脚本安装
- **下载地址**：
  - Anaconda：`https://www.anaconda.com/download/success`
  - Miniconda：`https://docs.conda.io/en/latest/miniconda.html`
- **需要 sudo**：否（建议用户级安装）
- **需要重启**：否
- **安装步骤**：
  1. 下载安装脚本
  2. 执行 `bash Anaconda3-xxx-Linux-x86_64.sh`
  3. 配置环境变量（自动或手动）
  4. 可选：配置 `.condarc` 指定环境路径

### CUDA Toolkit
- **作用**：NVIDIA GPU 并行计算平台
- **安装方式**：deb 包安装
- **版本选择**：根据深度学习框架和显卡型号选择
  - CUDA 12.6：最新版本，支持最新 GPU
  - CUDA 12.1：TensorFlow 2.15+ 推荐
  - CUDA 11.8：PyTorch 2.0+ 推荐
- **下载地址**：`https://developer.nvidia.com/cuda-downloads`
- **需要 sudo**：是
- **需要重启**：是（驱动安装后）
- **注意事项**：
  - 先安装 NVIDIA 驱动，重启后再安装 CUDA
  - 安装后需配置环境变量

### cuDNN
- **作用**：深度学习加速库
- **安装方式**：deb 包安装
- **版本要求**：需与 CUDA 版本匹配
- **下载地址**：`https://developer.nvidia.com/cudnn`
- **需要 sudo**：是
- **需要重启**：否
- **注意事项**：
  - 需要 NVIDIA 开发者账号
  - 安装后需配置环境变量

### ROS (Robot Operating System)
- **作用**：机器人操作系统
- **安装方式**：一键安装脚本 (fishros)
- **下载地址**：`http://fishros.com/install`
- **需要 sudo**：是
- **需要重启**：否
- **安装步骤**：
  ```bash
  wget http://fishros.com/install -O fishros
  sudo chmod +x ./fishros
  sudo ./fishros
  ```
- **注意事项**：根据提示选择 ROS 版本

---

## 终端工具

#### Terminator
- **作用**：多窗口终端，可分屏
- **安装方式**：apt 安装
- **安装命令**：`sudo apt install terminator -y`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`terminator`

#### Zsh
- **作用**：增强型 shell，支持插件和主题
- **安装方式**：apt 安装 + oh-my-zsh
- **安装命令**：`sudo apt install zsh -y`
- **需要 sudo**：是
- **需要重启**：否（但需注销重登录切换默认 shell）
- **推荐插件**：
  - `git`：Git 快捷命令
  - `zsh-autosuggestions`：命令自动补全
  - `zsh-syntax-highlighting`：语法高亮
- **推荐主题**：
  - `robbyrussell`（默认）
  - `agnoster`（更美观）
  - `powerlevel10k`（功能强大，需额外安装）

#### Oh-My-Zsh
- **作用**：zsh 配置管理框架
- **安装方式**：脚本安装
- **安装命令**：`sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`
- **需要 sudo**：否
- **需要重启**：否

---

## 其他工具

#### GParted
- **作用**：分区管理工具
- **安装方式**：apt 安装
- **安装命令**：`sudo apt install gparted -y`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`gparted`

#### Kazam
- **作用**：截图和录屏工具
- **安装方式**：apt 安装
- **安装命令**：`sudo apt install kazam -y`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`kazam`

---

## 安装建议

### 新系统初始化顺序
1. **基础工具**（Chrome、vscode 等）- 先安装常用工具
2. **开发环境**（conda、CUDA）- 配置开发环境
3. **终端工具**（zsh、terminator）- 提升效率
4. **重启系统** - 使驱动和环境变量生效

### 最小化安装
如果只需基本功能：
- **必装**：Chrome、vscode、conda
- **推荐**：terminator、zsh
- **可选**：其他工具根据需要

### 完整安装
适合算法工程师：
- **必装**：Chrome、vscode、conda、CUDA、cuDNN
- **推荐**：terminator、zsh + oh-my-zsh、kazam
- **可选**：Edge、Cursor、飞书、腾讯会议

---

## 常见问题

### Q: 如何选择 CUDA 版本？
A: 根据你的深度学习框架：
- TensorFlow 2.15+ → CUDA 12.1
- PyTorch 2.0+ → CUDA 11.8 或 12.1
- 最新 GPU (如 RTX 4090) → CUDA 12.x

### Q: conda 环境放在哪里？
A: 建议放在大容量磁盘：
```bash
# ~/.condarc
envs_dirs:
  - /media/your_disk/anaconda3/envs
```

### Q: 如何切换输入法？
A: 安装搜狗输入法后：
1. 系统设置 → 区域和语言 → 管理已安装的语言
2. 键盘输入法系统选择 fcitx
3. 重启系统
4. fcitx 配置中添加搜狗输入法

### Q: zsh 插件安装后不生效？
A: 确保在 `~/.zshrc` 中配置：
```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```
然后执行 `source ~/.zshrc`
