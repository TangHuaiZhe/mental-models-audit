# Regression Case 001 — 三花智控 H 股 02050

## 目的

验证 v0.1 Mental Models Audit 在工业制造 + A/H 双重上市场景中的模型选择、去重和 Adversarial Audit 能力。

## 分析对象

- company: 三花智控
- industry: 热管理 / 工业零部件 / 机器人执行器
- security: 02050.HK
- share_class: H 股，相对 A 股 002050 存在显著市场分割
- date: 2026-11-22

## v0.1 原始结果

- Material models: 26
- Secondary models: 61
- Not material: 13
- 去重后独立 mechanism clusters: 约 8

## 最有价值的增量发现

1. **company ≠ security**：三花可以是好公司，但 H 股的赔率结构需要单独分析。
2. **share_class 是独立分析对象**：A/H 市场分割、流动性、投资者结构、资本配置不能被公司基本面替代。
3. **机器人应按 Real Option 处理**：证据已从“研发/无订单”升级到“批量交付/产线爬坡”，但财务披露仍不足以纳入确定性主业盈利预测。
4. **高市占率 ≠ 强定价权**：护城河和价值捕获必须分开。
5. **Material 数量会制造伪共识**：26 个 Material 最终只有约 8 个独立机制。

## 暴露出的重复模型

- 021 / 075：Stock–Flow
- 067 / 091：路径依赖
- 070 / 098：可选择性 / 实物期权
- 024 / 076：名字相近，但机制需进一步区分，不应直接合并
- 027 / 065 / 069：同属韧性簇，但各自关注点不同，应 Router 去重而非直接删除

## v0.2 应通过的回归条件

- 对 02050.HK 必须自动建立 company + security + share_class 三层。
- Quick Scan 不得把 A/H 折价直接当作公司基本面优势。
- 070 与 098 不得同时作为两份独立支持证据。
- 021 与 075 默认只展开一个。
- Deep Audit 汇总时必须输出 raw Material 数量与 independent mechanism clusters 数量。
- Adversarial Audit 必须至少攻击：
  - 机器人兑现程度
  - 高市占率与定价权之间的差异
  - 增长均值回归
  - A/H 折价是否可兑现

## Verdict

v0.1：可用，但 Router 不是真正配置驱动，且重复模型会放大信心。

v0.2 目标：对象分层 + 机制簇去重 + 证据独立性 + 跨公司 Model Independence Audit。
