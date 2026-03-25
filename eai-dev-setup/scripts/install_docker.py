#!/usr/bin/env python3
"""
Docker 安装脚本（中国网络优化版）

功能：
- 使用阿里云镜像安装 Docker
- 配置国内镜像加速器
- 配置用户权限
- 支持完全卸载旧版本
"""

import argparse
import os
import sys
import subprocess
import json


def run_command(cmd, shell=False, check=True, use_sudo=False):
    """执行命令"""
    if use_sudo and not cmd.startswith("sudo"):
        if isinstance(cmd, list):
            cmd = ["sudo"] + cmd
        else:
            cmd = f"sudo {cmd}"
    
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=300
        )
        if check and result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, "命令执行超时"
    except Exception as e:
        return False, str(e)


def check_docker_installed():
    """检查 Docker 是否已安装"""
    success, output = run_command(["docker", "--version"], check=False)
    return success


def remove_old_docker(use_sudo=True):
    """卸载旧版本 Docker"""
    print("检查并卸载旧版本 Docker...")
    
    old_packages = [
        "docker", "docker-engine", "docker.io", "containerd", "runc"
    ]
    
    cmd = ["apt", "remove", "-y"] + old_packages
    success, output = run_command(cmd, use_sudo=use_sudo, check=False)
    
    if success:
        print("✓ 已清理旧版本")
    else:
        print("⚠️  清理旧版本时出现警告（可能未安装旧版本）")
    
    return True


def install_dependencies(use_sudo=True):
    """安装依赖包"""
    print("安装依赖包...")
    
    deps = ["ca-certificates", "curl", "gnupg", "lsb-release"]
    cmd = ["apt", "install", "-y"] + deps
    
    success, output = run_command(cmd, use_sudo=use_sudo)
    
    if success:
        print("✓ 依赖包安装成功")
        return True
    else:
        print(f"✗ 依赖包安装失败: {output}")
        return False


def add_aliyun_key(use_sudo=True):
    """添加阿里云 Docker GPG 密钥"""
    print("添加阿里云 Docker GPG 密钥...")
    
    # 创建密钥目录
    keyrings_dir = "/etc/apt/keyrings"
    run_command(["mkdir", "-p", keyrings_dir], use_sudo=use_sudo, check=False)
    
    # 下载并添加密钥（使用阿里云镜像）
    key_url = "https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg"
    
    success, output = run_command(
        f"curl -fsSL {key_url} | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
        shell=True,
        use_sudo=False
    )
    
    if success or os.path.exists("/etc/apt/keyrings/docker.gpg"):
        print("✓ GPG 密钥添加成功")
        return True
    else:
        print(f"✗ GPG 密钥添加失败: {output}")
        return False


def add_docker_repository(use_sudo=True):
    """添加 Docker 软件源（阿里云镜像）"""
    print("添加 Docker 软件源（阿里云镜像）...")
    
    # 获取 Ubuntu 版本代号
    success, codename = run_command(["lsb_release", "-cs"])
    if not success:
        codename = "jammy"  # 默认 Ubuntu 22.04
    
    codename = codename.strip()
    
    # 添加软件源
    repo_content = f"deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu {codename} stable"
    
    # 写入源文件
    success, output = run_command(
        f'echo "{repo_content}" | sudo tee /etc/apt/sources.list.d/docker.list',
        shell=True,
        use_sudo=False
    )
    
    if success:
        print(f"✓ Docker 软件源添加成功（{codename}）")
        return True
    else:
        print(f"✗ Docker 软件源添加失败: {output}")
        return False


def install_docker_ce(use_sudo=True):
    """安装 Docker CE"""
    print("安装 Docker CE...")
    
    # 更新包列表
    print("更新包列表...")
    run_command(["apt", "update"], use_sudo=use_sudo, check=False)
    
    # 安装 Docker
    packages = ["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"]
    cmd = ["apt", "install", "-y"] + packages
    
    success, output = run_command(cmd, use_sudo=use_sudo)
    
    if success:
        print("✓ Docker CE 安装成功")
        return True
    else:
        print(f"✗ Docker CE 安装失败: {output}")
        return False


def configure_mirror_accelerator(mirror_url=None, use_sudo=True):
    """配置 Docker 镜像加速器"""
    print("配置 Docker 镜像加速器...")
    
    if mirror_url is None:
        # 默认使用阿里云公共镜像
        mirror_url = "https://2jgearuk.mirror.aliyuncs.com"
    
    daemon_json = {
        "registry-mirrors": [mirror_url]
    }
    
    # 创建配置目录
    run_command(["mkdir", "-p", "/etc/docker"], use_sudo=use_sudo, check=False)
    
    # 写入配置
    config_content = json.dumps(daemon_json, indent=2)
    success, output = run_command(
        f'echo \'{config_content}\' | sudo tee /etc/docker/daemon.json',
        shell=True,
        use_sudo=False
    )
    
    if success:
        print(f"✓ 镜像加速器配置成功: {mirror_url}")
        return True
    else:
        print(f"✗ 镜像加速器配置失败: {output}")
        return False


def add_user_to_docker_group():
    """将当前用户添加到 docker 组"""
    print("配置用户权限...")
    
    username = os.environ.get("USER", "root")
    
    success, output = run_command(
        ["usermod", "-aG", "docker", username],
        use_sudo=True,
        check=False
    )
    
    if success or "already" in output.lower():
        print(f"✓ 已将用户 {username} 添加到 docker 组")
        print("⚠️  需要注销并重新登录后生效，或执行 'newgrp docker'")
        return True
    else:
        print(f"⚠️  添加用户到 docker 组失败: {output}")
        return False


def start_docker_service(use_sudo=True):
    """启动 Docker 服务"""
    print("启动 Docker 服务...")
    
    # 启动服务
    run_command(["systemctl", "start", "docker"], use_sudo=use_sudo, check=False)
    
    # 设置开机自启
    run_command(["systemctl", "enable", "docker"], use_sudo=use_sudo, check=False)
    
    # 检查状态
    success, output = run_command(["systemctl", "status", "docker"], use_sudo=use_sudo, check=False)
    
    if "active (running)" in output or success:
        print("✓ Docker 服务已启动")
        return True
    else:
        print("⚠️  Docker 服务状态检查失败")
        return False


def verify_docker():
    """验证 Docker 安装"""
    print("\n验证 Docker 安装...")
    
    # 检查版本
    success, output = run_command(["docker", "--version"], check=False)
    if success:
        print(f"Docker 版本: {output.strip()}")
    
    # 测试运行
    print("运行测试镜像 hello-world...")
    success, output = run_command(["docker", "run", "--rm", "hello-world"], check=False)
    
    if success or "Hello from Docker" in output:
        print("✓ Docker 运行正常")
        return True
    else:
        print(f"⚠️  Docker 测试失败，可能需要配置镜像加速器: {output}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Docker 安装工具（中国网络优化版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整安装 Docker（使用阿里云镜像）
  python install_docker.py --install
  
  # 仅配置镜像加速器
  python install_docker.py --config-mirror --mirror-url "https://your-mirror.mirror.aliyuncs.com"
  
  # 卸载旧版本
  python install_docker.py --remove-old
        """
    )
    
    parser.add_argument(
        '--install',
        action='store_true',
        help='完整安装 Docker'
    )
    
    parser.add_argument(
        '--remove-old',
        action='store_true',
        help='卸载旧版本 Docker'
    )
    
    parser.add_argument(
        '--config-mirror',
        action='store_true',
        help='配置镜像加速器'
    )
    
    parser.add_argument(
        '--mirror-url',
        help='镜像加速器 URL（默认使用阿里云公共镜像）'
    )
    
    parser.add_argument(
        '--no-user-group',
        action='store_true',
        help='不将当前用户添加到 docker 组'
    )
    
    parser.add_argument(
        '--verify',
        action='store_true',
        help='仅验证 Docker 安装'
    )
    
    args = parser.parse_args()
    
    # 检查是否已安装
    if check_docker_installed() and args.install:
        print("✓ Docker 已安装，跳过安装步骤")
        if not args.config_mirror and not args.verify:
            return 0
    
    # 仅验证
    if args.verify:
        return 0 if verify_docker() else 1
    
    # 卸载旧版本
    if args.remove_old:
        print("\n" + "="*60)
        print("⚠️  警告: 此操作需要 sudo 权限")
        print("="*60)
        print("即将卸载旧版本 Docker")
        
        response = input("\n是否继续? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("用户取消操作")
            return 1
        
        remove_old_docker()
        return 0
    
    # 完整安装
    if args.install:
        print("\n" + "="*60)
        print("⚠️  警告: 此操作需要 sudo 权限")
        print("="*60)
        print("即将安装 Docker（使用阿里云镜像）")
        
        response = input("\n是否继续? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("用户取消操作")
            return 1
        
        success = True
        
        # 1. 卸载旧版本
        remove_old_docker()
        
        # 2. 安装依赖
        if not install_dependencies():
            success = False
        
        # 3. 添加 GPG 密钥
        if success and not add_aliyun_key():
            success = False
        
        # 4. 添加软件源
        if success and not add_docker_repository():
            success = False
        
        # 5. 安装 Docker
        if success and not install_docker_ce():
            success = False
        
        # 6. 配置镜像加速器
        if success:
            configure_mirror_accelerator(args.mirror_url)
        
        # 7. 启动服务
        if success:
            start_docker_service()
        
        # 8. 添加用户到 docker 组
        if success and not args.no_user_group:
            add_user_to_docker_group()
        
        # 9. 验证安装
        if success:
            verify_docker()
        
        if success:
            print("\n" + "="*60)
            print("✓ Docker 安装完成")
            print("="*60)
            print("镜像加速器已配置")
            if not args.no_user_group:
                print("请执行 'newgrp docker' 或重新登录以使用户组生效")
            return 0
        else:
            print("\n✗ Docker 安装过程中出现错误")
            return 1
    
    # 仅配置镜像加速器
    if args.config_mirror:
        print("\n" + "="*60)
        print("⚠️  警告: 此操作需要 sudo 权限")
        print("="*60)
        
        response = input("\n是否继续? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("用户取消操作")
            return 1
        
        if configure_mirror_accelerator(args.mirror_url):
            # 重启 Docker 服务
            run_command(["systemctl", "daemon-reload"], use_sudo=True)
            run_command(["systemctl", "restart", "docker"], use_sudo=True)
            print("✓ 镜像加速器配置完成，Docker 服务已重启")
            return 0
        else:
            return 1
    
    # 无参数时显示帮助
    parser.print_help()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
