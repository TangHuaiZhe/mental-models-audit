# Mental Models Audit

> **Active Model Set: v1.0.0** — 首个基于跨行业 Regression Tests 完成换血的正式100模型集合。

本仓库收录《跨学科思维模型100讲》课程，并将每讲对应的模型做成可执行的公司与行业研究审查技能。

## 目标

课程用于理解模型的原理与边界；审查技能用于把模型应用到具体研究问题。每个技能明确：

- 什么时候值得调用
- 它试图回答什么
- 需要什么证据
- 如何推理
- 什么结果支持或反对当前研究论点
- 什么证据会证伪
- 与哪些模型应继续联动

## 三种运行模式

1. **quick-scan**：自动选择约 10–20 个高相关模型，适合首次研究。
2. **deep-audit**：100 个模型逐项过一遍，只允许 Material / Secondary / Not material 三种相关性判定。
3. **adversarial-audit**：默认当前 thesis 可能错，优先寻找反例、脆弱点、失效路径和被忽略的博弈反应。

## 目录

- `SKILL.md`：总控路由器
- `modules/`：10 个模块级 Skill
- `skills/`：100 个原子审查 Skill
- `schema/`：统一输出格式
- `config/`：模型注册表与路由
- `modes/`：三种运行模式说明
- `docs/`：架构与 deep-equity-research 集成说明
- `examples/`：输出模板
- `docs/course/`：100 讲课程正文
- `mkdocs.yml`：课程网站的导航、搜索与主题配置

## 与 deep-equity-research 的关系

`deep-equity-research` 负责事实底稿、财务、估值、来源纪律和最终研究报告；本系统负责**跨学科模型审计**。两者不重复：

> deep-equity-research 获取事实与完成估值  
> → mental-models-audit 选择模型并审查 thesis  
> → 将高价值发现、反方证据、未知数和证伪条件回填研究报告

## 在线课程（GitHub Pages）

[阅读《跨学科思维模型100讲》](https://tanghuaizhe.github.io/mental-models-audit/)

站点使用 MkDocs Material，由 `.github/workflows/pages.yml` 在 `main` 更新后自动构建并部署。

课程正文位于 `docs/course/`，共 100 讲；左侧导航按 10 个学科模块组织，并提供全文搜索、明暗主题、上一讲/下一讲以及课程与对应 Audit Skill 的链接。

GitHub Pages 已配置为由 GitHub Actions 发布。后续推送到 `main` 会自动重新构建网站。


## Model Set 版本治理

- Active models: `config/model-registry.yaml`
- v0.2.1 → v1.0 migration: `config/migration-map.yaml`
- Change rationale: `MODEL_SET_CHANGELOG.md`
- Legacy course/skill files继续保留，避免旧链接失效。
