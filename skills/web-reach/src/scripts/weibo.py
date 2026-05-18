#!/usr/bin/env python3
"""
微博模块 — 热搜、搜索、用户动态

通过微博公开接口获取数据，无需认证。

用法：
    python3 weibo.py hot                          # 热搜榜
    python3 weibo.py search "关键词"              # 搜索
    python3 weibo.py search "关键词" --limit 10   # 搜索（限制数量）
    python3 weibo.py user "用户ID"                # 用户最近动态
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://m.weibo.cn/",
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


def hot_search() -> str:
    """获取微博热搜"""
    # 尝试多个接口
    urls = [
        "https://weibo.com/ajax/side/hotSearch",
        "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot",
    ]

    for url in urls:
        data = fetch_json(url)
        if "error" not in data:
            break
    else:
        # 所有接口都失败，尝试通过 Jina Reader
        import urllib.request as req2
        try:
            jina_url = "https://r.jina.ai/https://s.weibo.com/top/summary"
            r = urllib.request.Request(jina_url, headers={
                "Accept": "text/markdown",
                "User-Agent": "Mozilla/5.0 (compatible; WebReach/1.0)",
            })
            with urllib.request.urlopen(r, timeout=15) as resp:
                content = resp.read().decode("utf-8")
                if content.strip():
                    return f"🔥 **微博热搜**\n\n{content[:2000]}"
        except Exception:
            pass
        return "❌ 获取热搜失败：微博接口限制，请稍后再试"

    # 解析 ajax/side/hotSearch 格式
    realtime = data.get("data", {}).get("realtime", [])
    if realtime:
        output = "🔥 **微博热搜**\n\n"
        for i, item in enumerate(realtime[:30], 1):
            word = item.get("word", "")
            num = item.get("num", 0)
            label = item.get("label_name", "")
            flag = f" [{label}]" if label else ""
            output += f"{i:2d}. {word}{flag}"
            if num:
                output += f" ({num:,})"
            output += "\n"
        return output

    # 解析移动端格式
    cards = data.get("data", {}).get("cards", [])
    if not cards:
        return "❌ 未获取到热搜数据"

    output = "🔥 **微博热搜**\n\n"
    count = 0
    for card in cards:
        card_group = card.get("card_group", [])
        for item in card_group:
            desc = item.get("desc", "")
            if desc:
                count += 1
                output += f"{count:2d}. {desc}\n"
                if count >= 30:
                    break
        if count >= 30:
            break

    return output if count > 0 else "❌ 未获取到热搜数据"


def search_weibo(query: str, limit: int = 10) -> str:
    """搜索微博"""
    encoded = urllib.parse.quote(query)
    url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{encoded}&page_type=searchall"
    data = fetch_json(url)

    if "error" in data:
        return f"❌ 搜索失败: {data['error']}"

    cards = data.get("data", {}).get("cards", [])
    if not cards:
        return f"未找到与 \"{query}\" 相关的微博"

    output = f"🔍 搜索: \"{query}\"\n\n"
    count = 0

    for card in cards:
        if card.get("card_type") == 9:
            mblog = card.get("mblog", {})
            if not mblog:
                continue

            user = mblog.get("user", {})
            username = user.get("screen_name", "未知")
            text = mblog.get("text", "")
            # 简单去除 HTML 标签
            import re
            text = re.sub(r"<[^>]+>", "", text).strip()
            created = mblog.get("created_at", "")
            reposts = mblog.get("reposts_count", 0)
            comments = mblog.get("comments_count", 0)
            likes = mblog.get("attitudes_count", 0)

            count += 1
            output += f"**{count}. @{username}** ({created})\n"
            if len(text) > 150:
                text = text[:150] + "..."
            output += f"   {text}\n"
            output += f"   转发:{reposts} 评论:{comments} 点赞:{likes}\n\n"

            if count >= limit:
                break
        elif card.get("card_type") == 11:
            # card_group 类型
            for item in card.get("card_group", []):
                if item.get("card_type") == 9:
                    mblog = item.get("mblog", {})
                    if not mblog:
                        continue
                    user = mblog.get("user", {})
                    username = user.get("screen_name", "未知")
                    text = mblog.get("text", "")
                    import re
                    text = re.sub(r"<[^>]+>", "", text).strip()

                    count += 1
                    output += f"**{count}. @{username}**\n"
                    if len(text) > 150:
                        text = text[:150] + "..."
                    output += f"   {text}\n\n"

                    if count >= limit:
                        break
            if count >= limit:
                break

    return output if count > 0 else f"未找到与 \"{query}\" 相关的微博"


def user_timeline(uid: str) -> str:
    """获取用户最近动态"""
    url = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=107603{uid}"
    data = fetch_json(url)

    if "error" in data:
        return f"❌ 获取用户动态失败: {data['error']}"

    cards = data.get("data", {}).get("cards", [])
    if not cards:
        return "❌ 未获取到用户动态"

    output = ""
    count = 0

    for card in cards:
        if card.get("card_type") == 9:
            mblog = card.get("mblog", {})
            if not mblog:
                continue

            if count == 0:
                user = mblog.get("user", {})
                username = user.get("screen_name", "未知")
                followers = user.get("followers_count", 0)
                output = f"👤 **@{username}** (粉丝: {followers:,})\n\n"

            text = mblog.get("text", "")
            import re
            text = re.sub(r"<[^>]+>", "", text).strip()
            created = mblog.get("created_at", "")

            count += 1
            if len(text) > 200:
                text = text[:200] + "..."
            output += f"{count}. ({created}) {text}\n\n"

            if count >= 10:
                break

    return output if count > 0 else "❌ 未获取到用户动态"


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 weibo.py hot")
        print('  python3 weibo.py search "关键词"')
        print('  python3 weibo.py user "用户ID"')
        sys.exit(1)

    command = sys.argv[1]

    if command == "hot":
        print(hot_search())
    elif command == "search":
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            sys.exit(1)
        query = sys.argv[2]
        limit = 10
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[idx + 1])
                except ValueError:
                    pass
        print(search_weibo(query, limit=limit))
    elif command == "user":
        if len(sys.argv) < 3:
            print("请提供用户ID")
            sys.exit(1)
        print(user_timeline(sys.argv[2]))
    else:
        print(f"未知命令: {command}")
        print("可用命令: hot, search, user")
        sys.exit(1)


if __name__ == "__main__":
    main()
