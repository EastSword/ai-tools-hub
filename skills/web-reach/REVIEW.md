# 审核记录

- **名称**：Web Reach
- **版本**：v1.0.0
- **审核日期**：2026-05-18
- **审核人**：qianli
- **结论**：🟢 通过

## 设计来源

基于 Agent Reach (https://github.com/Panniantong/Agent-Reach) 的能力设计改造。
原项目存在以下安全问题，本项目已全部修复：

| 原项目风险 | 本项目处理 |
|-----------|-----------|
| 自动 pip install / clone 仓库 | 移除，用户手动安装依赖 |
| 收集 Cookie（Twitter/小红书等） | 移除，不包含任何需认证的平台 |
| 要求 Agent shell 执行权限 | 移除，通过 Skill 脚本调用 |
| 10+ 第三方 CLI 依赖 | 精简为 2 个成熟库（yt-dlp + feedparser） |
| MCP Server 自动配置 | 移除 |
| 金融诱导推广链接 | 移除 |

## 检查项

- [x] 无隐藏指令 / 不可见字符
- [x] 无 prompt 注入 payload
- [x] 权限声明合理且最小化（只读公开数据）
- [x] 行为与描述一致
- [x] 无信息泄露风险
- [x] 不会覆盖系统安全规则
- [x] 无 Cookie/Token 收集
- [x] 网络请求目标明确且公开

## 网络访问范围

| 模块 | 目标 | 说明 |
|------|------|------|
| web | r.jina.ai | Jina Reader，免费公开 API |
| search | s.jina.ai | Jina Search，免费公开 API |
| youtube | youtube.com | 通过 yt-dlp 本地执行 |
| bilibili | bilibili.com | 通过 yt-dlp 本地执行 |
| rss | 用户指定的 RSS URL | feedparser 本地解析 |
| github | api.github.com | GitHub 公开 API |

## 备注

- web 和 search 模块零依赖（仅用 Python 标准库 urllib）
- youtube 和 bilibili 模块依赖 yt-dlp（154k star，成熟项目）
- rss 模块依赖 feedparser（2.3k star，Python 生态标准选择）
- github 模块零依赖（直接调用 GitHub REST API）
