# Calibration Phase：Milestone 1–2

## 权威来源与发布方向

GitHub `main` 中的 `docs/course/`、`skills/`、`config/` 和 `schema/` 是唯一事实来源。Notion 与 GitHub Pages 是单向发布目标；Notion 上的修改不会回写仓库。`config/model-registry.yaml` 的 `source` 现在指向课程文件，`path` 指向可执行审查技能。旧 Notion 链接转入 `content-manifest.yaml` 的页面映射。

当前 001–100 的 ID 与课程、技能文件被冻结。版本号分开记录在 `config/versions.yaml`：模型集合 1.0.0 不随路由或输出契约迭代而升级。历史 `tests/regression-cases.yaml` 保留为案例索引，不宣称是 100×公司完整标注。

## 内容清单与发布

`content-manifest.yaml` 每项记录模型 ID、Notion 页面 ID、课程路径、技能路径、课程 SHA-256、映射核验状态和最后同步时间。旧 registry 只提供 92 个页面 ID。2026-11-24 只读核对 Notion 课程总页的 100 条子页面清单后，补齐其余 8 个；旧 ID 全部与目录一致，新 8 页另逐页确认标题。清单的 `verified` 表示页面身份核对完成，不表示课程正文已同步。课程哈希取 GitHub 文件原始字节；技能路径用于保持可执行知识来源清晰，Notion 页面同步的是课程正文。技能更新通过 GitHub 链接供读者查阅，当前不在 Notion 中复制技能全文。

运行 `python scripts/validate_calibration.py` 校验数量、ID、路径、页面映射唯一性、哈希和配置结构。`python scripts/publish_notion.py` 是无需凭据的预览，输出逐页状态到 `.notion-publish-state.json`。页面映射现已核对；凭据只放在 `NOTION_API_KEY` 环境变量或 GitHub 环境密钥。单页试运行可用 `--model-id 001`；`--apply` 才写入目标页。发布后回读检查哈希标记，成功时间写入状态文件；`--write-manifest` 也将成功项的 `last_sync` 写回本地清单。CI 的更新清单在运行产物中，不会自动提交到 `main`。

写入使用 Notion API 2026-03-11 的 Markdown `replace_content`，保留课程 Markdown 结构。首次写入会替换目标页现有正文，因此必须先核对映射和页面内容；API 默认拒绝删除子页面或数据库，发布器不会绕过保护。目标页不完整、出现转换警告或回读缺少哈希标记时记为失败。429 与 5xx 临时错误有限重试，失败页留在状态文件，下一次可重跑。远端哈希标记相同则跳过；这是内容来源幂等判断，无法识别 Notion 上带有旧标记的人工改动，因此正式发布前应避免在 Notion 编辑。

GitHub Actions 的校验在 PR、`main` 推送和手动触发时运行。发布任务仅在仓库变量 `NOTION_PUBLISH_ENABLED=true` 且 `main` 推送或手动选择 `apply` 时执行，且要求 `notion-publication` 环境中配置 `NOTION_API_KEY`。PR 不写 Notion。运行产物分别保存预览和发布状态。发布任务在工作流凭据与首次实测完成前应保持关闭。

## 数据契约

`schema/audit-output.yaml` v4 在旧字段上追加证据的时点、期间、事实类型、来源类型、质量与口径说明；`confidence_basis` 说明置信度，`object_summaries` 分开 company、security、share_class、industry。缺失新字段读作 unknown，旧 v3 输出仍可读。交易柜台继续作为 security 的维度，不等于 share_class。

`config/mechanism-clusters.yaml` v3 给关系定义 `duplicate`、`complementary`、`object-specific` 和去重策略。旧 `max_expanded` 只控制展开预算，不自动代表票数。相同对象、命题和证据的 duplicate 只计一次；互补模型须有独立子问题与证据；对象专属关系不可跨公司、证券、股权类别和行业去重。`config/router.yaml` v4 采用这些语义。

`schema/benchmark.yaml` 是完整 100×公司标注的**模板**，要求证据 ID、时点、来源、独立性和审核信息。本阶段未填矩阵，也没有重新计算历史近似结果；只有 `all_models_adjudicated=true` 且证据齐全的案例才可进入精确基准统计。
