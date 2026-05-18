#!/usr/bin/env python3
"""
Bilibili 模块 — B站视频字幕提取

通过 yt-dlp 提取 B站视频字幕和信息。
需要安装：pip install yt-dlp

用法：
    python3 bilibili.py transcript "https://www.bilibili.com/video/BVxxx"
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
    """提取B站视频信息和字幕"""
    check_dependency()

    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--dump-json",
                "--skip-download",
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs", "zh,zh-Hans,en",
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
        uploader = info.get("uploader", "未知UP主")
        upload_date = info.get("upload_date", "")
        view_count = info.get("view_count", 0)
        like_count = info.get("like_count", 0)

        output = f"📺 **{title}**\n"
        output += f"   UP主: {uploader}\n"
        output += f"   时长: {duration // 60}:{duration % 60:02d}\n"
        if upload_date:
            output += f"   上传: {upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}\n"
        if view_count:
            output += f"   播放: {view_count:,}\n"
        if like_count:
            output += f"   点赞: {like_count:,}\n"
        output += "\n"

        # 字幕信息
        subtitles = info.get("subtitles", {})
        if subtitles:
            output += f"📝 字幕可用: {', '.join(subtitles.keys())}\n"
        else:
            output += "⚠️ 未找到字幕\n"

        # 描述
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


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print('  python3 bilibili.py transcript "https://www.bilibili.com/video/BVxxx"')
        sys.exit(1)

    command = sys.argv[1]
    url = sys.argv[2]

    if command == "transcript":
        print(get_transcript(url))
    else:
        print(f"未知命令: {command}")
        print("可用命令: transcript")
        sys.exit(1)


if __name__ == "__main__":
    main()
