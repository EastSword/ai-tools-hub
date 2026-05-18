#!/usr/bin/env python3
"""
GitHub 模块 — 查看公开仓库和搜索

通过 GitHub API 读取公开仓库信息。
无需认证即可访问公开数据（有速率限制：60次/小时）。
安装 gh CLI 后可提升到 5000次/小时。

用法：
    python3 github.py repo "owner/repo"
    python3 github.py search "关键词"
    python3 github.py search "关键词" --limit 5
"""

import sys
import json
import urllib.request
import urllib.error

GITHUB_API = "https://api.github.com"


def get_repo(repo_path: str) -> str:
    """获取仓库信息"""
    # 清理输入
    repo_path = repo_path.strip("/")
    if "github.com/" in repo_path:
        repo_path = repo_path.split("github.com/")[1].strip("/")
    # 去掉可能的子路径
    parts = repo_path.split("/")
    if len(parts) >= 2:
        repo_path = f"{parts[0]}/{parts[1]}"

    url = f"{GITHUB_API}/repos/{repo_path}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "WebReach/1.0",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        output = f"📦 **{data['full_name']}**\n"
        if data.get("description"):
            output += f"   {data['description']}\n"
        output += f"\n"
        output += f"   ⭐ {data.get('stargazers_count', 0):,} stars\n"
        output += f"   🍴 {data.get('forks_count', 0):,} forks\n"
        output += f"   👁️ {data.get('watchers_count', 0):,} watchers\n"
        output += f"   📝 语言: {data.get('language', '未知')}\n"
        output += f"   📄 License: {data.get('license', {}).get('spdx_id', '未知') if data.get('license') else '未知'}\n"
        output += f"   🕐 最后更新: {data.get('updated_at', '')[:10]}\n"
        output += f"   🔗 {data.get('html_url', '')}\n"

        if data.get("topics"):
            output += f"   🏷️ {', '.join(data['topics'])}\n"

        return output

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"❌ 仓库不存在: {repo_path}"
        elif e.code == 403:
            return "❌ API 速率限制，请稍后再试（或安装 gh CLI 提升限额）"
        return f"❌ HTTP 错误 {e.code}: {e.reason}"
    except Exception as e:
        return f"❌ 错误: {e}"


def search_repos(query: str, limit: int = 5) -> str:
    """搜索 GitHub 仓库"""
    encoded = urllib.parse.quote(query)

    url = f"{GITHUB_API}/search/repositories?q={encoded}&sort=stars&per_page={limit}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "WebReach/1.0",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        items = data.get("items", [])
        if not items:
            return f"未找到与 \"{query}\" 相关的仓库"

        output = f"🔍 搜索: \"{query}\" (共 {data.get('total_count', 0):,} 个结果)\n\n"

        for item in items:
            output += f"• **{item['full_name']}** ⭐{item.get('stargazers_count', 0):,}\n"
            if item.get("description"):
                desc = item["description"][:80]
                if len(item["description"]) > 80:
                    desc += "..."
                output += f"  {desc}\n"
            output += f"  {item.get('html_url', '')}\n\n"

        return output

    except urllib.error.HTTPError as e:
        if e.code == 403:
            return "❌ API 速率限制，请稍后再试"
        return f"❌ HTTP 错误 {e.code}: {e.reason}"
    except Exception as e:
        return f"❌ 错误: {e}"


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print('  python3 github.py repo "owner/repo"')
        print('  python3 github.py repo "https://github.com/owner/repo"')
        print('  python3 github.py search "关键词" [--limit N]')
        sys.exit(1)

    command = sys.argv[1]
    arg = sys.argv[2]

    if command == "repo":
        print(get_repo(arg))
    elif command == "search":
        limit = 5
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[idx + 1])
                except ValueError:
                    pass
        print(search_repos(arg, limit=limit))
    else:
        print(f"未知命令: {command}")
        print("可用命令: repo, search")
        sys.exit(1)


if __name__ == "__main__":
    main()
