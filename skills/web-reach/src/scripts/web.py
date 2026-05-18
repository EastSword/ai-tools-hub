#!/usr/bin/env python3
"""
Web 模块 — 读取任意公开网页内容

通过 Jina Reader API 获取网页的清洁 Markdown 文本。
无需 API Key，免费使用。

用法：
    python3 web.py read "https://example.com"
    python3 web.py read "https://example.com" --raw
"""

import sys
import json
import urllib.request
import urllib.error

JINA_READER_URL = "https://r.jina.ai/"


def read_url(url: str, raw: bool = False) -> str:
    """通过 Jina Reader 读取网页内容"""
    target = f"{JINA_READER_URL}{url}"

    headers = {
        "Accept": "text/markdown" if not raw else "text/plain",
        "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
    }

    req = urllib.request.Request(target, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
            return content
    except urllib.error.HTTPError as e:
        return f"❌ HTTP 错误 {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return f"❌ 网络错误: {e.reason}"
    except Exception as e:
        return f"❌ 未知错误: {e}"


def main():
    if len(sys.argv) < 3:
        print("用法: python3 web.py read <URL> [--raw]")
        print()
        print("示例:")
        print('  python3 web.py read "https://example.com"')
        sys.exit(1)

    command = sys.argv[1]
    url = sys.argv[2]
    raw = "--raw" in sys.argv

    if command == "read":
        result = read_url(url, raw=raw)
        print(result)
    else:
        print(f"未知命令: {command}")
        print("可用命令: read")
        sys.exit(1)


if __name__ == "__main__":
    main()
