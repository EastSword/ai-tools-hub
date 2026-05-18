<div align="center">

# 🛡️ AI Tools Hub

**经过安全审核的 AI 工具集合 — MCP Servers · Skills · Agents**

帮助开发者和安全团队更安全、更高效地使用 AI 能力

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---

## 为什么需要这个项目

AI Agent 生态正在爆发式增长。MCP Server、Skills、Agents 等工具层出不穷，但大多数缺乏安全审计——它们可能请求过多权限、依赖不可信的第三方包、自动执行远程指令、甚至包含供应链投毒风险。

**AI Tools Hub** 只收录经过代码审计和行为验证的工具。每个工具入库前都经过：

- 静态代码分析（依赖审计、权限检查、数据流追踪）
- 动态行为验证（网络请求监控、文件系统操作审计）
- 人工安全复核（逻辑审查、攻击面评估）

你可以放心地在日常工作中使用这里的任何工具。

---

## 📦 工具目录

### Skills

| 名称 | 分类 | 版本 | 说明 |
|:-----|:-----|:-----|:-----|
| [web-reach](./skills/web-reach/) | 互联网访问 | v1.0.0 | 13 个平台的只读访问能力（网页/搜索/YouTube/微博/GitHub 等） |
| [polymarket-trade](./skills/polymarket-trade/) | 数据查询 | v1.0.6 | Polymarket 预测市场只读查询 + 本地纸上交易模拟 |

### MCP Servers

| 名称 | 分类 | 版本 | 说明 |
|:-----|:-----|:-----|:-----|
| *征集中* | — | — | 欢迎提交经过安全审核的 MCP Server |

### Agents

| 名称 | 分类 | 版本 | 说明 |
|:-----|:-----|:-----|:-----|
| *征集中* | — | — | 欢迎提交经过安全审核的 Agent 配置 |

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/EastSword/ai-tools-hub.git
cd ai-tools-hub
```

### 2. 安装 Skill

**方式 A：让 AI 帮你装**

在 Kiro / Cursor / Windsurf / Claude Code 等 AI 编码工具中打开本仓库，直接对话：

```
你：帮我安装 skills/web-reach 这个 Skill
你：帮我安装 skills/polymarket-trade 这个 Skill
```

**方式 B：手动安装**

```bash
# 用户级（全局生效）
cp -r skills/web-reach/src/ ~/.kiro/skills/web-reach/
cp -r skills/polymarket-trade/src/ ~/.kiro/skills/polymarket-trade/

# 或项目级（仅当前项目）
cp -r skills/<name>/src/ .kiro/skills/<name>/
```

### 3. 安装 MCP Server

进入 `mcps/<name>/` 目录，将配置合并到你的 MCP 配置文件：

```bash
# 用户级
~/.kiro/settings/mcp.json

# 项目级
<project>/.kiro/settings/mcp.json
```

### 4. 验证

- Skill → 对话中输入 `#` 查看是否出现
- MCP → 命令面板搜索 `MCP`，确认 Server 已连接

---

## 🌐 Web Reach — 互联网访问能力

给你的 AI 加上互联网能力。在对话中直接说"帮我看看这个网页"、"搜一下最新的 LLM 框架"、"微博热搜是什么"——AI 就能帮你做到。

**即装即用（无需认证）：**

| 模块 | 能力 |
|------|------|
| 🌐 网页 | 读取任意网页内容 |
| 🔍 搜索 | 互联网搜索 |
| 📺 YouTube | 视频搜索、字幕提取 |
| 📺 B站 | 视频字幕提取 |
| 📡 RSS | 订阅源读取 |
| 📦 GitHub | 仓库信息、代码搜索 |
| 📰 微博 | 热搜、搜索 |
| 💬 微信公众号 | 文章搜索 |
| 💻 V2EX | 热帖浏览 |
| 💼 LinkedIn | 个人主页读取 |

**按需启用（需配置 Cookie）：** Twitter/X · 小红书 · 雪球

→ 详见 [skills/web-reach/README.md](./skills/web-reach/README.md)

---

## 📊 Polymarket Trade — 预测市场查询

Polymarket 预测市场的只读数据查询工具，附带本地模拟交易功能。

```
你：现在 Polymarket 上哪些市场波动最大？
你：搜一下关于 ethereum etf 的市场
你：模拟买入 ethereum-etf-2025，200 美元
```

- 查询市场赔率和成交量
- 搜索和浏览预测事件
- 追踪价格变动趋势
- 模拟纸上交易（本地 JSON，不涉及真实资金）

→ 详见 [skills/polymarket-trade/README.md](./skills/polymarket-trade/README.md)

---

## 🔒 安全原则

| 原则 | 说明 |
|------|------|
| **只读优先** | 所有工具默认只读，不发布、不修改、不删除 |
| **最小依赖** | 尽量使用标准库，第三方依赖必须是成熟项目 |
| **凭证自管** | 用户主动配置，本地存储，权限 600 |
| **模块隔离** | 每个工具独立，不装就不存在 |
| **网络透明** | 所有请求目标明确可审计 |
| **无自主调用** | Agent 不会自动触发工具（需用户显式调用） |
| **无远程指令** | 不从远程 URL 加载执行指令 |
| **无商业推广** | 不包含任何推广链接或利益关联 |

---

## 📁 仓库结构

```
ai-tools-hub/
├── README.md                        # 本文件
├── skills/
│   ├── web-reach/                   # 互联网访问能力（13 个平台）
│   │   ├── README.md                # 详细使用文档
│   │   ├── REVIEW.md                # 安全审核记录
│   │   └── src/                     # Skill 源码
│   │       ├── SKILL.md
│   │       └── scripts/
│   └── polymarket-trade/            # Polymarket 预测市场查询
│       ├── README.md
│       └── src/
│           ├── SKILL.md
│           ├── _meta.json
│           └── scripts/
├── mcps/                            # MCP Servers（征集中）
│   └── _template/
└── agents/                          # Agent 配置（征集中）
    └── _template/
```

---

## 兼容性

已测试的 AI 编码工具：

| 工具 | Skill | MCP |
|------|-------|-----|
| Kiro | ✅ | ✅ |
| Cursor | ✅ | ✅ |
| Windsurf | ✅ | ✅ |
| Claude Code | ✅ | ✅ |
| Trae | ✅ | ✅ |

---

## 贡献

欢迎提交经过安全审核的工具。提交前请确保：

1. 工具功能明确，文档完整
2. 无过度权限请求
3. 依赖清晰，无可疑第三方包
4. 附带安全审核说明（REVIEW.md）

提交 PR 后我们会进行安全复核。

---

## License

MIT

---

<div align="center">

**东方隐侠安全团队** · 让 AI 工具链更安全

</div>
