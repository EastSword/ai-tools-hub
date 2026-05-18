#!/usr/bin/env python3
"""
凭证管理模块 — 安全存储和读取认证信息

凭证统一存放在 ~/.web-reach/credentials/ 目录下，文件权限 600。
每个平台一个 JSON 文件。

用法：
    python3 credentials.py set twitter '{"cookie": "..."}'
    python3 credentials.py get twitter
    python3 credentials.py list
    python3 credentials.py remove twitter
"""

import sys
import os
import json
from pathlib import Path

CREDENTIALS_DIR = Path.home() / ".web-reach" / "credentials"


def ensure_dir():
    """确保凭证目录存在且权限正确"""
    CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(CREDENTIALS_DIR, 0o700)
    os.chmod(CREDENTIALS_DIR.parent, 0o700)


def set_credential(platform: str, data: str):
    """保存凭证"""
    ensure_dir()

    # 验证是合法 JSON
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError:
        print(f"❌ 凭证格式错误，请提供合法的 JSON")
        sys.exit(1)

    filepath = CREDENTIALS_DIR / f"{platform}.json"
    with open(filepath, "w") as f:
        json.dump(parsed, f, indent=2)
    os.chmod(filepath, 0o600)

    print(f"✅ {platform} 凭证已保存到 {filepath}")
    print(f"   文件权限: 600 (仅所有者可读写)")


def get_credential(platform: str) -> dict:
    """读取凭证"""
    filepath = CREDENTIALS_DIR / f"{platform}.json"
    if not filepath.exists():
        return None

    with open(filepath) as f:
        return json.load(f)


def list_credentials():
    """列出已配置的凭证"""
    ensure_dir()
    files = list(CREDENTIALS_DIR.glob("*.json"))

    if not files:
        print("暂无已配置的凭证")
        print(f"\n凭证目录: {CREDENTIALS_DIR}")
        return

    print("📋 **已配置的凭证**\n")
    for f in sorted(files):
        platform = f.stem
        size = f.stat().st_size
        mode = oct(f.stat().st_mode)[-3:]
        print(f"  • {platform} ({size} bytes, 权限: {mode})")

    print(f"\n凭证目录: {CREDENTIALS_DIR}")


def remove_credential(platform: str):
    """删除凭证"""
    filepath = CREDENTIALS_DIR / f"{platform}.json"
    if filepath.exists():
        filepath.unlink()
        print(f"✅ {platform} 凭证已删除")
    else:
        print(f"⚠️ {platform} 凭证不存在")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 credentials.py list")
        print('  python3 credentials.py set <平台> \'{"cookie": "..."}\'')
        print("  python3 credentials.py get <平台>")
        print("  python3 credentials.py remove <平台>")
        print()
        print("支持的平台: twitter, xiaohongshu, xueqiu")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_credentials()
    elif command == "set":
        if len(sys.argv) < 4:
            print("请提供平台名和凭证 JSON")
            sys.exit(1)
        set_credential(sys.argv[2], sys.argv[3])
    elif command == "get":
        if len(sys.argv) < 3:
            print("请提供平台名")
            sys.exit(1)
        cred = get_credential(sys.argv[2])
        if cred:
            print(f"✅ {sys.argv[2]} 凭证已配置")
            # 不输出实际内容，只确认存在
            print(f"   字段: {', '.join(cred.keys())}")
        else:
            print(f"❌ {sys.argv[2]} 凭证未配置")
    elif command == "remove":
        if len(sys.argv) < 3:
            print("请提供平台名")
            sys.exit(1)
        remove_credential(sys.argv[2])
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
