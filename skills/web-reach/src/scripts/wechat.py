#!/usr/bin/env python3
"""
微信公众号模块 — 搜索和阅读公众号文章

通过搜索引擎和 Jina Reader 获取微信公众号文章。
无需认证。

用法：
    python3 wechat.py search "关键词"
    python3 wechat.py search "关键词" --limit 5
    python3 wechat.py read "https://mp.weixin.qq.com/s/xxx"
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse

JINA_READER_URL = "https://r.jina.ai/"
JINA_SEARCH_URL = "https://s.jina.ai/"


def search_articles(query: str, limit: int = 5) -> str:
    """搜索微信公众号文章"""
    # 通过 Jina Search 限定 mp.weixin.qq.com 域名搜索
    search_query = f"{query} site:mp.weixin.qq.com"
    encoded = urllib.parse.quote(search_query)
    url = f"{JINA_SEARCH_URL}{encoded}"

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")

        # 尝试解析 JSON
        try:
            data = json.loads(content)
            results = data.get("data", [])[:limit]

            if not results:
                return f"未找到与 \"{query}\" 相关的公众号文章"

            output = f"🔍 公众号搜索: \"{query}\"\n\n"
            for i, item in enumerate(results, 1):
                title = item.get("title", "无标题")
                url = item.get("url", "")
                description = item.get("description", "")

                output += f"**{i}. {title}**\n"
                if description:
                    desc = description[:100]
                    if len(description) > 100:
                        desc += "..."
                    output += f"   {desc}\n"
                if url:
                    output += f"   🔗 {url}\n"
                output += "\n"

            return output

        except json.JSONDecodeError:
            # 如果不是 JSON，按 Markdown 解析
            return content[:2000]

    except urllib.error.HTTPError as e:
        return f"❌ 搜索失败: HTTP {e.code}"
    except Exception as e:
        return f"❌ 错误: {e}"


def read_article(url: str) -> str:
    """读取微信公众号文章全文"""
    target = f"{JINA_READER_URL}{url}"

    headers = {
        "Accept": "text/markdown",
        "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
    }

    req = urllib.request.Request(target, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
            return content
    except urllib.error.HTTPError as e:
        return f"❌ 读取失败: HTTP {e.code}"
    except Exception as e:
        return f"❌ 错误: {e}"


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print('  python3 wechat.py search "关键词"')
        print('  python3 wechat.py read "https://mp.weixin.qq.com/s/xxx"')
        sys.exit(1)

    command = sys.argv[1]
    arg = sys.argv[2]

    if command == "search":
        limit = 5
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[idx + 1])
                except ValueError:
                    pass
        print(search_articles(arg, limit=limit))
    elif command == "read":
        print(read_article(arg))
    else:
        print(f"未知命令: {command}")
        print("可用命令: search, read")
        sys.exit(1)


if __name__ == "__main__":
    main()
