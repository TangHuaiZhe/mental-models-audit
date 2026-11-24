# Calibration Phase：Milestone 1–2 + Contract Hardening

## 权威来源与发布方向

GitHub `main` 中的 `docs/course/`、`skills/`、`config/` 和 `schema/` 是唯一事实来源。Notion 与 GitHub Pages 是单向发布目标；Notion 上的修改不会回写仓库。`config/model-registry.yaml` 的 `source` 现在指向课程文件，`path` 指向可执行审查技能。旧 Notion 链接转入 `content-manifest.yaml` 的页面映射。

当前 001–100 的 ID 与课程、技能文件被冻结。版本号分开记录在 `config/versions.yaml`：模型集合 1.0.0 不随路由或输出契约迭代而升级。历史 `tests/regression-cases.yaml` 保留为案例索引，不宣称是 100×公司完整标注。

## 内容清单与发布

`content-manifest.yaml` 每项记录模型 ID、Notion 页面 ID、课程路径、技能路径、课程 SHA-256、映射核验状态和最后同步时间。旧 registry 只提供 92 个页面 ID。2026-11-24 只读核对 Notion 课程总页的 100 条子页面清单后，补齐其余 8 个；旧 ID 全部与目录一致，新 8 页另逐页确认标题。清单的 `verified` 表示页面身份核对完成，不表示课程正文已同步。课程哈希取 GitHub 文件原始字节；技能路径用于保持可执行知识来源清晰，Notion 页面同步的是课程正文。技能更新通过 GitHub 链接供读者查阅，当前不在 Notion 中复制技能全文。

课程正文发生有意修改后，先运行 `python scripts/refresh_content_manifest.py --write` 更新受影响课程的 SHA-256；CI 会先运行不带 `--write` 的检查模式，发现 stale hash 就直接失败。随后运行 `python scripts/validate_calibration.py` 校验数量、ID、路径、页面映射唯一性、哈希和配置结构。`python scripts/publish_notion.py` 是无需凭据的预览，输出逐页状态到 `.notion-publish-state.json`。页面映射现已核对；凭据只放在 `NOTION_API_KEY` 环境变量或 GitHub 环境密钥。单页试运行可用 `--model-id 001`；`--apply` 才写入目标页。发布后回读检查哈希标记，成功时间写入状态文件；`--write-manifest` 也将成功项的 `last_sync` 写回本地清单。CI 的更新清单在运行产物中，不会自动提交到 `main`。

写入使用 Notion API 2026-03-11 的 Markdown `replace_content`。发布器会去掉 GitHub 课程文件最顶部的 H1，因为 Notion 页面标题已经单独存在，避免同步后出现重复标题；其余课程 Markdown 结构保留。首次写入会替换目标页现有正文，因此必须先核对映射和页面内容；API 默认拒绝删除子页面或数据库，发布器不会绕过保护。目标页不完整、出现转换警告或回读缺少哈希标记时记为失败。429 与 5xx 临时错误有限重试，失败页留在状态文件，下一次可重跑。远端哈希标记相同则跳过；这是内容来源幂等判断，无法识别 Notion 上带有旧标记的人工改动，因此正式发布前应避免在 Notion 编辑。

GitHub Actions 的校验在 PR、`main` 推送和手动触发时运行。发布任务仅在仓库变量 `NOTION_PUBLISH_ENABLED=true` 且 `main` 推送或手动选择 `apply` 时执行，且要求 `notion-publication` 环境中配置 `NOTION_API_KEY`。PR 不写 Notion。运行产物分别保存预览和发布状态。发布任务在工作流凭据与首次实测完成前应保持关闭。

## 数据契约

`schema/audit-output.yaml` v5 将 evidence 拆成事实时点、指标期间、发布时间、获取时间、claim type、source type、质量和口径；同时保留旧的单一 `confidence` 兼容字段，并新增 `evidence_confidence / mechanism_confidence / underwriting_confidence` 三维置信度。`object_summaries` 继续分开 company、security、share_class、industry。

`config/model-relationships.yaml` 是模型对关系的 canonical source，支持 `duplicate / complementary / object_specific / prerequisite / supports / commonly_confused_with / conflicts_with`。`config/mechanism-clusters.yaml` v4 只负责候选分组和展示预算，不再承担硬去重语义。特别地，024 Leverage ↔ 076 Leverage Points、031 Base Rate ↔ 054 Base Rate Neglect 明确为 `complementary`。`config/router.yaml` v5 已移除统一的 `same_cluster_already_selected: -3`；只有 `duplicate` 且同一对象、命题、证据成立时才硬去重。

`schema/benchmark.yaml` v2 是完整 100×case 标注模板。除了 relevance 和 evidence，还记录 `incremental_information`、`decision_impact`、共享证据、同结论关系和 pairwise independence，以支持后续 CoSelection / SameEvidence / SameConclusion / IncrementalInformation 以及消融测试。只有全部100模型完成裁决且证据引用完整的案例，才能进入精确 benchmark 聚合。
