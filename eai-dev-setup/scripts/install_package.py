#!/usr/bin/env python3
"""
Ubuntu 软件包安装脚本

功能：
- 支持 apt 安装
- 支持 deb 包安装（本地或 URL）
- 支持检查软件是否已安装
- 提供安装状态反馈
"""

import argparse
import subprocess
import os
import sys
import tempfile
import shutil
from pathlib import Path


def run_command(cmd, shell=False, check=True):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=600  # 10 分钟超时
        )
        if check and result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, "命令执行超时"
    except Exception as e:
        return False, str(e)


def check_package_installed(package_name):
    """检查包是否已安装"""
    success, output = run_command(
        ["dpkg", "-l", package_name],
        check=False
    )
    if success and package_name in output:
        return True
    return False


def check_command_exists(command):
    """检查命令是否存在"""
    return shutil.which(command) is not None


def install_with_apt(package_name, use_sudo=False):
    """使用 apt 安装包"""
    print(f"准备使用 apt 安装: {package_name}")
    
    # 先更新包列表
    update_cmd = ["apt", "update"]
    if use_sudo:
        update_cmd.insert(0, "sudo")
    
    print("更新包列表...")
    success, output = run_command(update_cmd, check=False)
    if not success:
        print(f"警告: 更新包列表失败: {output}")
    
    # 安装包
    install_cmd = ["apt", "install", "-y", package_name]
    if use_sudo:
        install_cmd.insert(0, "sudo")
    
    print(f"执行安装命令: {' '.join(install_cmd)}")
    success, output = run_command(install_cmd, check=False)
    
    if success:
        print(f"✓ {package_name} 安装成功")
        return True, "安装成功"
    else:
        print(f"✗ {package_name} 安装失败: {output}")
        return False, f"安装失败: {output}"


def install_from_deb_file(deb_path, use_sudo=False):
    """从本地 deb 文件安装"""
    if not os.path.exists(deb_path):
        return False, f"文件不存在: {deb_path}"
    
    print(f"准备从 deb 文件安装: {deb_path}")
    
    install_cmd = ["dpkg", "-i", deb_path]
    if use_sudo:
        install_cmd.insert(0, "sudo")
    
    success, output = run_command(install_cmd, check=False)
    
    if not success:
        # 尝试修复依赖
        print("尝试修复依赖...")
        fix_cmd = ["apt", "install", "-f", "-y"]
        if use_sudo:
            fix_cmd.insert(0, "sudo")
        
        run_command(fix_cmd, check=False)
        
        # 再次尝试安装
        success, output = run_command(install_cmd, check=False)
    
    if success:
        print(f"✓ 安装成功")
        return True, "安装成功"
    else:
        print(f"✗ 安装失败: {output}")
        return False, f"安装失败: {output}"


def download_file(url, dest_path):
    """下载文件"""
    try:
        import requests
        print(f"下载文件: {url}")
        
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r下载进度: {percent:.1f}%", end='', flush=True)
        
        print(f"\n✓ 下载完成: {dest_path}")
        return True, "下载成功"
    
    except Exception as e:
        print(f"\n✗ 下载失败: {str(e)}")
        return False, f"下载失败: {str(e)}"


def install_from_url(url, use_sudo=False, temp_dir=None):
    """从 URL 下载并安装 deb 包"""
    if temp_dir is None:
        temp_dir = tempfile.gettempdir()
    
    # 从 URL 提取文件名
    filename = url.split('/')[-1]
    if not filename.endswith('.deb'):
        filename = 'package.deb'
    
    deb_path = os.path.join(temp_dir, filename)
    
    # 下载文件
    success, msg = download_file(url, deb_path)
    if not success:
        return False, msg
    
    # 安装
    success, msg = install_from_deb_file(deb_path, use_sudo)
    
    # 清理临时文件
    try:
        os.remove(deb_path)
        print(f"已清理临时文件: {deb_path}")
    except:
        pass
    
    return success, msg


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Ubuntu 软件包安装工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用 apt 安装 terminator
  python install_package.py --package-name terminator --install-type apt --use-sudo
  
  # 从 URL 安装 Chrome
  python install_package.py --package-name google-chrome-stable --install-type url \\
      --deb-url "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" --use-sudo
  
  # 安装本地 deb 包
  python install_package.py --package-name myapp --install-type deb --deb-path /path/to/package.deb --use-sudo
        """
    )
    
    parser.add_argument(
        '--package-name',
        required=True,
        help='软件包名称'
    )
    
    parser.add_argument(
        '--install-type',
        choices=['apt', 'deb', 'url'],
        required=True,
        help='安装方式: apt(apt源), deb(本地deb文件), url(从URL下载deb)'
    )
    
    parser.add_argument(
        '--deb-path',
        help='本地 deb 文件路径 (install-type=deb 时必需)'
    )
    
    parser.add_argument(
        '--deb-url',
        help='deb 文件下载 URL (install-type=url 时必需)'
    )
    
    parser.add_argument(
        '--use-sudo',
        action='store_true',
        help='使用 sudo 权限执行安装'
    )
    
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='仅检查是否已安装，不执行安装'
    )
    
    args = parser.parse_args()
    
    # 检查模式
    if args.check_only:
        installed = check_package_installed(args.package_name)
        if installed:
            print(f"✓ {args.package_name} 已安装")
            return 0
        else:
            print(f"✗ {args.package_name} 未安装")
            return 1
    
    # 检查是否已安装
    if check_package_installed(args.package_name):
        print(f"✓ {args.package_name} 已安装，跳过")
        return 0
    
    # 根据 sudo 参数提示用户
    if args.use_sudo:
        print("\n" + "="*60)
        print("⚠️  警告: 此操作需要 sudo 权限")
        print("="*60)
        print(f"即将安装: {args.package_name}")
        print(f"安装方式: {args.install_type}")
        
        if args.install_type == 'url':
            print(f"下载地址: {args.deb_url}")
        
        response = input("\n是否继续? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("用户取消安装")
            return 1
    
    # 执行安装
    if args.install_type == 'apt':
        success, msg = install_with_apt(args.package_name, args.use_sudo)
    
    elif args.install_type == 'deb':
        if not args.deb_path:
            print("错误: install-type=deb 时必须指定 --deb-path")
            return 1
        success, msg = install_from_deb_file(args.deb_path, args.use_sudo)
    
    elif args.install_type == 'url':
        if not args.deb_url:
            print("错误: install-type=url 时必须指定 --deb-url")
            return 1
        success, msg = install_from_url(args.deb_url, args.use_sudo)
    
    else:
        print(f"错误: 不支持的安装类型: {args.install_type}")
        return 1
    
    if success:
        print(f"\n✓ 安装成功: {args.package_name}")
        return 0
    else:
        print(f"\n✗ 安装失败: {msg}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
