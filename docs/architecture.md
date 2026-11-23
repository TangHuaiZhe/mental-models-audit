# Architecture

## 三层结构

### Layer 1 — Router
`mental-models-audit/SKILL.md`

负责识别问题、选择模式、挑模型、去重与综合。

### Layer 2 — Module Skills
10 个模块，每个模块包含 10 个模型。模块 Skill 负责该学科视角下的预筛选，不直接替代原子模型。

### Layer 3 — Atomic Auditors
100 个原子 Skill。每个只负责一个模型，保持问题边界窄、输出一致、证伪明确。

## 为什么不机械跑100个长分析

模型之间高度相关。完整审计的正确做法是：
100个模型全部过相关性筛选，但只有 Material 模型展开。汇总阶段按底层机制去重，避免“同一事实被多个模型重复计票”。

## 数据与推理分离

本系统默认不负责制造事实。若与 deep-equity-research 联用：
- 原始披露/金融工具建立事实底稿
- 本系统引用事实做机制审计
- 数据缺失返回 unknown
- 不用模型常识代替公司证据

## 模型关系图

每个原子 Skill 的 `next_models` 形成有向图。Router 可以根据一次审计结果继续深挖，而不是按 001→100 线性调用。

## v0.2.1 — Router 与模型独立性

v0.2 增加一层集中式路由元数据：

- `config/model-routing-metadata.yaml`：每个模型的 analysis object、tags、mechanism cluster、overlap 与 independence score。
- `config/mechanism-clusters.yaml`：定义重复/近重复模型的主模型、辅助模型和最大展开数量。
- `config/replacement-candidates.yaml`：记录可能替换重复模型的新候选，不自动改课程编号。
- `tests/regression-cases.yaml`：跨行业回归测试矩阵。
- `docs/model-independence-audit.md`：Model Independence Audit 规则。

### 计权单位

100 个模型是 **blind-spot checklist**，不是 100 票投票。最终综合的基本计权单位是 **independent mechanism cluster**。

因此报告同时记录：

- raw Material models；
- independent mechanism clusters；
- duplicate/supporting models；
- shared vs independent evidence。

### 分析对象

Router 在选模型前必须先区分：

`business / company / industry / security / share_class / trading_counter / policy / strategy / analyst_self`。

对具体上市证券，必须区分公司质量与证券赔率。`share_class` 处理 A/H 等不同类别、证券形式或权利差异；`trading_counter` 处理同一股份的不同交易货币或柜台。腾讯 0700.HK 与 80700.HK 属于后者；ADR 应先核对存托与转换关系。交易柜台价差要考虑汇率、流动性与转换摩擦，不能记作两类股份套利。

### 资本配置与平台机制

AI 资本开支、算力预付款上升并伴随自由现金流受压时，触发 041/066/094/096/097 审计；098 只覆盖可分阶段或可放弃的部分。记录现金流定义与付款时点，避免单季负值直接推断长期回报。`config/router.yaml` 给出问题到模型的映射。

046 的单位成本下降、047 的参与者间价值增益、068 的跨角色互补依赖是三个不同机制。路由元数据和原子 Skill 记录各自 `trigger` / `anti_trigger`；只有不同证据支持不同问题时才可同时计入独立机制。

### 模型替换纪律

单次公司中的模型重叠不能直接触发删除。只有跨多个商业 archetype 的回归测试显示：高共选率、高同证据率、高同结论率、低增量信息率，才进入 Merge/Replace。


## v1.0 — Active Model Set

v1.0 将“课程概念集合”升级为经过跨行业回归测试的 active 100 模型集合。

### Active / Legacy 分离

- Router 只读取 `config/model-registry.yaml` 的100个 active 模型。
- 被替换、合并或收窄的旧模型保留旧路径，但作为 compatibility stub，不参与路由。
- 迁移关系统一记录在 `config/migration-map.yaml`。
- 原课程页面不删除；新模型发布在 `docs/model-set-v1/`。

### 7进7出

新增：Goodhart's Law、Explore–Exploit、Wright's Law、S-Curve、Capital Cycle、Power Law、Maturity Transformation / Duration Gap。

合并：旧021→075；旧091→067。

替换：旧015、019、053、057、058释放给更高增量模型。

收窄：070只保留反脆弱/凸性；分阶段投资选择权归098。

### 模块仍保持 10 × 10

v1.0允许模型跨原课程编号区间重新归类。模块是研究视角，不再等同于ID连续区间；每个模块仍恰好10个 active 模型。
