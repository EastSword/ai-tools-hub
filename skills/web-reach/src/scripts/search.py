#!/usr/bin/env python3
"""
Search 模块 — 全网搜索

通过 Jina Search API 进行语义搜索。
无需 API Key，免费使用。

用法：
    python3 search.py query "搜索关键词"
    python3 search.py query "搜索关键词" --limit 5
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse

JINA_SEARCH_URL = "https://s.jina.ai/"


def search(query: str, limit: int = 5) -> str:
    """通过 Jina Search 搜索"""
    encoded_query = urllib.parse.quote(query)
    target = f"{JINA_SEARCH_URL}{encoded_query}"

    headers = {
        "Accept": "text/markdown",
        "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
    }

    req = urllib.request.Request(target, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
            # 限制返回结果数量
            lines = content.split("\n")
            result_count = 0
            output_lines = []
            for line in lines:
                output_lines.append(line)
                if line.startswith("# ") or line.startswith("## "):
                    result_count += 1
                    if result_count > limit:
                        break
            return "\n".join(output_lines)
    except urllib.error.HTTPError as e:
        return f"❌ HTTP 错误 {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return f"❌ 网络错误: {e.reason}"
    except Exception as e:
        return f"❌ 未知错误: {e}"


def main():
    if len(sys.argv) < 3:
        print("用法: python3 search.py query <关键词> [--limit N]")
        print()
        print("示例:")
        print('  python3 search.py query "LLM framework comparison"')
        print('  python3 search.py query "kubernetes security" --limit 10')
        sys.exit(1)

    command = sys.argv[1]
    query = sys.argv[2]

    limit = 5
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            try:
                limit = int(sys.argv[idx + 1])
            except ValueError:
                pass

    if command == "query":
        result = search(query, limit=limit)
        print(result)
    else:
        print(f"未知命令: {command}")
        print("可用命令: query")
        sys.exit(1)


if __name__ == "__main__":
    main()
