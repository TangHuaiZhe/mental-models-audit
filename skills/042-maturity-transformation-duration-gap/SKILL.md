---
name: mm-042-maturity-transformation-duration-gap
description: '使用 Model Set v1.0 的「期限转换与久期缺口（Maturity Transformation / Duration Gap）」审查公司、行业或投资 thesis。先判相关性，再检查证据、机制、反例、未知数、证伪条件与证据独立性。'
metadata:
  model_id: "042"
  module: "05"
  version: "1.0.0"
  model_set: "1.0.0"
---

# 042 期限转换与久期缺口（Maturity Transformation / Duration Gap）

课程页面：https://tanghuaizhe.github.io/mental-models-audit/course/042-maturity-transformation-duration-gap/

## 何时调用

当银行、保险、REIT、地产或高负债企业的资产与负债期限、重定价周期或流动性承诺不匹配，可能改变利差、流动性和偿付风险时调用。

若它不会改变经营判断、风险判断、估值或下一步证据优先级，标记为 `Not material` 并停止展开。

## 审查问题

1. 资产与负债的合同期限、实际久期和重定价周期分别是多少？
2. 利率上升/下降100bp时，资产收益率与负债成本谁先重定价，净息差如何变化？
3. 短期可赎回/可提款负债支持了多少长期或低流动性资产？
4. 压力情景下需要变现资产时，账面久期风险会不会转化成真实损失或流动性缺口？
5. 资本、流动性缓冲和稳定负债来源是否足以覆盖期限错配？

## 证据要求

- 优先引用公司、交易所、监管原始披露、可靠结构化财务数据、行业一手数据或可复核事实。
- 区分：已披露事实 / 外部证据 / 分析判断 / 前瞻假设。
- 不允许用模型名称、类比或行业口号本身充当证据。
- 关键事实缺失时写入 `unknowns`，不要补故事。
- 必须记录 `evidence_independence` 与 `incremental_information`，避免与邻近模型重复计票。

## 执行步骤

1. 给出相关性：`Material | Secondary | Not material`。
2. 写出本模型试图回答的唯一核心问题。
3. 分列支持与反对证据，并注明来源/期间。
4. 明确底层机制，而不是只做类比。
5. 说明对收入、利润率、ROIC、竞争位置、资本需求、尾部风险、现金流或估值中的哪一项产生影响。
6. 给出最强反例或边界条件。
7. 写出至少一个可观察、尽量带时间/阈值的证伪条件。
8. 给出 0–100 的置信度。
9. 检查是否与其他模型共享同一证据或机制。
10. 推荐 0–3 个下一模型；若只是重复机制则不推荐。

优先联动：`024`、`033`、`075`。

## 输出

严格遵循 `../../schema/audit-output.yaml`。若为 `Not material`，只输出 model、relevance、reason，可省略其余字段。

## 边界

不要把所有负债风险都归为久期缺口。若核心问题只是杠杆倍数或尾部损失，优先024/033；本模型要求存在期限、重定价或流动性错配。
