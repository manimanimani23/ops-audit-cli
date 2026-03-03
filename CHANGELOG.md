# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-03

### Added
- 初期リリース
- 10の監査ルールを実装（R1-R10）
- Python標準ライブラリのみで動作（依存ゼロ）
- CI/CD統合用終了コード制御
- 3モード監査（ok/warn/critical）
- 翌日アクション自動生成

### Rules Implemented
- R1: Error Rate Spike
- R2: Retry Loop Risk
- R3: Latency Degradation
- R4: Cost Overrun (Absolute)
- R5: Cost Efficiency Drop
- R6: Combined Failure Risk
- R7: Latency-Cost Coupled Risk
- R8: Silent Failure Suspicion
- R9: Throughput Collapse
- R10: Notes Alert Keyword

## [Unreleased]

### Planned
- HTMLレポート出力
- PDFレポート出力
- カスタムルール設定ファイル対応
- Slack/Discord Webhook連携
