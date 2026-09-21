#!/usr/bin/env python3
"""
Django 项目软著源代码合并工具
自动排除虚拟环境、依赖包、静态文件、迁移文件等
"""

import os
import sys
from pathlib import Path

# ==================== 配置区域 ====================
SOURCE_DIR = "."  # 项目根目录，可改为绝对路径如 "/path/to/your/project"
OUTPUT_FILE = "软著_Django源代码.txt"

# 排除的目录（Django 项目常见不需要提交的）
EXCLUDE_DIRS = {
    # 版本控制 & IDE
    '.git', '.svn', '.hg', '.idea', '.vscode', '.cursor',
    # Python 虚拟环境
    'venv', 'env', '.venv', '.env', 'virtualenv',
    # 依赖包
    'node_modules', 'bower_components',
    # Django 生成文件
    '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
    'staticfiles', 'media', 'collected_static',
    # 构建输出
    'dist', 'build', 'target', '.egg-info', '.eggs',
    # 日志
    'logs', '*.log',
    # 测试覆盖率
    'htmlcov', '.coverage',
    # 文档构建
    'docs/_build',
}

# 排除的文件模式
EXCLUDE_FILES = {
    # 配置文件（可能含敏感信息）
    '.env', '.env.local', '.env.production', '.env.development',
    # 密钥文件
    '*.pem', '*.key', '*.crt', '*.p12',
    # 数据库文件
    '*.db', '*.sqlite3', '*.sqlite',
    # 二进制 & 资源文件
    '*.png', '*.jpg', '*.jpeg', '*.gif', '*.ico', '*.svg',
    '*.woff', '*.woff2', '*.ttf', '*.eot',
    '*.mp3', '*.mp4', '*.wav', '*.pdf',
    # 压缩包
    '*.zip', '*.tar', '*.gz', '*.rar', '*.7z', '.md', '.txt',
    # 其他
    '*.min.js', '*.min.css',  # 压缩后的文件
    'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock',
    '.DS_Store', 'Thumbs.db',
}

# 包含的代码文件扩展名
INCLUDE_EXTS = {
    '.py',      # Python 主代码
    '.html',    # Django 模板
    '.css',     # 样式
    '.js',      # JavaScript
    '.sql',     # SQL 文件
    '.sh',      # Shell 脚本
    '.yaml', '.yml',  # 配置文件
    '.json',    # JSON 配置（排除 lock 文件）
    '.ini', '.cfg',   # 配置文件
    '.rst',     # 文档
}

# 最大文件大小（字节），超过则跳过
MAX_FILE_SIZE = 10000 * 1024  # 500KB


def should_exclude_dir(dirname):
    """判断目录是否应该排除"""
    return dirname in EXCLUDE_DIRS or dirname.startswith('.')

def should_exclude_file(filename):
    """判断文件是否应该排除"""
    # 检查完整文件名匹配
    if filename in EXCLUDE_FILES:
        return True
    # 检查通配符模式
    for pattern in EXCLUDE_FILES:
        if pattern.startswith('*') and filename.endswith(pattern[1:]):
            return True
    return False

def should_include_file(filepath):
    """判断文件是否应该包含在合并中"""
    ext = Path(filepath).suffix.lower()
    return ext in INCLUDE_EXTS

def get_file_lines(filepath):
    """安全读取文件内容"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read().splitlines()
        except UnicodeDecodeError:
            continue
    return None  # 无法解码

def merge_django_project():
    """合并 Django 项目源代码"""
    source_path = Path(SOURCE_DIR).resolve()
    output_path = source_path / OUTPUT_FILE

    if not source_path.exists():
        print(f"❌ 错误: 目录不存在: {source_path}")
        sys.exit(1)

    print(f"📁 项目目录: {source_path}")
    print(f"📄 输出文件: {output_path}")
    print("=" * 60)

    total_files = 0
    total_lines = 0
    skipped_files = []
    included_files = []

    with open(output_path, 'w', encoding='utf-8') as out:
        # 遍历项目目录
        for root, dirs, files in os.walk(source_path):
            root_path = Path(root)
            rel_root = root_path.relative_to(source_path)

            # 跳过排除的目录
            dirs[:] = [d for d in dirs if not should_exclude_dir(d)]

            for filename in sorted(files):
                filepath = root_path / filename
                rel_path = filepath.relative_to(source_path)

                # 排除输出文件自身
                if filename == OUTPUT_FILE:
                    continue

                # 排除特定文件
                if should_exclude_file(filename):
                    skipped_files.append((str(rel_path), "排除文件"))
                    continue

                # 检查扩展名
                if not should_include_file(filepath):
                    skipped_files.append((str(rel_path), "非代码文件"))
                    continue

                # 检查文件大小
                try:
                    file_size = filepath.stat().st_size
                    if file_size > MAX_FILE_SIZE:
                        skipped_files.append((str(rel_path), f"文件过大({file_size//1024}KB)"))
                        continue
                except:
                    continue

                # 读取文件内容
                lines = get_file_lines(filepath)
                if lines is None:
                    skipped_files.append((str(rel_path), "无法解码"))
                    continue

                # ========== 只写入代码内容，不加任何额外信息 ==========
                for line in lines:
                    out.write(line + "\n")

                total_files += 1
                total_lines += len(lines)
                included_files.append((str(rel_path), len(lines)))

                if total_files % 10 == 0:
                    print(f"  已处理 {total_files} 个文件...")

        # ========== 代码末尾添加文件清单统计 ==========
        out.write("\n")
        out.write("=" * 70 + "\n")
        out.write("/* 文件清单 */\n")
        out.write("=" * 70 + "\n\n")

        for fpath, lines in included_files:
            out.write(f"  {fpath:<60} ({lines:>5} 行)\n")

        out.write(f"\n  {'合计':<60} ({total_lines:>5} 行)\n")

    # 打印统计
    print("\n" + "=" * 60)
    print(f"✅ 合并完成！")
    print(f"   包含文件: {total_files} 个")
    print(f"   总行数: {total_lines} 行")
    print(f"   输出文件: {output_path}")
    print(f"   跳过文件: {len(skipped_files)} 个")

    if skipped_files:
        print("\n📋 跳过的文件:")
        for fpath, reason in skipped_files[:20]:  # 只显示前20个
            print(f"   - {fpath} ({reason})")
        if len(skipped_files) > 20:
            print(f"   ... 还有 {len(skipped_files) - 20} 个")

    # 软著页数估算（按每页50行）
    estimated_pages = (total_lines + 49) // 50
    print(f"\n📄 估算页数: 约 {estimated_pages} 页 (按每页50行)")

    if estimated_pages > 60:
        print("⚠️  超过60页，软著通常只需提交前30页+后30页")
        print("   请手动截取或使用脚本自动截取")

if __name__ == "__main__":
    merge_django_project()