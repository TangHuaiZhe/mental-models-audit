# Model Set v1.0 Changelog

## Why v1.0

v1.0 is the first model-set revision driven by cross-archetype regression tests rather than by course symmetry. The objective is higher **independent incremental information** for company, industry and security research.

Regression archetypes used in the decision:
- industrial manufacturing
- brand consumer
- platform internet
- semiconductor manufacturing
- SaaS / network infrastructure
- advanced manufacturing
- banking / financial institution
- innovative biotech

## Merge

### 021 → 075
Old **守恒、存量与流量** and old **存量与流量模型** repeatedly asked the same stock/flow question. Their mechanism is consolidated into **075 存量—流量动力学**.

### 091 → 067
Old **路径依赖与制度惯性** is an application of the broader path-dependence mechanism. It is consolidated into **067 路径依赖与锁定**.

## Narrow

### 070
Old **反脆弱与可选择性** overlapped materially with 098 Real Options. v1.0 narrows 070 to **反脆弱、凸性与非对称收益**. Staged continuation/abandonment decisions belong to 098.

## Replace

| ID | v0.2.1 | v1.0 | Regression rationale |
|---|---|---|---|
| 015 | 思想实验 | Goodhart's Law | Thought experiment is primarily a reasoning technique and overlaps counterfactual/scenario stress tests; Goodhart added clear incremental value in channel/KPI audits. |
| 021 | 守恒、存量与流量 | Wright's Law | Old mechanism merged into075; learning curves were independently material in semiconductor and battery manufacturing. |
| 034 | 大数定律 | Power Law / Pareto | LLN is foundational but rarely decision-changing as an atomic company auditor; power-law concentration materially changes biotech/platform analysis. |
| 042 | 边际效用 | Maturity Transformation / Duration Gap | Marginal utility was rarely material in fundamental audits; banks exposed a missing asset-liability repricing mechanism. |
| 053 | 可得性启发 | S-Curve / Diffusion | Availability bias was usually subsumed by stronger analyst-bias checks; adoption-stage analysis repeatedly mattered in technology/advanced manufacturing. |
| 057 | 沉没成本谬误 | Explore–Exploit | Sunk cost is largely covered by opportunity cost/inversion; explore–exploit independently changed capital-allocation analysis in platform and biotech cases. |
| 091 | 路径依赖与制度惯性 | Capital Cycle | Old mechanism merged into067; capital-cycle dynamics independently mattered in AI, semiconductors and batteries. |

## Keep despite similarity

- 046 Scale Economies, 047 Network Effects, 068 Ecosystem: regression on platform/network businesses showed distinct mechanisms.
- 027 Safety Margin, 065 Robustness, 069 Diversity/Resilience: may share evidence but ask different failure-resilience questions.
- 041 Opportunity Cost and 096 Strategic Tradeoffs: one prices alternatives, the other evaluates mutually incompatible activity systems.
- 066 Arms Race and 091 Capital Cycle: strategic compulsion to invest is different from the later supply/ROIC cycle.

## Compatibility

Old skill and course files are not deleted. `config/migration-map.yaml` is the compatibility source of truth. Active models are defined only by `config/model-registry.yaml`.
