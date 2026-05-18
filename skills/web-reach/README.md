# 🌐 Web Reach

| 版本 | 最近更新 | License | 安全状态 |
|------|----------|---------|----------|
| v1.0.0 | 2026-05-18 | MIT | ✅ 审核通过 |

**给你的 AI 加上互联网能力。** 在对话中直接说"帮我看看这个网页"、"搜一下最新的 LLM 框架"、"微博热搜是什么"——AI 就能帮你做到。

---

## 能力一览

### 即装即用（无需认证）

| 模块 | 你可以这样问 AI |
|------|-----------------|
| 🌐 **网页** | "帮我看看这个链接写了什么" |
| 🔍 **搜索** | "搜一下 kubernetes 安全最佳实践" |
| 📺 **YouTube** | "这个视频讲了什么？" / "搜一下 Rust 教程" |
| 📺 **B站** | "这个B站视频的字幕帮我提取一下" |
| 📡 **RSS** | "帮我读一下这个博客的最新文章" |
| 📦 **GitHub** | "这个仓库是做什么的？" / "搜一下 MCP Server" |
| 📰 **微博** | "现在微博热搜是什么？" / "搜一下 AI 安全" |
| 💬 **微信公众号** | "搜一下公众号里关于大模型的文章" |
| 💻 **V2EX** | "V2EX 现在什么帖子最火？" |
| 💼 **LinkedIn** | "帮我看看这个人的 LinkedIn" |

### 按需启用（需要配置 Cookie）

| 模块 | 你可以这样问 AI | 注意 |
|------|-----------------|------|
| 🐦 **Twitter/X** | "看看这条推文" / "搜一下推特上的讨论" | ⚠️ 用小号 |
| 📕 **小红书** | "搜一下小红书上关于 AI 编程的笔记" | ⚠️ 用小号 |
| 📈 **雪球** | "茅台现在什么行情？" / "雪球热帖" | Cookie 会过期 |

---

## 安装

### 方式一：让 AI 帮你装

克隆本仓库后，在 Kiro / Codex / Trae / Claude Code 中打开，直接说：

```
你：帮我安装 skills/web-reach 这个 Skill
```

### 方式二：手动安装

```bash
# 全部模块
cp -r skills/web-reach/src/ ~/.kiro/skills/web-reach/

# 可选依赖（YouTube/B站字幕需要）
pip install yt-dlp

# 可选依赖（RSS 需要）
pip install feedparser
```

### 验证

```
你：帮我搜一下 "AI agent security"
```

AI 返回搜索结果就说明安装成功。

---

## 使用示例

安装后直接在 AI 对话中用自然语言，不需要记任何命令。

### 日常信息获取

```
你：帮我看看这个链接 https://xxx.com/article
你：搜一下最新的 LLM 框架对比
你：现在微博热搜是什么？
你：V2EX 今天什么帖子最火？
```

### 技术研究

```
你：这个 GitHub 仓库是做什么的？https://github.com/xxx/yyy
你：搜一下 GitHub 上有什么好用的安全工具
你：帮我读一下这个 RSS 源的最新内容
你：搜一下公众号里关于 DevSecOps 的文章
```

### 视频内容

```
你：这个 YouTube 视频讲了什么？https://youtube.com/watch?v=xxx
你：帮我搜一下 YouTube 上关于 Rust 的教程
你：这个B站视频的字幕帮我提取一下
```

### 社交平台（需配置 Cookie）

```
你：帮我配置 Twitter 的 Cookie
你：看看这条推文说了什么 https://x.com/xxx/status/123
你：搜一下小红书上关于远程办公的笔记
你：茅台现在什么行情？
```

---

## 配置认证模块

需要 Cookie 的模块（Twitter、小红书、雪球），在对话中让 AI 帮你配置：

```
你：帮我配置 Twitter 的 Cookie，我的 Cookie 是 "auth_token=xxx; ct0=yyy"
```

或者手动配置：

```bash
# 查看已配置的凭证
python3 ~/.kiro/skills/web-reach/scripts/credentials.py list

# 配置某个平台
python3 ~/.kiro/skills/web-reach/scripts/credentials.py set twitter '{"cookie": "你的cookie"}'

# 删除凭证
python3 ~/.kiro/skills/web-reach/scripts/credentials.py remove twitter
```

**Cookie 获取方式：**
1. 用浏览器登录目标平台（**建议使用小号**）
2. 安装 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 浏览器插件
3. 导出 Cookie 字符串
4. 发给 AI 或手动配置

> ⚠️ Cookie 等同于完整登录权限。认证模块请务必使用小号，平台可能检测到非正常访问并封号。

> 🔒 凭证存储在 `~/.web-reach/credentials/`，文件权限 600（仅所有者可读写），不上传不外传。

---

## 安全设计

| 原则 | 说明 |
|------|------|
| 只读 | 所有模块只读取数据，不发布、不修改、不删除 |
| 不自动安装 | 不会自动 pip install 或修改系统环境 |
| 凭证自管 | Cookie 由用户主动配置，存储在本地，权限 600 |
| 模块隔离 | 每个平台一个独立脚本，不装就不存在 |
| 网络透明 | 所有请求目标明确：Jina API、YouTube、GitHub 等公开服务 |
| 无自主调用 | Agent 不会自动触发（`disable-model-invocation: true`） |

---

## 依赖说明

| 模块 | 需要安装 | 说明 |
|------|----------|------|
| web / search / github / weibo / wechat / v2ex / linkedin | 无 | 纯 Python 标准库 |
| youtube / bilibili | `pip install yt-dlp` | 154k star，成熟项目 |
| rss | `pip install feedparser` | Python 生态标准 RSS 库 |
| twitter / xiaohongshu / xueqiu | 无额外依赖 | 但需要配置 Cookie |

---

## 卸载

```bash
# 删除 Skill
rm -rf ~/.kiro/skills/web-reach/

# 同时清理凭证（如有）
rm -rf ~/.web-reach/
```

---

## 项目来源与改进说明

### 参考来源

本项目的能力设计参考了 [Agent Reach](https://github.com/Panniantong/Agent-Reach)（19.7k star），一个为 AI Agent 提供互联网访问能力的开源项目。Agent Reach 覆盖了 15 个平台，思路很好，但在安全评审中发现了几个不可接受的风险。

### 为什么要单独做一个 Skill

Agent Reach 的核心问题：

1. **它是一个"安装器"，不是一个 Skill** — 它要求 Agent 拥有 shell 执行权限，然后自动 `pip install`、`clone` 仓库、配置 MCP Server。这意味着你把系统控制权交给了一个第三方脚本。

2. **供应链攻击面太大** — 它依赖 10+ 个第三方 CLI 工具（twitter-cli、rdt-cli、xhs-cli、mcporter 等），每一个都是独立的攻击面。任何一个上游被投毒，你的环境就被攻破。

3. **自动收集 Cookie** — 安装流程会引导 Agent 主动向用户索要各平台的 Cookie，存储在本地。虽然声称"不外传"，但整个流程缺乏用户主动意识。

4. **install.md 本身就是攻击向量** — 用户被引导把一个远程 URL 丢给 Agent 执行。如果该 URL 内容被篡改（仓库劫持、DNS 劫持），Agent 会盲目执行恶意指令。

5. **包含商业推广** — README 底部有 API 中转站和云服务的推广链接，存在利益关联。

### Web Reach 的改进

| 问题 | Agent Reach 的做法 | Web Reach 的做法 |
|------|-------------------|-----------------|
| 安装方式 | Agent 自动执行 pip install + clone | 用户手动复制文件，不修改系统 |
| 依赖管理 | 10+ 第三方 CLI，自动安装 | 2 个成熟库，用户自行安装 |
| Cookie 收集 | 安装流程自动引导收集 | 用户自主决定，单独配置步骤 |
| Agent 权限 | 要求 shell 执行权限 | 不要求，通过 Skill 脚本调用 |
| 写入操作 | 支持发帖、评论、点赞 | 仅只读，不做任何写入 |
| 模块粒度 | 全量安装，不用也在 | 按需选装，不装就不存在 |
| 远程指令 | 让 Agent 读取远程 install.md 执行 | 所有代码在本地仓库，可审计 |
| 推广内容 | 包含商业推广链接 | 无 |

### 一句话总结

Agent Reach 的想法很好，但它的实现方式对安全要求高的团队来说风险不可控。Web Reach 保留了核心能力（13 个平台的只读访问），去掉了所有高风险设计，让用户对自己的环境有完全的控制权。

详细审核记录见 [REVIEW.md](./REVIEW.md)
