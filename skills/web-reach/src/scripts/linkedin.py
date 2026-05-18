#!/usr/bin/env python3
"""
LinkedIn 模块 — 读取公开页面

通过 Jina Reader 读取 LinkedIn 公开页面。
无需认证（仅限公开可见的内容）。

用法：
    python3 linkedin.py profile "https://linkedin.com/in/username"
    python3 linkedin.py company "https://linkedin.com/company/name"
    python3 linkedin.py read "https://linkedin.com/..."
"""

import sys
import urllib.request
import urllib.error

JINA_READER_URL = "https://r.jina.ai/"


def read_page(url: str) -> str:
    """通过 Jina Reader 读取 LinkedIn 页面"""
    if not url.startswith("http"):
        url = f"https://www.linkedin.com/in/{url}"

    target = f"{JINA_READER_URL}{url}"

    headers = {
        "Accept": "text/markdown",
        "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
    }

    req = urllib.request.Request(target, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
            if not content.strip():
                return "⚠️ 页面内容为空，可能需要登录才能查看"
            return content
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return "⚠️ 该页面需要登录才能查看"
        return f"❌ HTTP 错误 {e.code}: {e.reason}"
    except Exception as e:
        return f"❌ 错误: {e}"


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print('  python3 linkedin.py profile "https://linkedin.com/in/username"')
        print('  python3 linkedin.py company "https://linkedin.com/company/name"')
        print('  python3 linkedin.py read "https://linkedin.com/..."')
        sys.exit(1)

    command = sys.argv[1]
    url = sys.argv[2]

    if command in ("profile", "company", "read"):
        print(read_page(url))
    else:
        print(f"未知命令: {command}")
        print("可用命令: profile, company, read")
        sys.exit(1)


if __name__ == "__main__":
    main()
