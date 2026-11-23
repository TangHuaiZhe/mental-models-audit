# Model Independence Audit

## 目的

100个模型不是100票。系统追求的是**独立增量信息**，而不是模型数量。

## 真重复的判定

只有同时满足以下三项，才进入“合并/替换”候选：

1. **Mechanism overlap**：底层机制高度相同。
2. **Evidence overlap**：分析时依赖基本相同的事实或数据。
3. **Decision overlap**：最终改变同一个决策变量或证伪条件。

单次公司中重叠，不等于全局重复。必须跨行业回归测试。

## 四个统计指标

每对候选模型记录：

- `co_selection_rate`：两者同时被选中的比例。
- `same_evidence_rate`：依赖同一核心证据的比例。
- `same_conclusion_rate`：导向同一结论的比例。
- `incremental_information_rate`：第二个模型真正增加新机制、新证据或新行动的比例。

建议替换阈值见 `config/replacement-candidates.yaml`。

## 回归测试组合

至少覆盖：

1. 工业制造：三花智控
2. 品牌消费：贵州茅台
3. 平台互联网：腾讯
4. SaaS / 网络基础设施：Cloudflare
5. 半导体制造：台积电
6. 新能源制造：宁德时代
7. 金融机构：大型银行
8. 创新药：研发型生物科技公司

前三例已记录在 `tests/results/`：三花约 26 个 Material 对应约 8 个独立机制簇；茅台 17 对应 17；腾讯的既有审计估计约 32 对应约 29。腾讯数字是近似汇总，尚无逐项可复算的 100 模型评分表，不应作为精确独立性统计或替换阈值依据。

腾讯案例支持收窄 046/047/068 的触发边界，并为“探索—利用权衡”提供强候选信号、为“资本周期”提供中强候选信号。竞争者共同投入解释军备竞赛，扩产后行业资本回报变化属于资本周期；两者不应共用同一结论。候选优先级是后续检验顺序，不等于正式纳入 100 讲。

## 结果分类

- **Keep**：独立机制清晰。
- **Narrow**：保留但收窄定义，避免与邻近模型重复。
- **Merge**：合并为一个Core Model。
- **Replace**：释放编号，引入更高增量价值的新模型。

## 关键纪律

在完成至少 6 个不同商业 archetype 的回归测试前，不正式重排100讲编号。Router 可以先进行机制簇去重，但课程层保持稳定。


## v1.0 Revision Decision

跨 archetype 回归已经覆盖：工业制造、品牌消费、平台互联网、SaaS/网络基础设施、半导体制造、先进制造、银行、创新药。

因此 v1.0 不再只维护候选池，而正式执行第一次 model-set revision。

### 强新增信号

- Wright's Law：TSMC、CATL
- Capital Cycle：TSMC、CATL、AI基础设施
- S-Curve：CATL、Cloudflare、创新扩散问题
- Goodhart's Law：茅台渠道/KPI
- Explore–Exploit：腾讯、创新药
- Power Law：创新药与集中度经济
- Maturity Transformation / Duration Gap：银行

### 高重叠/低增量

- 021 vs 075：合并
- 067 vs 091：合并
- 070 optionality vs 098 real options：070收窄
- 053 Availability、057 Sunk Cost、058 Endowment/Mental Accounting：在公司/行业基本面审计中长期独立增量低
- 015 Thought Experiment、019 Fact–Value：保留为legacy课程方法论，但退出active公司审查集合

### 统计纪律

回归中的 Material 数量只用于诊断 Router，不用于给 thesis 投票。active set 的选择依据仍是机制独立性、证据独立性和决策增量。
