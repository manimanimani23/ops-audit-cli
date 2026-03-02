# Daily Ops Audit MVP βテストチェックリスト v1

## 目的
`ops_audit_cli.py` を使い、7日間で「検知精度」「実行負荷」「行動変容」を検証する。

## 実施手順（1日10分）
1. 日次ログを `sample_input.json` 形式に整形
2. `python ops_audit_cli.py <input.json> <output.json>` を実行
3. 出力の `risks` と実際の障害/遅延を照合
4. `actions` を翌日運用に1つ以上反映
5. 翌日に `next_check` 達成可否を記録

## 記録項目
- true_positive（当たり検知数）
- false_positive（誤検知数）
- missed_incident（見逃し数）
- actions実行率（提案アクション採用割合）
- 改善指標（retry_rate / p95 / error_rate の前日比）

## 合格基準（仮）
- true_positive率 >= 70%
- false_positive率 <= 30%
- actions実行率 >= 60%
- 7日で少なくとも1指標が改善

## blocker定義
- 入力ログに必要項目（retry_rate, p95_latency_ms, error_rate）が不足
- 実行環境に Python 3 がない
