#!/usr/bin/env python3
"""
YouTube 模块 — 视频字幕提取和搜索

通过 yt-dlp 提取 YouTube 视频字幕。
需要安装：pip install yt-dlp

用法：
    python3 youtube.py transcript "https://youtube.com/watch?v=xxx"
    python3 youtube.py search "关键词"
    python3 youtube.py search "关键词" --limit 5
"""

import sys
import json
import subprocess
import shutil


def check_dependency():
    """检查 yt-dlp 是否已安装"""
    if not shutil.which("yt-dlp"):
        print("❌ 未找到 yt-dlp，请先安装：pip install yt-dlp")
        sys.exit(1)


def get_transcript(url: str) -> str:
    """提取视频字幕"""
    check_dependency()

    try:
        # 获取视频信息和字幕
        result = subprocess.run(
            [
                "yt-dlp",
                "--dump-json",
                "--skip-download",
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs", "zh,en,zh-Hans,zh-Hant",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            return f"❌ 获取视频信息失败: {result.stderr.strip()}"

        info = json.loads(result.stdout)

        title = info.get("title", "未知标题")
        duration = info.get("duration", 0)
        channel = info.get("channel", "未知频道")
        upload_date = info.get("upload_date", "")

        output = f"📺 **{title}**\n"
        output += f"   频道: {channel}\n"
        output += f"   时长: {duration // 60}:{duration % 60:02d}\n"
        if upload_date:
            output += f"   上传: {upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}\n"
        output += "\n"

        # 尝试获取字幕
        subtitles = info.get("subtitles", {})
        auto_captions = info.get("automatic_captions", {})

        # 优先手动字幕，其次自动字幕
        sub_data = None
        sub_lang = None
        for lang in ["zh", "zh-Hans", "en", "zh-Hant"]:
            if lang in subtitles:
                sub_data = subtitles[lang]
                sub_lang = lang
                break
            if lang in auto_captions:
                sub_data = auto_captions[lang]
                sub_lang = f"{lang}(auto)"
                break

        if sub_data:
            output += f"📝 字幕 ({sub_lang}):\n\n"
            # 尝试获取纯文本格式的字幕
            # 实际字幕内容需要额外下载，这里返回字幕可用的信息
            output += "(字幕可用，使用 yt-dlp 下载完整字幕文件)\n"
        else:
            output += "⚠️ 未找到可用字幕\n"

        # 如果有描述
        description = info.get("description", "")
        if description:
            output += f"\n📄 视频描述:\n{description[:500]}"
            if len(description) > 500:
                output += "\n...(已截断)"

        return output

    except subprocess.TimeoutExpired:
        return "❌ 超时：视频信息获取超过 60 秒"
    except json.JSONDecodeError:
        return "❌ 解析视频信息失败"
    except Exception as e:
        return f"❌ 错误: {e}"


def search_videos(query: str, limit: int = 5) -> str:
    """搜索 YouTube 视频"""
    check_dependency()

    try:
        result = subprocess.run(
            [
                "yt-dlp",
                f"ytsearch{limit}:{query}",
                "--dump-json",
                "--skip-download",
                "--flat-playlist",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            return f"❌ 搜索失败: {result.stderr.strip()}"

        output = f"🔍 搜索: \"{query}\"\n\n"

        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            try:
                info = json.loads(line)
                title = info.get("title", "未知")
                url = info.get("url", info.get("webpage_url", ""))
                duration = info.get("duration", 0)
                channel = info.get("channel", info.get("uploader", ""))

                output += f"• **{title}**\n"
                if channel:
                    output += f"  频道: {channel}"
                if duration:
                    output += f" | 时长: {duration // 60}:{duration % 60:02d}"
                output += "\n"
                if url:
                    output += f"  {url}\n"
                output += "\n"
            except json.JSONDecodeError:
                continue

        return output if output.count("•") > 0 else "未找到相关视频"

    except subprocess.TimeoutExpired:
        return "❌ 搜索超时"
    except Exception as e:
        return f"❌ 错误: {e}"


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print('  python3 youtube.py transcript "https://youtube.com/watch?v=xxx"')
        print('  python3 youtube.py search "关键词" [--limit N]')
        sys.exit(1)

    command = sys.argv[1]
    arg = sys.argv[2]

    if command == "transcript":
        print(get_transcript(arg))
    elif command == "search":
        limit = 5
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[idx + 1])
                except ValueError:
                    pass
        print(search_videos(arg, limit=limit))
    else:
        print(f"未知命令: {command}")
        print("可用命令: transcript, search")
        sys.exit(1)


if __name__ == "__main__":
    main()
