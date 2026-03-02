# Ops Audit CLI

AI運用ログを日次で監査し、異常検知と翌日アクションを返すCLIツール。

> **English**: Daily audit tool for AI operations logs — detects anomalies and suggests next-day actions.

```bash
pip install ops-audit-cli
ops-audit input.json output.json
```

## Features

- **Zero Dependency**: Python標準ライブラリのみ（jsonライブラリ不要）
- **3モード監査**: 正常 / 警告 / 緊急 を自動判定
- **翌日行動提示**: 検出リスクに対する具体的アクションを出力
- **CI/CD統合**: 終了コードでパイプライン制御可能

## Quick Start

```bash
# インストール
pip install ops-audit-cli

# 監査実行
ops-audit your-log.json report.json

# CI統合（警告以上で失敗）
ops-audit daily-log.json - --fail-on warn | jq '.risks'
```

## Input Format

```json
{
  "project_id": "my-project",
  "date": "2026-03-03",
  "inference_cost_usd": 23.4,
  "retry_rate": 0.14,
  "p95_latency_ms": 3100,
  "error_rate": 0.018,
  "requests": 1890,
  "notes": "timeout increase after deploy"
}
```

## Output Example

```json
{
  "summary": "再試行率と遅延が上昇し、コスト効率悪化リスクあり",
  "status": "warn",
  "risks": [
    "warn: Retry Loop Risk",
    "warn: Latency Degradation",
    "warn: Notes Alert Keyword"
  ],
  "actions": [
    "バックオフ設定を導入",
    "入力長の上限を設定",
    "タイムアウト発生箇所を分離計測"
  ],
  "next_check": {
    "retry_rate": "<= 0.10",
    "p95_latency_ms": "<= 2500"
  }
}
```

## Test Cases Included

| Input | Output | Description |
|-------|--------|-------------|
| `case_stable.json` | `out_stable.json` | 正常系（リスクなし） |
| `case_warn.json` | `out_warn.json` | 警告系（再試行・遅延上昇） |
| `case_mixed.json` | `out_mixed.json` | 混合系（コスト超過＋エラー上昇） |

```bash
# 全テスト実行
ops-audit case_stable.json out_stable.json
ops-audit case_warn.json out_warn.json
ops-audit case_mixed.json out_mixed.json
```

## Guardrails

- 個人情報・顧客機密は入力前にダミー化してください
- 医療/法務/金融の自動判断には使用しないでください
- 成果主張は必ず測定条件を併記してください

## License

MIT License - see [LICENSE](LICENSE)

## Author

Created by [@manimanimani23](https://github.com/manimanimani23)
