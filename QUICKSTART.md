# Ops Audit CLI - Quick Start Guide

## 5分で始める

### 1. インストール
```bash
pip install ops-audit-cli
```

### 2. 入力ファイルを作成
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

### 3. 監査実行
```bash
ops-audit input.json output.json
```

### 4. 結果確認
```bash
cat output.json | jq '.summary, .status, .actions'
```

## CI/CD連携

```yaml
# .github/workflows/audit.yml
- name: Run Ops Audit
  run: |
    ops-audit daily-log.json - --fail-on warn | jq '.risks'
```

## 終了コード

| コード | 意味 |
|--------|------|
| 0 | 正常（status: ok） |
| 1 | 入力エラー |
| 2 | 監査失敗（--fail-onで指定したレベル以上） |

## 入力項目一覧

| 項目 | 型 | 必須 | 説明 |
|------|-----|------|------|
| project_id | string | ○ | プロジェクト識別子 |
| date | string | ○ | YYYY-MM-DD形式 |
| inference_cost_usd | number | ○ | 推論コスト（USD） |
| retry_rate | number | ○ | 再試行率（0-1） |
| p95_latency_ms | number | ○ | P95レイテンシ（ms） |
| error_rate | number | ○ | エラー率（0-1） |
| requests | number | - | リクエスト数 |
| notes | string | - | 備考・インシデント記録 |

## 監査ルール一覧

| ルール | 条件 | アクション |
|--------|------|------------|
| R1 Error Rate Spike | error_rate >= 5% | 失敗タイプを分析 |
| R2 Retry Loop Risk | retry_rate >= 25% | バックオフ設定を見直す |
| R3 Latency Degradation | P95 >= 5000ms | タイムアウト設定を点検 |
| R4 Cost Overrun | cost >= $50 | 高コスト経路を特定 |
| R5 Cost Efficiency | cost/req >= $0.03 | キャッシュ適用を検討 |
| R6 Combined Failure | retry + error 高値 | 原因を分離して切り分け |
| R7 Latency-Cost Coupled | レイテンシ+コスト両方悪化 | 緊急対応 |
| R8 Silent Failure | retryありでerror=0 | ログ欠損を監査 |
| R9 Throughput Collapse | 前日比-40%以上 | トラフィック異常確認 |
| R10 Notes Alert | notesに警報キーワード | 手動レビュー優先 |

## サンプル出力

```json
{
  "project_id": "my-project",
  "date": "2026-03-03",
  "summary": "緊急リスク1件、警告リスク2件を検出。対応を検討してください。",
  "status": "critical",
  "risks": [
    "critical: Error Rate Spike (>= 5%)",
    "warn: Retry Rate Elevated (>= 12%)",
    "warn: Notes Alert Keyword: timeout"
  ],
  "actions": [
    "失敗タイプ上位3件を抽出し、当日変更との差分確認",
    "再試行回数上限とバックオフ戦略を見直す",
    "手動インシデントレビューを優先"
  ],
  "next_check": {
    "error_rate": "<= 0.01",
    "retry_rate": "<= 0.10"
  }
}
```

## トラブルシューティング

### "File not found" エラー
入力ファイルのパスを確認してください。相対パス・絶対パス両方対応しています。

### "Invalid JSON" エラー
JSONの構文を確認してください。カンマの付け忘れや引用符の不一致が多いです。

### 終了コード2が返る
--fail-onオプションで指定したレベル以上のリスクが検出された場合、終了コード2を返します。これはCI/CDでの失敗判定に利用できます。

## ライセンス

MIT License - 商用利用・改変・再配布可能
