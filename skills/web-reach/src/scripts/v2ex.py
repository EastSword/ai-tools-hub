#!/usr/bin/env python3
"""
V2EX 模块 — 热门帖子、节点浏览、帖子详情

通过 V2EX 公开 API 获取数据，无需认证。

用法：
    python3 v2ex.py hot                       # 热门帖子
    python3 v2ex.py node "python"             # 节点帖子
    python3 v2ex.py topic 123456              # 帖子详情
    python3 v2ex.py replies 123456            # 帖子回复
"""

import sys
import json
import urllib.request
import urllib.error

V2EX_API = "https://www.v2ex.com/api/v2"
V2EX_API_V1 = "https://www.v2ex.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
    "Accept": "application/json",
}


def fetch_json(url: str) -> dict:
    """通用 JSON 请求"""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def hot_topics() -> str:
    """获取热门帖子"""
    data = fetch_json(f"{V2EX_API_V1}/topics/hot.json")

    if isinstance(data, dict) and "error" in data:
        return f"❌ 获取热门帖子失败: {data['error']}"

    if not isinstance(data, list) or not data:
        return "❌ 未获取到热门帖子"

    output = "🔥 **V2EX 热门帖子**\n\n"
    for i, topic in enumerate(data[:20], 1):
        title = topic.get("title", "无标题")
        node = topic.get("node", {}).get("title", "")
        replies = topic.get("replies", 0)
        member = topic.get("member", {}).get("username", "")

        output += f"{i:2d}. **{title}**\n"
        output += f"    [{node}] @{member} | 回复:{replies}\n\n"

    return output


def node_topics(node_name: str) -> str:
    """获取节点帖子"""
    data = fetch_json(f"{V2EX_API_V1}/topics/show.json?node_name={node_name}")

    if isinstance(data, dict) and "error" in data:
        return f"❌ 获取节点帖子失败: {data['error']}"

    if not isinstance(data, list) or not data:
        return f"❌ 未找到节点 \"{node_name}\" 或无帖子"

    output = f"📂 **V2EX 节点: {node_name}**\n\n"
    for i, topic in enumerate(data[:15], 1):
        title = topic.get("title", "无标题")
        replies = topic.get("replies", 0)
        member = topic.get("member", {}).get("username", "")
        topic_id = topic.get("id", "")

        output += f"{i:2d}. **{title}**\n"
        output += f"    @{member} | 回复:{replies} | ID:{topic_id}\n\n"

    return output


def topic_detail(topic_id: str) -> str:
    """获取帖子详情"""
    data = fetch_json(f"{V2EX_API_V1}/topics/show.json?id={topic_id}")

    if isinstance(data, dict) and "error" in data:
        return f"❌ 获取帖子失败: {data['error']}"

    if isinstance(data, list) and data:
        topic = data[0]
    elif isinstance(data, dict):
        topic = data
    else:
        return "❌ 未找到帖子"

    title = topic.get("title", "无标题")
    content = topic.get("content", "")
    member = topic.get("member", {}).get("username", "")
    node = topic.get("node", {}).get("title", "")
    replies = topic.get("replies", 0)
    created = topic.get("created", "")

    output = f"📝 **{title}**\n\n"
    output += f"作者: @{member} | 节点: [{node}] | 回复: {replies}\n\n"
    if content:
        output += f"---\n\n{content}\n"
    else:
        output += "(无正文内容)\n"

    return output


def topic_replies(topic_id: str) -> str:
    """获取帖子回复"""
    data = fetch_json(f"{V2EX_API_V1}/replies/show.json?topic_id={topic_id}")

    if isinstance(data, dict) and "error" in data:
        return f"❌ 获取回复失败: {data['error']}"

    if not isinstance(data, list) or not data:
        return "暂无回复"

    output = f"💬 **帖子 #{topic_id} 的回复** (共 {len(data)} 条)\n\n"
    for i, reply in enumerate(data[:20], 1):
        member = reply.get("member", {}).get("username", "")
        content = reply.get("content", "")
        if len(content) > 200:
            content = content[:200] + "..."
        output += f"{i}. @{member}: {content}\n\n"

    if len(data) > 20:
        output += f"... 还有 {len(data) - 20} 条回复\n"

    return output


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 v2ex.py hot")
        print('  python3 v2ex.py node "python"')
        print("  python3 v2ex.py topic 123456")
        print("  python3 v2ex.py replies 123456")
        sys.exit(1)

    command = sys.argv[1]

    if command == "hot":
        print(hot_topics())
    elif command == "node":
        if len(sys.argv) < 3:
            print("请提供节点名称")
            sys.exit(1)
        print(node_topics(sys.argv[2]))
    elif command == "topic":
        if len(sys.argv) < 3:
            print("请提供帖子ID")
            sys.exit(1)
        print(topic_detail(sys.argv[2]))
    elif command == "replies":
        if len(sys.argv) < 3:
            print("请提供帖子ID")
            sys.exit(1)
        print(topic_replies(sys.argv[2]))
    else:
        print(f"未知命令: {command}")
        print("可用命令: hot, node, topic, replies")
        sys.exit(1)


if __name__ == "__main__":
    main()
