#!/usr/bin/env python3
"""
Zsh 和 Oh-My-Zsh 配置脚本（中国网络优化版）

功能：
- 安装 zsh
- 安装 oh-my-zsh（支持国内 Gitee 镜像）
- 安装常用插件（支持国内 Gitee 镜像）
- 配置主题
- 设置为默认 shell
"""

import argparse
import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, shell=False, check=True, input_text=None):
    """执行命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=300,
            input=input_text
        )
        if check and result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except subprocess.TimeoutExpired:
        return False, "命令执行超时"
    except Exception as e:
        return False, str(e)


def check_zsh_installed():
    """检查 zsh 是否已安装"""
    return shutil.which('zsh') is not None


def check_oh_my_zsh_installed():
    """检查 oh-my-zsh 是否已安装"""
    oh_my_zsh_dir = os.path.expanduser("~/.oh-my-zsh")
    return os.path.exists(oh_my_zsh_dir)


def install_zsh(use_sudo=False):
    """安装 zsh"""
    print("准备安装 zsh...")
    
    if check_zsh_installed():
        print("✓ zsh 已安装")
        return True, "zsh 已安装"
    
    # 更新包列表
    update_cmd = ["apt", "update"]
    if use_sudo:
        update_cmd.insert(0, "sudo")
    
    print("更新包列表...")
    run_command(update_cmd, check=False)
    
    # 安装 zsh
    install_cmd = ["apt", "install", "-y", "zsh"]
    if use_sudo:
        install_cmd.insert(0, "sudo")
    
    print(f"执行安装: {' '.join(install_cmd)}")
    success, output = run_command(install_cmd, check=False)
    
    if success:
        print("✓ zsh 安装成功")
        return True, "安装成功"
    else:
        print(f"✗ zsh 安装失败: {output}")
        return False, f"安装失败: {output}"


def install_oh_my_zsh(use_china_mirror=True):
    """安装 oh-my-zsh，支持国内镜像"""
    print("准备安装 oh-my-zsh...")
    
    if check_oh_my_zsh_installed():
        print("✓ oh-my-zsh 已安装")
        return True, "oh-my-zsh 已安装"
    
    # 国内 Gitee 镜像（推荐）
    if use_china_mirror:
        print("使用 Gitee 国内镜像安装...")
        install_url = "https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh"
        
        success, output = run_command(
            ["sh", "-c", f"curl -fsSL {install_url}"],
            shell=True,
            check=False,
            input_text="n\n"
        )
        
        if success or check_oh_my_zsh_installed():
            print("✓ oh-my-zsh 安装成功（Gitee 镜像）")
            return True, "安装成功"
    
    # 官方 GitHub 源（备选）
    print("尝试官方 GitHub 源...")
    install_url = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    
    # 方法1: 使用 wget
    success, output = run_command(
        ["sh", "-c", f"wget {install_url} -O - | sh"],
        shell=True,
        check=False,
        input_text="n\n"
    )
    
    if success or check_oh_my_zsh_installed():
        print("✓ oh-my-zsh 安装成功")
        return True, "安装成功"
    
    # 方法2: 使用 curl
    success, output = run_command(
        ["sh", "-c", f"curl -fsSL {install_url}"],
        shell=True,
        check=False,
        input_text="n\n"
    )
    
    if check_oh_my_zsh_installed():
        print("✓ oh-my-zsh 安装成功")
        return True, "安装成功"
    
    print(f"✗ oh-my-zsh 安装失败: {output}")
    return False, f"安装失败: {output}"


def install_zsh_plugins(plugins, use_china_mirror=True):
    """安装 zsh 插件，支持国内镜像"""
    print(f"准备安装插件: {plugins}")
    
    zsh_custom = os.path.expanduser("~/.oh-my-zsh/custom/plugins")
    os.makedirs(zsh_custom, exist_ok=True)
    
    # 插件源映射（支持国内镜像）
    plugin_map = {
        "zsh-autosuggestions": {
            "github": "https://github.com/zsh-users/zsh-autosuggestions",
            "gitee": "https://gitee.com/zsh-users/zsh-autosuggestions"
        },
        "zsh-syntax-highlighting": {
            "github": "https://github.com/zsh-users/zsh-syntax-highlighting",
            "gitee": "https://gitee.com/Annihilater/zsh-syntax-highlighting"
        }
    }
    
    installed = []
    for plugin in plugins:
        if plugin not in plugin_map:
            print(f"⚠️  未知插件: {plugin}，跳过")
            continue
        
        plugin_dir = os.path.join(zsh_custom, plugin)
        
        if os.path.exists(plugin_dir):
            print(f"✓ 插件已存在: {plugin}")
            installed.append(plugin)
            continue
        
        # 优先使用国内镜像
        clone_url = None
        if use_china_mirror:
            clone_url = plugin_map[plugin].get("gitee")
        
        # 尝试克隆
        sources = []
        if use_china_mirror and "gitee" in plugin_map[plugin]:
            sources.append(("Gitee", plugin_map[plugin]["gitee"]))
        if "github" in plugin_map[plugin]:
            sources.append(("GitHub", plugin_map[plugin]["github"]))
        
        for source_name, url in sources:
            print(f"尝试从 {source_name} 克隆 {plugin}...")
            success, output = run_command(
                ["git", "clone", url, plugin_dir],
                check=False
            )
            
            if success:
                print(f"✓ 插件安装成功: {plugin}（{source_name}）")
                installed.append(plugin)
                break
            else:
                print(f"✗ 从 {source_name} 克隆失败: {output}")
        
        if plugin not in installed:
            print(f"✗ 插件安装失败: {plugin}")
    
    return installed


def configure_zshrc(plugins, theme="robbyrussell"):
    """配置 .zshrc"""
    zshrc_path = os.path.expanduser("~/.zshrc")
    
    if not os.path.exists(zshrc_path):
        # 复制模板
        template_path = os.path.expanduser("~/.oh-my-zsh/templates/zshrc.zsh-template")
        if os.path.exists(template_path):
            shutil.copy2(template_path, zshrc_path)
            print(f"✓ 已创建 .zshrc")
        else:
            print(f"✗ 找不到模板文件")
            return False
    
    # 读取当前配置
    with open(zshrc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改主题
    import re
    content = re.sub(
        r'ZSH_THEME="[^"]*"',
        f'ZSH_THEME="{theme}"',
        content
    )
    print(f"✓ 已设置主题: {theme}")
    
    # 修改插件
    if plugins:
        plugins_str = ' '.join(plugins)
        content = re.sub(
            r'plugins=\([^)]*\)',
            f'plugins=({plugins_str})',
            content
        )
        print(f"✓ 已配置插件: {plugins_str}")
    
    # 写回文件
    with open(zshrc_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True


def set_default_shell():
    """设置 zsh 为默认 shell"""
    current_shell = os.environ.get('SHELL', '')
    
    if 'zsh' in current_shell:
        print("✓ zsh 已是默认 shell")
        return True, "已是默认 shell"
    
    zsh_path = shutil.which('zsh')
    if not zsh_path:
        return False, "找不到 zsh 路径"
    
    print(f"准备设置默认 shell 为: {zsh_path}")
    print("⚠️  此操作需要输入密码")
    
    success, output = run_command(
        ["chsh", "-s", zsh_path],
        check=False
    )
    
    if success or "password" in output.lower():
        print("✓ 已设置 zsh 为默认 shell")
        print("⚠️  需要注销并重新登录后生效")
        return True, "设置成功"
    
    print(f"✗ 设置失败: {output}")
    return False, f"设置失败: {output}"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Zsh 和 Oh-My-Zsh 配置工具（中国网络优化版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整安装（使用国内镜像）
  python setup_zsh.py --use-sudo --install-oh-my-zsh --china-mirror
  
  # 安装并配置插件（国内镜像）
  python setup_zsh.py --use-sudo --install-oh-my-zsh --china-mirror \\
      --plugins "git zsh-autosuggestions zsh-syntax-highlighting" --theme agnoster
  
  # 使用官方源安装
  python setup_zsh.py --use-sudo --install-oh-my-zsh --no-china-mirror
  
  # 设置为默认 shell
  python setup_zsh.py --set-default-shell
        """
    )
    
    parser.add_argument(
        '--use-sudo',
        action='store_true',
        help='使用 sudo 权限安装 zsh'
    )
    
    parser.add_argument(
        '--install-zsh',
        action='store_true',
        help='安装 zsh'
    )
    
    parser.add_argument(
        '--install-oh-my-zsh',
        action='store_true',
        help='安装 oh-my-zsh'
    )
    
    parser.add_argument(
        '--plugins',
        help='插件列表 (空格分隔)'
    )
    
    parser.add_argument(
        '--theme',
        default='robbyrussell',
        help='主题名称 (默认: robbyrussell)'
    )
    
    parser.add_argument(
        '--china-mirror',
        action='store_true',
        default=True,
        help='使用国内镜像源 (默认启用)'
    )
    
    parser.add_argument(
        '--no-china-mirror',
        action='store_true',
        help='不使用国内镜像源'
    )
    
    parser.add_argument(
        '--set-default-shell',
        action='store_true',
        help='设置 zsh 为默认 shell'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='执行完整配置 (安装 zsh, oh-my-zsh, 插件, 设置默认 shell)'
    )
    
    args = parser.parse_args()
    
    # 处理镜像选项
    use_china_mirror = not args.no_china_mirror
    
    # 如果指定 --all，则启用所有选项
    if args.all:
        args.install_zsh = True
        args.install_oh_my_zsh = True
        args.set_default_shell = True
        if not args.plugins:
            args.plugins = "git zsh-autosuggestions zsh-syntax-highlighting"
    
    success = True
    
    # 提示 sudo 权限
    if args.use_sudo and args.install_zsh:
        print("\n" + "="*60)
        print("⚠️  警告: 此操作需要 sudo 权限")
        print("="*60)
        print("即将安装: zsh")
        
        response = input("\n是否继续? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("用户取消操作")
            return 1
    
    # 安装 zsh
    if args.install_zsh:
        if not install_zsh(args.use_sudo)[0]:
            success = False
    
    # 安装 oh-my-zsh
    if args.install_oh_my_zsh:
        if not install_oh_my_zsh(use_china_mirror)[0]:
            success = False
    
    # 安装插件
    if args.plugins:
        plugins = args.plugins.split()
        installed = install_zsh_plugins(plugins, use_china_mirror)
        
        if installed:
            if not configure_zshrc(installed, args.theme):
                success = False
    
    # 设置默认 shell
    if args.set_default_shell:
        if not set_default_shell()[0]:
            success = False
    
    if success:
        print("\n✓ 配置完成")
        if args.set_default_shell:
            print("⚠️  需要注销并重新登录后生效")
        else:
            print("💡 执行 'zsh' 或重新打开终端体验新配置")
        return 0
    else:
        print("\n✗ 配置过程中出现错误")
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
