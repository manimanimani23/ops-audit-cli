# Agent Economy MVP: Daily Ops Audit

AI運用ログを日次で監査し、異常検知と翌日アクションを返す最小MVPです。

## Files
- `ops-audit-schema-v1.json`: 入力スキーマ
- `ops-audit-rules-v1.md`: 監査ルール10本
- `ops_audit_cli.py`: ルール適用CLI（Python標準ライブラリのみ）
- `sample_input.json`: 動作確認用サンプル入力
- `sample_output.json`: CLI実行で生成したサンプル出力
- `beta-test-checklist-v1.md`: 7日βテストの評価項目

## Quick Start
1. 日次ログを以下のJSONに整形
2. （任意）`ops-audit-schema-v1.json` でスキーマ検証
3. CLIで監査レポート生成
   - `py -3 ops_audit_cli.py sample_input.json sample_output.json`
4. 出力の `risks` / `actions` を翌日運用に反映

### Test Cases
- `case_stable.json` → `out_stable.json`: 正常系（リスクなし）
- `case_warn.json` → `out_warn.json`: 警告系（再試行・遅延上昇）
- `case_mixed.json` → `out_mixed.json`: 混合系（コスト超過＋エラー上昇）

```bash
# 全テストケースを一括実行
py -3 ops_audit_cli.py case_stable.json out_stable.json
py -3 ops_audit_cli.py case_warn.json out_warn.json
py -3 ops_audit_cli.py case_mixed.json out_mixed.json
```
```json
{
  "project_id": "demo-a",
  "date": "2026-02-26",
  "inference_cost_usd": 23.4,
  "retry_rate": 0.14,
  "p95_latency_ms": 3100,
  "error_rate": 0.018,
  "requests": 1890,
  "notes": "timeout increase after deploy"
}
```

### Expected High-level Output
- Summary: 再試行率と遅延が上昇し、コスト効率悪化リスクあり
- Risks:
  - warn: Retry Loop Risk
  - warn: Latency Degradation
  - warn: Notes Alert Keyword
- Actions:
  1. バックオフ設定を導入
  2. 入力長の上限を設定
  3. タイムアウト発生箇所を分離計測
- Next Check:
  - retry_rate <= 0.10
  - p95_latency_ms <= 2500

## Guardrails
- 個人情報・顧客機密は入力禁止（ダミー化必須）
- 医療/法務/金融の自動判断には使用しない
- 成果主張は測定条件を併記する

## Next
- CLI実装（schema validation + rule engine）
- Free/Proの呼び出し回数制限
- 7日βテストで閾値チューニング
