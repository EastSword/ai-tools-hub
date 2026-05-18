#!/usr/bin/env python3
"""
雪球模块 — 股票行情、热门帖子（需要认证）

⚠️ 需要配置 Cookie 才能使用。

配置方式：
    python3 credentials.py set xueqiu '{"cookie": "你的cookie字符串"}'

Cookie 获取方式：
    1. 用浏览器登录雪球
    2. 安装 Cookie-Editor 浏览器插件
    3. 导出 Cookie 字符串
    4. 通过 credentials.py 保存

用法：
    python3 xueqiu.py hot                     # 热门帖子
    python3 xueqiu.py quote "SH600519"        # 股票行情
    python3 xueqiu.py search "茅台"           # 搜索股票
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

CREDENTIALS_FILE = Path.home() / ".web-reach" / "credentials" / "xueqiu.json"
BASE_URL = "https://xueqiu.com"
STOCK_API = "https://stock.xueqiu.com"


def get_cookie() -> str:
    """读取雪球 Cookie"""
    if not CREDENTIALS_FILE.exists():
        print("❌ 雪球凭证未配置")
        print()
        print("配置方式：")
        print("  1. 用浏览器登录雪球")
        print("  2. 用 Cookie-Editor 插件导出 Cookie")
        print("  3. 运行: python3 credentials.py set xueqiu '{\"cookie\": \"你的cookie\"}'")
        sys.exit(1)

    with open(CREDENTIALS_FILE) as f:
        data = json.load(f)
    return data.get("cookie", "")


def fetch_with_cookie(url: str) -> dict:
    """带 Cookie 的请求"""
    cookie = get_cookie()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Cookie": cookie,
        "Accept": "application/json",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}（Cookie 可能已过期）"}
    except Exception as e:
        return {"error": str(e)}


def hot_posts() -> str:
    """获取热门帖子"""
    url = f"{BASE_URL}/statuses/hot/listV2.json?since_id=-1&max_id=-1&size=15"
    data = fetch_with_cookie(url)

    if "error" in data:
        return f"❌ 获取热帖失败: {data['error']}"

    items = data.get("items", [])
    if not items:
        return "❌ 未获取到热门帖子"

    output = "🔥 **雪球热帖**\n\n"
    for i, item in enumerate(items[:15], 1):
        original = item.get("original_status", item)
        title = original.get("title", "")
        text = original.get("text", "")
        user = original.get("user", {}).get("screen_name", "")
        reply_count = original.get("reply_count", 0)
        like_count = original.get("like_count", 0)

        # 简单去除 HTML
        import re
        text = re.sub(r"<[^>]+>", "", text).strip()

        display = title if title else (text[:80] + "..." if len(text) > 80 else text)
        output += f"{i:2d}. **{display}**\n"
        output += f"    @{user} | 回复:{reply_count} 点赞:{like_count}\n\n"

    return output


def get_quote(symbol: str) -> str:
    """获取股票行情"""
    url = f"{STOCK_API}/v5/stock/quote.json?symbol={symbol}&extend=detail"
    data = fetch_with_cookie(url)

    if "error" in data:
        return f"❌ 获取行情失败: {data['error']}"

    quote = data.get("data", {}).get("quote", {})
    if not quote:
        return f"❌ 未找到股票: {symbol}"

    name = quote.get("name", symbol)
    current = quote.get("current", 0)
    percent = quote.get("percent", 0)
    chg = quote.get("chg", 0)
    high = quote.get("high", 0)
    low = quote.get("low", 0)
    volume = quote.get("volume", 0)
    amount = quote.get("amount", 0)
    market_capital = quote.get("market_capital", 0)

    arrow = "📈" if percent >= 0 else "📉"

    output = f"{arrow} **{name}** ({symbol})\n\n"
    output += f"   现价: ¥{current}\n"
    output += f"   涨跌: {chg:+.2f} ({percent:+.2f}%)\n"
    output += f"   最高: ¥{high} | 最低: ¥{low}\n"
    if volume:
        output += f"   成交量: {volume:,.0f}\n"
    if amount:
        output += f"   成交额: ¥{amount:,.0f}\n"
    if market_capital:
        output += f"   市值: ¥{market_capital/1e8:,.1f}亿\n"

    return output


def search_stock(query: str) -> str:
    """搜索股票"""
    encoded = urllib.parse.quote(query)
    url = f"{BASE_URL}/stock/search.json?code={encoded}&size=10"
    data = fetch_with_cookie(url)

    if "error" in data:
        return f"❌ 搜索失败: {data['error']}"

    stocks = data.get("stocks", [])
    if not stocks:
        return f"未找到与 \"{query}\" 相关的股票"

    output = f"🔍 搜索: \"{query}\"\n\n"
    for stock in stocks[:10]:
        code = stock.get("code", "")
        name = stock.get("name", "")
        exchange = stock.get("exchange", "")
        output += f"  • {name} ({code}) [{exchange}]\n"

    return output


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 xueqiu.py hot")
        print('  python3 xueqiu.py quote "SH600519"')
        print('  python3 xueqiu.py search "茅台"')
        print()
        print("⚠️ 需要先配置 Cookie：")
        print('  python3 credentials.py set xueqiu \'{"cookie": "..."}\'')
        sys.exit(1)

    command = sys.argv[1]

    if command == "hot":
        print(hot_posts())
    elif command == "quote":
        if len(sys.argv) < 3:
            print("请提供股票代码，如 SH600519")
            sys.exit(1)
        print(get_quote(sys.argv[2]))
    elif command == "search":
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            sys.exit(1)
        print(search_stock(sys.argv[2]))
    else:
        print(f"未知命令: {command}")
        print("可用命令: hot, quote, search")
        sys.exit(1)


if __name__ == "__main__":
    main()
