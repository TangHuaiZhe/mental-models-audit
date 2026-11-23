# MODEL SET CHANGELOG

## v1.0.0-rc1

### Evidence base
修订基于工业制造、品牌消费、平台互联网、半导体制造、SaaS/网络基础设施、先进制造、银行、创新药等多个 archetype 的回归测试。

### Merge
- 021 守恒、存量与流量 → 075 Stock–Flow Dynamics。
- 091 制度路径依赖 → 067 Path Dependence & Lock-in。

### Narrow
- 070 反脆弱与可选择性 → **反脆弱、凸性与非对称收益**；分阶段投资选择权归 098 Real Options。

### Replace / Add
- 015 → Goodhart's Law
- 019 → Explore–Exploit Tradeoff
- 021 slot → Wright's Law / Experience Curve
- 053 → S-Curve / Diffusion of Innovation
- 057 → Capital Cycle
- 058 → Power Law / Pareto Distribution
- 091 slot → Maturity Transformation / Duration Gap

### Module rebalance
- 036 Selection/Survivorship Bias → Module 02
- 067 Path Dependence → Module 02
- 044 Incentive/Principal-Agent → Module 06
- 090 Identity/Norms → Module 06

### Compatibility
旧课程页面不删除；旧 Skill 路径保留为兼容迁移入口。Router 只读取 active `config/model-registry.yaml`。
