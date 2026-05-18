---
name: web-reach
description: 给 AI Agent 添加互联网访问能力。读网页、视频字幕、搜索、RSS、社交平台。模块化设计，按需启用。
homepage: https://polymarket.com
user-invocable: true
disable-model-invocation: true
metadata:
  emoji: "🌐"
  requires:
    bins: [python3]
---

# Web Reach

给 AI Agent 添加互联网访问能力。模块化设计，按需启用。

## 公开模块（无需认证）

### 🌐 读网页
```bash
python3 {baseDir}/scripts/web.py read "URL"
```

### 🔍 搜索
```bash
python3 {baseDir}/scripts/search.py query "关键词"
python3 {baseDir}/scripts/search.py query "关键词" --limit 10
```

### 📺 YouTube 字幕
```bash
python3 {baseDir}/scripts/youtube.py transcript "URL"
python3 {baseDir}/scripts/youtube.py search "关键词"
```

### 📺 B站字幕
```bash
python3 {baseDir}/scripts/bilibili.py transcript "URL"
```

### 📡 RSS
```bash
python3 {baseDir}/scripts/rss.py read "FEED_URL"
python3 {baseDir}/scripts/rss.py read "FEED_URL" --limit 5
```

### 📦 GitHub
```bash
python3 {baseDir}/scripts/github.py repo "owner/repo"
python3 {baseDir}/scripts/github.py search "关键词"
```

### 📰 微博
```bash
python3 {baseDir}/scripts/weibo.py hot
python3 {baseDir}/scripts/weibo.py search "关键词"
python3 {baseDir}/scripts/weibo.py user "用户ID"
```

### 💬 微信公众号
```bash
python3 {baseDir}/scripts/wechat.py search "关键词"
python3 {baseDir}/scripts/wechat.py read "https://mp.weixin.qq.com/s/xxx"
```

### 💻 V2EX
```bash
python3 {baseDir}/scripts/v2ex.py hot
python3 {baseDir}/scripts/v2ex.py node "python"
python3 {baseDir}/scripts/v2ex.py topic 123456
python3 {baseDir}/scripts/v2ex.py replies 123456
```

### 💼 LinkedIn（公开页面）
```bash
python3 {baseDir}/scripts/linkedin.py profile "https://linkedin.com/in/username"
python3 {baseDir}/scripts/linkedin.py company "https://linkedin.com/company/name"
```

## 认证模块（需要配置 Cookie）

以下模块需要用户主动配置凭证才能使用。凭证存储在 `~/.web-reach/credentials/`，权限 600。

### 凭证管理
```bash
python3 {baseDir}/scripts/credentials.py list
python3 {baseDir}/scripts/credentials.py set <平台> '{"cookie": "..."}'
python3 {baseDir}/scripts/credentials.py get <平台>
python3 {baseDir}/scripts/credentials.py remove <平台>
```

### 🐦 Twitter/X（需要 Cookie）
```bash
python3 {baseDir}/scripts/twitter.py tweet "https://x.com/user/status/123"
python3 {baseDir}/scripts/twitter.py search "关键词"
python3 {baseDir}/scripts/twitter.py user "username"
```
⚠️ 配置: `python3 {baseDir}/scripts/credentials.py set twitter '{"cookie": "..."}'`
⚠️ 建议使用小号，存在封号风险。

### 📕 小红书（需要 Cookie）
```bash
python3 {baseDir}/scripts/xiaohongshu.py search "关键词"
python3 {baseDir}/scripts/xiaohongshu.py read "笔记URL"
```
⚠️ 配置: `python3 {baseDir}/scripts/credentials.py set xiaohongshu '{"cookie": "..."}'`
⚠️ 建议使用小号，存在封号风险。

### 📈 雪球（需要 Cookie）
```bash
python3 {baseDir}/scripts/xueqiu.py hot
python3 {baseDir}/scripts/xueqiu.py quote "SH600519"
python3 {baseDir}/scripts/xueqiu.py search "茅台"
```
⚠️ 配置: `python3 {baseDir}/scripts/credentials.py set xueqiu '{"cookie": "..."}'`

## 安全说明

- 公开模块：只读公开数据，不需要任何认证
- 认证模块：凭证由用户自行管理，存储在本地 `~/.web-reach/credentials/`（权限 600）
- 所有模块只读，不写入任何外部服务
- 不会被 Agent 自主调用（disable-model-invocation: true）
- 认证模块建议使用小号，避免主账号被封
