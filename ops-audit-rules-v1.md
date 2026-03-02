# Ops Audit Rules v1

日次監査ルール（優先度順）です。各ルールは `status: ok|warn|critical` を返す想定。

## R1. Error Rate Spike
- 条件: `error_rate >= 0.05` で `critical`
- 条件: `error_rate >= 0.02` で `warn`
- 推奨アクション: 失敗タイプ上位3件を抽出し、当日変更との差分確認

## R2. Retry Loop Risk
- 条件: `retry_rate >= 0.25` で `critical`
- 条件: `retry_rate >= 0.12` で `warn`
- 推奨アクション: 再試行回数上限とバックオフを設定

## R3. Latency Degradation
- 条件: `p95_latency_ms >= 5000` で `critical`
- 条件: `p95_latency_ms >= 2500` で `warn`
- 推奨アクション: 入力長分布とタイムアウト設定を点検

## R4. Cost Overrun (Absolute)
- 条件: `inference_cost_usd >= 50` で `critical`
- 条件: `inference_cost_usd >= 20` で `warn`
- 推奨アクション: 高コスト経路上位を特定しキャッシュ適用

## R5. Cost Efficiency Drop
- 前提: `requests` が存在
- 条件: `cost_per_request = inference_cost_usd / max(requests,1)`
- 条件: `cost_per_request >= 0.03` で `critical`
- 条件: `cost_per_request >= 0.015` で `warn`

## R6. Combined Failure Risk
- 条件: `retry_rate >= 0.12` かつ `error_rate >= 0.02` で `critical`
- 推奨アクション: プロンプト/ツール失敗を分離して原因切り分け

## R7. Latency-Cost Coupled Risk
- 条件: `p95_latency_ms >= 2500` かつ `inference_cost_usd >= 20` で `critical`

## R8. Silent Failure Suspicion
- 前提: `requests` が存在
- 条件: `requests > 0` かつ `error_rate = 0` かつ `retry_rate >= 0.15` で `warn`
- 推奨アクション: ログ欠損・集計漏れを監査

## R9. Throughput Collapse
- 前提: 前日値がある
- 条件: `requests` が前日比 -40% 以下で `warn`
- 条件: `requests` が前日比 -60% 以下で `critical`

## R10. Notes Alert Keyword
- 条件: `notes` に `incident|outage|timeout|rollback` を含む場合 `warn`
- 推奨アクション: 手動インシデントレビューを優先

---

## Output Format (固定)
1. Summary（1-2行）
2. Risks（critical/warnの箇条書き）
3. Actions（優先順3件）
4. Next Check（翌日の確認ポイント1-2件）
