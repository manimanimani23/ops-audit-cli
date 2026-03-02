# Daily Ops Audit MVP - β Test Report (2026-02-26)

## Scope
`ops_audit_cli.py` の最小実装を3ケースで手動検証し、検知ロジックの妥当性を確認。

## Test Cases

### 1) Stable Case (`case_stable.json`)
- 入力: retry 0.04 / p95 1200ms / error 0.004
- 期待: リスクなし（安定）
- 結果: **PASS**
- 出力: `out_stable.json`

### 2) Warning Burst Case (`case_warn.json`)
- 入力: retry 0.13 / p95 2900ms / error 0.021 / notes: timeout after deploy
- 期待: retry・latency・error・notes の複合警告
- 結果: **PASS**
- 出力: `out_warn.json`

### 3) Mixed Signal Case (`case_mixed.json`)
- 入力: retry 0.11 / p95 1800ms / error 0.010 / notes: rate limit 429
- 期待: retry + notes 警告
- 結果: **PASS**
- 出力: `out_mixed.json`

## Findings
- 最小MVPとしては、主要しきい値（retry/p95/error）に対する検知は動作。
- `notes` キーワード由来の補助警告も機能。
- 現状は `warn/info` 中心で、`critical` 判定と前日比較（R9）は未実装。

## Next Actions (<= 60 min task candidates)
1. `critical` レベル判定を導入（error/retry/latencyの上位閾値）。
2. 前日比較用の `prev_day` 入力を追加し Throughput Collapse を実装。
3. README に「v1実装済みルール / 未実装ルール」を明記して公開時の期待値を統一。

## Safety
- 個人情報・決済・規約抵触行為なし。
