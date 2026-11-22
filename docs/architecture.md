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

## v0.2 — Router 与模型独立性

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

`business / company / industry / security / share_class / policy / strategy / analyst_self`。

对具体上市证券，禁止把“好公司”直接等价为“好证券”；存在 A/H、ADR 或不同股权类别时，必须显式增加 `share_class` 层。

### 模型替换纪律

单次公司中的模型重叠不能直接触发删除。只有跨多个商业 archetype 的回归测试显示：高共选率、高同证据率、高同结论率、低增量信息率，才进入 Merge/Replace。
