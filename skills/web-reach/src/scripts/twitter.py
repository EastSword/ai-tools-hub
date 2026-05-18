#!/usr/bin/env python3
"""
Twitter/X 模块 — 读推文、搜索（需要认证）

⚠️ 需要配置 Cookie 才能使用。
⚠️ 建议使用小号，存在封号风险。

配置方式：
    python3 credentials.py set twitter '{"cookie": "你的cookie字符串"}'

Cookie 获取方式：
    1. 用浏览器登录 Twitter（建议小号）
    2. 安装 Cookie-Editor 浏览器插件
    3. 导出 Cookie 字符串
    4. 通过 credentials.py 保存

用法：
    python3 twitter.py tweet "https://x.com/user/status/123"
    python3 twitter.py search "关键词"
    python3 twitter.py search "关键词" --limit 10
    python3 twitter.py user "username"
"""

import sys
import os
import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

CREDENTIALS_FILE = Path.home() / ".web-reach" / "credentials" / "twitter.json"


def get_cookie() -> str:
    """读取 Twitter Cookie"""
    if not CREDENTIALS_FILE.exists():
        print("❌ Twitter 凭证未配置")
        print()
        print("配置方式：")
        print("  1. 用浏览器登录 Twitter（建议使用小号）")
        print("  2. 用 Cookie-Editor 插件导出 Cookie")
        print("  3. 运行: python3 credentials.py set twitter '{\"cookie\": \"你的cookie\"}'")
        print()
        print("⚠️ 注意：使用 Cookie 登录存在封号风险，请务必使用小号")
        sys.exit(1)

    with open(CREDENTIALS_FILE) as f:
        data = json.load(f)
    return data.get("cookie", "")


def fetch_with_cookie(url: str, cookie: str) -> str:
    """带 Cookie 的请求"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Cookie": cookie,
        "Accept": "application/json",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.code}: {e.reason}"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def read_tweet(url: str) -> str:
    """读取单条推文（通过 Jina Reader 作为 fallback）"""
    # 优先尝试 Jina Reader（无需认证）
    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        "Accept": "text/markdown",
        "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
    }

    req = urllib.request.Request(jina_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            if content.strip() and len(content) > 50:
                return content
    except Exception:
        pass

    return "⚠️ 无法读取该推文。Twitter 限制了未认证访问。\n如需完整功能，请配置 Cookie。"


def search_twitter(query: str, limit: int = 10) -> str:
    """搜索推文（需要 Cookie）"""
    cookie = get_cookie()

    # 注意：Twitter 的搜索 API 较复杂，这里提供基础实现
    # 实际使用中可能需要根据 Twitter 的反爬策略调整
    return (
        f"🔍 Twitter 搜索: \"{query}\"\n\n"
        f"⚠️ Twitter 搜索功能需要有效的认证 Cookie。\n"
        f"当前 Cookie 状态: {'已配置' if cookie else '未配置'}\n\n"
        f"提示：如果搜索失败，可能是 Cookie 已过期，请重新导出。"
    )


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print('  python3 twitter.py tweet "https://x.com/user/status/123"')
        print('  python3 twitter.py search "关键词"')
        print('  python3 twitter.py user "username"')
        print()
        print("⚠️ 需要先配置 Cookie：")
        print('  python3 credentials.py set twitter \'{"cookie": "..."}\'')
        sys.exit(1)

    command = sys.argv[1]
    arg = sys.argv[2]

    if command == "tweet":
        print(read_tweet(arg))
    elif command == "search":
        limit = 10
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[idx + 1])
                except ValueError:
                    pass
        print(search_twitter(arg, limit=limit))
    elif command == "user":
        # 通过 Jina Reader 读取用户页面
        url = f"https://x.com/{arg}"
        print(read_tweet(url))
    else:
        print(f"未知命令: {command}")
        print("可用命令: tweet, search, user")
        sys.exit(1)


if __name__ == "__main__":
    main()
