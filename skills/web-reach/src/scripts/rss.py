#!/usr/bin/env python3
"""
RSS 模块 — 读取 RSS/Atom 订阅源

通过 feedparser 解析 RSS 和 Atom 订阅源。
需要安装：pip install feedparser

用法：
    python3 rss.py read "https://blog.example.com/feed.xml"
    python3 rss.py read "https://blog.example.com/feed.xml" --limit 5
"""

import sys

try:
    import feedparser
except ImportError:
    print("❌ 未找到 feedparser，请先安装：pip install feedparser")
    sys.exit(1)


def read_feed(url: str, limit: int = 10) -> str:
    """读取 RSS/Atom 订阅源"""
    try:
        feed = feedparser.parse(url)

        if feed.bozo and not feed.entries:
            return f"❌ 解析失败: {feed.bozo_exception}"

        title = feed.feed.get("title", "未知订阅源")
        link = feed.feed.get("link", "")
        description = feed.feed.get("description", "")

        output = f"📡 **{title}**\n"
        if description:
            output += f"   {description[:100]}\n"
        if link:
            output += f"   {link}\n"
        output += f"   共 {len(feed.entries)} 条内容\n\n"

        for i, entry in enumerate(feed.entries[:limit]):
            entry_title = entry.get("title", "无标题")
            entry_link = entry.get("link", "")
            published = entry.get("published", entry.get("updated", ""))
            summary = entry.get("summary", "")

            output += f"**{i+1}. {entry_title}**\n"
            if published:
                output += f"   📅 {published}\n"
            if summary:
                # 清理 HTML 标签
                clean_summary = summary.replace("<p>", "").replace("</p>", "\n")
                clean_summary = clean_summary.replace("<br>", "\n").replace("<br/>", "\n")
                # 简单去除其他标签
                import re
                clean_summary = re.sub(r"<[^>]+>", "", clean_summary).strip()
                if len(clean_summary) > 200:
                    clean_summary = clean_summary[:200] + "..."
                output += f"   {clean_summary}\n"
            if entry_link:
                output += f"   🔗 {entry_link}\n"
            output += "\n"

        return output

    except Exception as e:
        return f"❌ 错误: {e}"


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print('  python3 rss.py read "https://blog.example.com/feed.xml"')
        print('  python3 rss.py read "https://blog.example.com/feed.xml" --limit 5')
        sys.exit(1)

    command = sys.argv[1]
    url = sys.argv[2]

    limit = 10
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            try:
                limit = int(sys.argv[idx + 1])
            except ValueError:
                pass

    if command == "read":
        print(read_feed(url, limit=limit))
    else:
        print(f"未知命令: {command}")
        print("可用命令: read")
        sys.exit(1)


if __name__ == "__main__":
    main()
