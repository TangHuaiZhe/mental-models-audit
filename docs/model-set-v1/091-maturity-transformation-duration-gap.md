# 091｜期限转换与久期缺口

> **Model Set v1.0 新增/修订模型。** GitHub版本是当前 active audit 规范；被替换的旧《跨学科思维模型100讲》页面仍保留为 legacy。

## 一句话定义

金融机构用不同期限和流动性的负债支持资产，资产负债重定价速度差异形成利率和流动性风险。

## 核心机制

短期负债可能先涨成本而长期资产收益率滞后，或存款可随时流出而贷款难以变现，从而影响NIM、流动性和资本。

## 典型应用

- 商业银行存款与长期贷款。
- 保险负债与长久期资产。
- REIT和地产的短债长投。

## 何时调用

对应原子审查器：[`skills/091-maturity-transformation-duration-gap/SKILL.md`](https://github.com/TangHuaiZhe/mental-models-audit/blob/model-set-v1/skills/091-maturity-transformation-duration-gap/SKILL.md)

## 审计纪律

- 模型名称不是证据。
- Material 必须给出独立证据、机制、边界和证伪条件。
- 与其他模型共享同一事实时不得重复计权。
- 先区分 business / company / industry / security / share_class / trading_counter / policy / strategy / analyst_self。

## 迁移

详见 `config/migration-map.yaml`。
