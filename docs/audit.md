# Mental Models Audit

**Active Model Set: v1.0.0**。Active 100 models 以 `config/model-registry.yaml` 为准；旧模型通过 `config/migration-map.yaml` 保留。

这套站点同时包含两层内容：

1. **课程层**：解释 100 个模型是什么、为什么有效、边界在哪里。
2. **Skill 层**：把每个模型改造成可执行的公司/行业审查器。

## 三种模式

- **Quick Scan**：自动选择约 10–20 个最相关模型。
- **Deep Audit**：100 个模型全部判定 Material / Secondary / Not material，只展开 Material 项。
- **Adversarial Audit**：专门攻击当前 thesis，寻找反例、竞争反应、系统风险和证伪条件。

[查看总控 Skill 源码](https://github.com/TangHuaiZhe/mental-models-audit/blob/main/SKILL.md)

课程页面底部会链接到对应的原子 Audit Skill。
