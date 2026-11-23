---
name: mental-models-audit
description: '使用《跨学科思维模型100讲》对应的100个原子审查器，对上市公司、行业、商业模式、政策、战略或投资命题进行跨学科审计。支持 quick-scan、deep-audit 与 adversarial-audit；输出相关性、证据、机制、反方、未知数、证伪条件和后续模型路由。'
metadata:
  version: "1.0.0"
---

# Mental Models Audit Router

## 角色

你不是在展示模型名词，而是在做 **模型选择、证据审查和结构化反证**。

默认研究对象可以是：

- 上市公司
- 行业
- 商业模式
- 政策/制度
- 战略命题
- 已形成的投资 thesis

若与 `deep-equity-research` 联用，事实与数字必须继承其数据源、时间口径与零虚构纪律。

## Model Set v1.0

v1.0 是经过多 archetype 回归测试后的首个正式模型集合。Active model 以 `config/model-registry.yaml` 为唯一清单；旧模型与旧 URL 通过 `config/migration-map.yaml` 保留可追踪性。

- **100 active models 固定为审计器集合，不等于100票。**
- 合并模型的旧机制由新主模型吸收；被替换模型保留 legacy 文件但不再参与 Router。
- 新模型若来自回归测试而非原 Notion 课程，课程页使用 GitHub v1.0 页面作为当前发布源。
- `MODEL_SET_CHANGELOG.md` 记录 Keep / Narrow / Merge / Replace 与证据。

## 核心原则

1. **模型是工具，不是答案。** 不得为了“用满100个模型”强行制造内容。
2. **先判相关性，再分析。** 每个原子模型先给 `Material / Secondary / Not material`。
3. **独立证据优先。** 多个模型如果依赖同一事实，不得当成多份独立确认。
4. **机制优先于类比。** 必须解释因果/博弈/反馈机制。
5. **反方必须真实。** 最强反例不能是稻草人。
6. **显式未知。** 证据不足时输出 unknowns，不用故事补齐。
7. **可证伪。** Material 模型至少给一个可观察的 falsification condition。
8. **避免重复计数。** 模型重叠时合并为机制簇，而不是重复加分。


## 分析对象分层

在选择模型前，先明确当前在分析什么：

- `business`：业务本身是否创造价值；
- `company`：企业组织、资本配置、竞争优势与财务质量；
- `industry`：行业结构、供需、技术和竞争均衡；
- `security`：证券价格、赔率和估值；
- `share_class`：A/H、不同投票权或 ADR 等证券形式、股份权利及转换关系需单独分析的情形；
- `trading_counter`：同一股份的不同计价或交收货币柜台，例如腾讯 0700.HK 与 80700.HK；比较交易成本、汇率和流动性，但不把柜台当作新股权类别；
- `policy`：政策和制度；
- `strategy`：战略选择；
- `analyst_self`：分析者自身偏差。

**禁止把“好公司”直接推导为“好证券”。** 对具体股票研究，至少同时建立 `company` 与 `security` 两层；存在不同股份权利或证券形式时，核对后追加 `share_class`；同一股份有多个交易柜台时追加 `trading_counter`。ADR 是否构成独立证券形式，应核对存托安排、转换与投票权，不能仅凭代码判断。

## 资本配置审计触发

当 AI 算力采购、资本开支或预付款明显上升，并伴随自由现金流受压、转负或净现金下降时，执行 `config/router.yaml` 的 `capital_allocation_audit`。分别调用 041 机会成本、066 军备竞赛、094 战略资源配置、096 战略取舍、097 情景规划；只有支出确实可分阶段、延后或放弃时，才用 098 实物期权分析可选性。先核对现金流口径、付款时点、核心业务表现及 AI 单位经济；单季负自由现金流只是触发信号。

046 规模经济、047 网络效应与 068 生态系统分别审查成本曲线、参与者间价值增益、跨角色互补依赖。每项都要检查原子 Skill 的 `trigger` 与 `anti_trigger`，不得仅因平台规模大而同时判为 Material。

## 模型独立性纪律

100个模型是盲点清单，不是100票投票。读取：

- `config/model-routing-metadata.yaml`
- `config/mechanism-clusters.yaml`
- `config/replacement-candidates.yaml`

若多个模型属于同一 mechanism cluster：

1. 默认只展开主模型；
2. 第二模型只有在回答不同子问题且拥有独立证据时才展开；
3. 汇总时只能算一个底层机制；
4. 长期通过 `docs/model-independence-audit.md` 的跨公司回归结果决定是否合并或替换模型。

## 三种模式

### quick-scan

适合首次研究。

- 从100模型中选约10–20个
- 至少覆盖：认识论/统计、商业经济、系统、博弈或战略、心理偏差
- 只选择能改变结论或下一步研究优先级的模型
- 最终给出：Top positive mechanisms、Top risks、Critical unknowns、Next evidence

### deep-audit

适合高确信度 thesis、重大仓位前或年度复盘。

- 100模型全部经过相关性判断
- Not material 项只需一句原因，禁止硬写
- Material 项完整执行审查
- 汇总时将相似模型聚为机制簇
- 输出覆盖率：哪些关键机制已有证据，哪些仍是盲区

### adversarial-audit

适合“攻击已有结论”。

- 默认 thesis 可能错
- 优先调用反演、基准率、竞争、替代、尾部风险、系统陷阱、制度激励、护城河侵蚀、情景与证伪相关模型
- 主动寻找能让 bull case 失效的证据
- 不为了唱反调而反对；证据不足时明确写 unknown

## 路由流程

1. 定义研究对象与 thesis。
2. 列出当前事实底稿与数据缺口。
3. 判断问题类型：事实 / 因果 / 风险 / 商业质量 / 组织制度 / 战略。
4. 读取 `config/model-registry.yaml` 确认100模型清单，再读取 `config/model-routing-metadata.yaml` 按 analysis object、tags、机制簇与重叠关系筛选候选模型。
5. 读取 `config/mechanism-clusters.yaml` 去重后，运行选中的原子 Skill。
6. 同一机制簇默认只保留一个主模型；只有第二模型回答不同子问题且依赖独立证据时才允许并行展开。
7. 检查模型冲突与证据独立性：哪些模型给出相反建议？哪些只是同一事实的重复表达？
8. 输出统一审计报告，并按机制簇而不是模型数量计权。
9. 若与 deep-equity-research 联用，把结果映射回：商业模式、护城河、财务质量、增长、估值、反方、证伪与跟踪清单。
10. 若本次为Smoke Test或回归测试，把共选率、同证据率、同结论率和增量信息率写入 Model Independence Audit。

## 统一输出

每个原子 Skill 至少返回：

- model
- relevance
- question
- evidence_for
- evidence_against
- mechanism
- implication
- bull_case_impact
- bear_case_impact
- unknowns
- falsification
- confidence
- next_models

见 `schema/audit-output.yaml`。

## 停止规则

满足任一条件可停止继续调用模型：

- 新模型只重复既有机制，不增加信息
- 关键结论受制于数据缺口，继续推理不能提高质量
- 已得到足以改变行动的证据
- 当前决策高度可逆，继续分析的信息边际价值低

不要把“100个模型”变成新的 Analysis Paralysis。
