#!/usr/bin/env python3
"""
小红书模块 — 搜索和阅读笔记（需要认证）

⚠️ 需要配置 Cookie 才能使用。
⚠️ 建议使用小号，存在封号风险。

配置方式：
    python3 credentials.py set xiaohongshu '{"cookie": "你的cookie字符串"}'

Cookie 获取方式：
    1. 用浏览器登录小红书网页版（建议小号）
    2. 安装 Cookie-Editor 浏览器插件
    3. 导出 Cookie 字符串
    4. 通过 credentials.py 保存

用法：
    python3 xiaohongshu.py search "关键词"
    python3 xiaohongshu.py read "笔记URL"
"""

import sys
import os
import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

CREDENTIALS_FILE = Path.home() / ".web-reach" / "credentials" / "xiaohongshu.json"
JINA_READER_URL = "https://r.jina.ai/"


def get_cookie() -> str:
    """读取小红书 Cookie"""
    if not CREDENTIALS_FILE.exists():
        print("❌ 小红书凭证未配置")
        print()
        print("配置方式：")
        print("  1. 用浏览器登录小红书网页版（建议使用小号）")
        print("  2. 用 Cookie-Editor 插件导出 Cookie")
        print("  3. 运行: python3 credentials.py set xiaohongshu '{\"cookie\": \"你的cookie\"}'")
        print()
        print("⚠️ 注意：使用 Cookie 登录存在封号风险，请务必使用小号")
        sys.exit(1)

    with open(CREDENTIALS_FILE) as f:
        data = json.load(f)
    return data.get("cookie", "")


def search_notes(query: str, limit: int = 10) -> str:
    """搜索小红书笔记"""
    cookie = get_cookie()

    # 通过小红书搜索 API
    encoded = urllib.parse.quote(query)
    url = f"https://edith.xiaohongshu.com/api/sns/web/v1/search/notes?keyword={encoded}&page=1&page_size={limit}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Cookie": cookie,
        "Origin": "https://www.xiaohongshu.com",
        "Referer": "https://www.xiaohongshu.com/",
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if data.get("code") != 0:
            return f"❌ 搜索失败: {data.get('msg', '未知错误')}（Cookie 可能已过期）"

        items = data.get("data", {}).get("items", [])
        if not items:
            return f"未找到与 \"{query}\" 相关的笔记"

        output = f"🔍 小红书搜索: \"{query}\"\n\n"
        for i, item in enumerate(items[:limit], 1):
            note = item.get("note_card", {})
            title = note.get("display_title", "无标题")
            user = note.get("user", {}).get("nickname", "")
            likes = note.get("interact_info", {}).get("liked_count", "0")
            note_id = note.get("note_id", "")

            output += f"**{i}. {title}**\n"
            output += f"   @{user} | ❤️ {likes}\n"
            if note_id:
                output += f"   🔗 https://www.xiaohongshu.com/explore/{note_id}\n"
            output += "\n"

        return output

    except urllib.error.HTTPError as e:
        return f"❌ 请求失败: HTTP {e.code}（Cookie 可能已过期）"
    except Exception as e:
        return f"❌ 错误: {e}"


def read_note(url: str) -> str:
    """读取小红书笔记内容"""
    # 优先尝试 Jina Reader
    target = f"{JINA_READER_URL}{url}"
    headers = {
        "Accept": "text/markdown",
        "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
    }

    req = urllib.request.Request(target, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
            if content.strip() and len(content) > 50:
                return content
    except Exception:
        pass

    return "⚠️ 无法读取该笔记。小红书限制了未认证访问。"


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print('  python3 xiaohongshu.py search "关键词"')
        print('  python3 xiaohongshu.py read "https://www.xiaohongshu.com/explore/xxx"')
        print()
        print("⚠️ 需要先配置 Cookie：")
        print('  python3 credentials.py set xiaohongshu \'{"cookie": "..."}\'')
        sys.exit(1)

    command = sys.argv[1]
    arg = sys.argv[2]

    if command == "search":
        limit = 10
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[idx + 1])
                except ValueError:
                    pass
        print(search_notes(arg, limit=limit))
    elif command == "read":
        print(read_note(arg))
    else:
        print(f"未知命令: {command}")
        print("可用命令: search, read")
        sys.exit(1)


if __name__ == "__main__":
    main()
