# Ubuntu 开发工具清单（中国网络优化版）

本文档列出所有可自动安装的工具，包括安装方式、权限要求和注意事项。

## 目录
- [基础工具](#基础工具)
- [开发环境](#开发环境)
- [终端工具](#终端工具)
- [其他工具](#其他工具)
- [国内镜像源配置](#国内镜像源配置)

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
- **下载地址**：`https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`microsoft-edge-stable`

### 编辑器类

#### Visual Studio Code
- **作用**：必装的代码编辑器
- **安装方式**：deb 包下载安装
- **下载地址**：
  - 官方：`https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64`
  - 国内镜像：`https://mirrors.huaweicloud.com/vscode/`（华为云镜像）
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`code`

#### Cursor
- **作用**：AI 代码编辑器，类似 VSCode 但集成 AI 功能
- **安装方式**：deb 包下载安装
- **下载地址**：`https://www.cursor.com/api/download?platform=linux&arch=x64`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`cursor`
- **注意**：可能需要代理下载

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
- **下载地址**：`https://www.todesk.com/download/linux.html`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`todesk`

#### 腾讯会议
- **作用**：视频会议工具
- **安装方式**：deb 包下载安装
- **下载地址**：`https://meeting.tencent.com/download-center.html`
- **需要 sudo**：是
- **需要重启**：否
- **包名**：`tencent-meeting`

#### WPS Office
- **作用**：办公文档套件
- **安装方式**：deb 包下载安装
- **下载地址**：`https://www.wps.cn/product/wpslinux`
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
- **安装步骤**：
  ```bash
  # 1. 安装 fcitx 框架
  sudo apt install fcitx fcitx-bin fcitx-table-all fcitx-config-gtk
  
  # 2. 安装搜狗输入法 deb 包
  sudo dpkg -i sogoupinyin_xxx_amd64.deb
  
  # 3. 修复依赖
  sudo apt install -f
  
  # 4. 重启系统
  sudo reboot
  
  # 5. 配置输入法
  im-config -n fcitx
  ```

### 代理工具

#### Clash Verge Rev
- **作用**：代理工具 GUI 版本，方便科学上网
- **安装方式**：deb 包下载安装
- **下载地址**：`https://github.com/clash-verge-rev/clash-verge-rev/releases`
- **版本选择**：
  - Ubuntu 22.04：选择 1.7 版本（`clash-verge_xxx_amd64.deb`）
  - Ubuntu 20.04：选择 1.6 版本
- **需要 sudo**：是
- **需要重启**：否
- **注意**：
  - 安装后需要导入订阅或配置文件
  - 建议配置为系统代理以加速 GitHub 等网站访问

---

## 开发环境

### Conda (Anaconda/Miniconda)
- **作用**：Python 环境管理工具，深度学习必备
- **安装方式**：脚本安装
- **下载地址**：
  - 清华镜像：`https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/`
  - 官方：`https://www.anaconda.com/download`
- **需要 sudo**：否（建议用户级安装）
- **需要重启**：否
- **国内镜像配置**：
  ```bash
  # 配置清华源
  conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  conda config --set show_channel_urls yes
  ```

### Docker
- **作用**：容器化部署工具
- **安装方式**：使用阿里云镜像安装
- **安装脚本**：`scripts/install_docker.py`
- **需要 sudo**：是
- **需要重启**：否
- **国内镜像配置**：
  ```bash
  # 使用脚本安装（自动配置阿里云镜像）
  python scripts/install_docker.py --install
  
  # 或手动配置镜像加速器
  sudo mkdir -p /etc/docker
  sudo tee /etc/docker/daemon.json <<-'EOF'
  {
    "registry-mirrors": ["https://2jgearuk.mirror.aliyuncs.com"]
  }
  EOF
  sudo systemctl daemon-reload
  sudo systemctl restart docker
  ```
- **可用镜像仓库**：
  - AtomHub：`https://hub.atomgit.com/`
  - 阿里云：`https://<your-id>.mirror.aliyuncs.com`（需注册获取专属地址）

### CUDA Toolkit
- **作用**：NVIDIA GPU 并行计算平台
- **安装方式**：deb 包安装
- **版本选择**：根据深度学习框架和显卡型号选择
- **下载地址**：
  - 官方：`https://developer.nvidia.com/cuda-downloads`
  - 国内镜像：可使用阿里云、清华镜像
- **需要 sudo**：是
- **需要重启**：是（驱动安装后）
- **详细步骤**：参考 [references/cuda_guide.md](cuda_guide.md)

### cuDNN
- **作用**：深度学习加速库
- **安装方式**：deb 包安装
- **版本要求**：需与 CUDA 版本匹配
- **下载地址**：`https://developer.nvidia.com/cudnn`（需要 NVIDIA 开发者账号）
- **需要 sudo**：是
- **需要重启**：否
- **详细步骤**：参考 [references/cuda_guide.md](cuda_guide.md)

### ROS (Robot Operating System)
- **作用**：机器人操作系统
- **安装方式**：一键安装脚本 (fishros)
- **安装命令**：
  ```bash
  wget http://fishros.com/install -O fishros
  sudo chmod +x ./fishros
  sudo ./fishros
  ```
- **需要 sudo**：是
- **需要重启**：否

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
- **安装脚本**：`scripts/setup_zsh.py`
- **需要 sudo**：是
- **需要重启**：否（但需注销重登录切换默认 shell）

#### Oh-My-Zsh
- **作用**：zsh 配置管理框架
- **安装方式**：脚本安装
- **国内镜像**：`https://gitee.com/shmhlsy/oh-my-zsh-install.sh`
- **安装命令**：
  ```bash
  # 使用国内镜像安装
  sh -c "$(curl -fsSL https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh)"
  ```
- **需要 sudo**：否

#### Zsh 插件
- **zsh-autosuggestions**：命令自动补全建议
  - GitHub：`https://github.com/zsh-users/zsh-autosuggestions`
  - Gitee 镜像：`https://gitee.com/zsh-users/zsh-autosuggestions`
  
- **zsh-syntax-highlighting**：命令语法高亮
  - GitHub：`https://github.com/zsh-users/zsh-syntax-highlighting`
  - Gitee 镜像：`https://gitee.com/Annihilater/zsh-syntax-highlighting`

**安装命令**：
```bash
# 安装 zsh-autosuggestions（Gitee 镜像）
git clone https://gitee.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# 安装 zsh-syntax-highlighting（Gitee 镜像）
git clone https://gitee.com/Annihilater/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

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

## 国内镜像源配置

### pip 镜像源

**临时使用**：
```bash
pip install package_name -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**永久配置**：
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**常用镜像源**：
- 清华：`https://pypi.tuna.tsinghua.edu.cn/simple`
- 阿里云：`https://mirrors.aliyun.com/pypi/simple/`
- 豆瓣：`https://pypi.douban.com/simple/`

### conda 镜像源

```bash
# 配置清华源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --set show_channel_urls yes
```

### apt 镜像源

**备份并修改 `/etc/apt/sources.list`**：
```bash
# 清华源（Ubuntu 22.04）
sudo sed -i 's@archive.ubuntu.com@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list
sudo sed -i 's@security.ubuntu.com@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list
sudo apt update
```

### Docker 镜像源

```bash
# 配置阿里云镜像加速器
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://2jgearuk.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 安装建议

### 新系统初始化顺序
1. **配置镜像源** - 使用国内镜像加速下载
2. **安装代理工具** - Clash Verge（如需访问 GitHub 等）
3. **基础工具** - Chrome、vscode 等
4. **开发环境** - conda、Docker、CUDA
5. **终端工具** - zsh、terminator
6. **重启系统** - 使驱动和环境变量生效

### 最小化安装
如果只需基本功能：
- **必装**：Chrome、vscode、conda、Docker
- **推荐**：terminator、zsh
- **可选**：其他工具根据需要

### 完整安装
适合算法工程师：
- **必装**：Chrome、vscode、conda、CUDA、cuDNN、Docker
- **推荐**：terminator、zsh + oh-my-zsh、kazam、Clash Verge
- **可选**：Edge、Cursor、飞书、腾讯会议

---

## 常见问题

### Q: GitHub 访问慢或无法访问怎么办？
A: 
1. 安装 Clash Verge 并配置代理
2. 或使用 Gitee 镜像（如 oh-my-zsh、zsh 插件）

### Q: Docker Hub 被封怎么办？
A: 
1. 配置阿里云等国内镜像加速器
2. 使用 AtomHub：`https://hub.atomgit.com/`

### Q: pip 安装包很慢？
A: 配置清华或阿里云 pip 镜像源

### Q: conda 创建环境很慢？
A: 配置清华 conda 镜像源
