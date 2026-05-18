# Polymarket Trade

| 版本 | 最近更新 | 来源 | License | 安全状态 |
|------|----------|------|---------|----------|
| v1.0.6 | 2026-05-12 | [joelchance/polymarket-trade](https://github.com/joelchance) | MIT-0 | ✅ 审核通过 |

---

## 这个 Skill 是什么

一个 Polymarket 预测市场的**只读数据查询工具**，附带本地模拟交易功能。

你在 AI 对话中用对话提问，Agent 自动获取 Polymarket 上各类事件的实时赔率、成交量和价格走势——不需要打开浏览器，不需要连接钱包。

## 它能做什么 / 不能做什么

| ✅ 能做 | ❌ 不能做 |
|---------|-----------|
| 查询市场赔率和成交量 | 执行真实交易 |
| 搜索和浏览预测事件 | 连接钱包或链上操作 |
| 追踪价格变动趋势 | 管理真实资金 |
| 设置本地价格告警 | 访问你的任何账户 |
| 模拟纸上交易（本地 JSON） | 发送你的数据到第三方 |

**一句话定位：Polymarket 的只读 AI 助手 + 本地纸上交易模拟器。**

## 适用场景

- **研究员/分析师**：快速获取市场情绪数据，辅助判断事件走向概率
- **交易员**：用纸上交易验证策略逻辑，不动真金白银
- **产品/运营**：监控与业务相关的预测市场动态（如加密资产、监管政策）
- **日常信息获取**：把预测市场当作一个概率化的新闻源

---

## 使用指南

### 安装

**1. 克隆本仓库到本地**

```bash
git clone <本仓库地址>
```

**2. 让 AI 帮你安装**

在 Kiro / Codex / Trae / Claude Code 等 AI 编码工具中，打开本仓库目录，直接对话：

```
你：帮我安装 skills/polymarket-trade 这个 Skill
```

AI 会自动将 `src/` 目录下的文件复制到正确的 Skills 目录，并处理好依赖。

**手动安装（可选）：**

如果你更习惯手动操作：

```bash
# 用户级（全局所有项目生效）
cp -r skills/polymarket-trade/src/ ~/.kiro/skills/polymarket-trade/

# 或项目级（仅当前项目生效）
cp -r skills/polymarket-trade/src/ .kiro/skills/polymarket-trade/
```

**3. 验证**

在 AI 对话中输入 `#` 查看 Skills 列表，确认 `polymarket` 已出现。之后直接用自然语言提问即可。

### 怎么用

安装完成后，在 AI 对话中直接用自然语言提问，Agent 会自动调用这个 Skill 获取数据并返回结果。

**场景一：早间市场速览**

```
你：现在 Polymarket 上哪些市场波动最大？
你：今天有哪些预测市场要结算？
```

**场景二：追踪特定事件**

```
你：搜一下 Polymarket 上关于 ethereum etf 的市场
你：帮我关注 ethereum-etf-2025 这个市场，赔率超过 70% 提醒我
你：我的 watchlist 里现在有什么？
```

**场景三：验证判断（纸上交易）**

```
你：模拟买入 ethereum-etf-2025，200 美元
你：看看我的模拟持仓情况
你：把 ethereum-etf-2025 卖了
```

初始模拟资金 $10,000，纯本地记录，不涉及任何真实资金。

**场景四：研报数据支撑**

```
你：给我一份 crypto 分类的 Polymarket 市场摘要
你：bitcoin-100k 这个市场现在什么情况？赔率多少？
你：最近一周政治类市场有什么大的变动？
```

### 定时任务（可选）

如果想自动化监控，可以在对话中让 AI 帮你配置：

```
你：帮我设置一个每小时检查 Polymarket 告警的定时任务
你：帮我加一个每天早上 9 点查看市场波动的 cron
你：把之前设置的 Polymarket 定时任务删掉
```

AI 会基于当前 Skill 目录下的脚本自动生成并配置 cron 任务。

> ⚠️ 不用时记得让 AI 帮你清理定时任务。

### 卸载

```bash
# 删除 Skill 文件
rm -rf ~/.kiro/skills/polymarket-trade/

# 清理本地数据
rm -rf ~/.polymarket/
```

---

## ⚠️ 注意事项

1. **不是交易工具** — 没有链上交互能力，不要期望用它下单
2. **不构成投资建议** — 数据仅供参考，决策责任自负
3. **本地文件** — 不再使用时建议删除 `~/.polymarket/` 目录

---

## 技术细节

| 项目 | 说明 |
|------|------|
| 数据来源 | Polymarket Gamma API（`gamma-api.polymarket.com`，公开接口，无需认证） |
| 本地存储 | `~/.polymarket/watchlist.json` + `portfolio.json` |
| 依赖 | Python 3 + `requests` 库 |
| Agent 自主调用 | 已禁用（`disable-model-invocation: true`） |

<details>
<summary>底层命令参考（维护者/审核者）</summary>

Agent 在后台调用的脚本命令：

```bash
python3 scripts/polymarket.py trending       # 热门市场
python3 scripts/polymarket.py search "xxx"   # 搜索
python3 scripts/polymarket.py movers         # 最大波动
python3 scripts/polymarket.py calendar       # 即将结算
python3 scripts/polymarket.py category crypto # 分类浏览
python3 scripts/polymarket.py watch add xxx  # 添加关注
python3 scripts/polymarket.py alerts         # 检查告警
python3 scripts/polymarket.py buy xxx 100    # 模拟买入
python3 scripts/polymarket.py portfolio      # 查看持仓
python3 scripts/polymarket.py sell xxx       # 模拟卖出
python3 scripts/polymarket.py digest crypto  # 分类摘要
python3 scripts/polymarket.py event xxx      # 事件详情
```

支持的分类：`politics` / `crypto` / `sports` / `tech` / `business`

</details>

---

## 安全审核摘要

已通过平台自动化审计（静态分析 + VirusTotal）及安全人员人工复核。

- 网络行为透明，仅访问 Polymarket 公开 API
- 无凭证需求，无数据外传
- 本地文件写入范围明确
- 原始文档中的金融诱导外链已在入库时移除

详见 [REVIEW.md](./REVIEW.md)
