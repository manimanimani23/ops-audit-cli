# Publication Kit v1 (Agent Economy MVP)

目的: `projects/agent-economy` を「公開可能な最小単位」に整え、公開時の手戻りをゼロにする。

## 1) 公開前チェック（15分）
- [ ] 入力データに個人情報が含まれていない（sample/case/out すべて確認）
- [ ] 依存は Python 標準ライブラリのみ（`ops_audit_cli.py`）
- [ ] README の Quick Start が現状ファイル名と一致
- [ ] テスト結果3ケース（stable/warn/mixed）が再現可能

### 再現コマンド
```powershell
cd F:\AI\MANI\projects\agent-economy
py -3 ops_audit_cli.py case_stable.json out_stable.json
py -3 ops_audit_cli.py case_warn.json out_warn.json
py -3 ops_audit_cli.py case_mixed.json out_mixed.json
```

## 2) GitHub公開テンプレ（30分）

### リポジトリ説明（短文）
Daily Ops Audit MVP: a lightweight rule-based CLI that audits AI operation logs and returns risk/action recommendations.

### トピック案
`aiops`, `agent-economy`, `observability`, `python-cli`, `rule-engine`, `cost-monitoring`

### 初回リリースノート（v0.1.0）
- Added: JSON input schema (`ops-audit-schema-v1.json`)
- Added: 10 audit rules (`ops-audit-rules-v1.md`)
- Added: CLI auditor (`ops_audit_cli.py`)
- Added: 3-case beta test outputs (`out_stable/out_warn/out_mixed`)
- Added: beta checklist/report for threshold tuning

## 3) 公開本文テンプレ

### GitHub README追記用（冒頭に追加）
```markdown
## What this solves
This MVP helps operators quickly detect cost/latency/retry anomalies from daily logs and convert them into concrete next-day actions.
```

### X投稿テンプレ（個人情報ゼロ）
```text
Shipped v0.1 of a tiny "Daily Ops Audit" agent MVP.
- Input: daily AI ops metrics (cost/retry/latency/error)
- Output: risk labels + next actions
- Stack: Python stdlib only

Now tuning thresholds with beta cases (stable/warn/mixed).
```

### note投稿テンプレ（日本語）
```text
AI運用の「日次監査」を最小構成で回せるMVPを公開準備しました。
入力はコスト・再試行率・遅延などの基本メトリクス、出力はリスク判定と翌日アクションです。
次の1週間で閾値調整（stable/warn/mixed）を行い、誤検知率を下げます。
```

## 4) 公開判定ゲート（Go/No-Go）
- Go条件:
  - sample/case/out に個人情報なし
  - READMEだけで実行再現できる
  - 3ケースの出力が期待方向に一致
- No-Go条件:
  - 公開先ポリシー未承認
  - 投稿導線で CAPTCHA/2FA が必要

## 5) 次アクション（公開承認後すぐ実行）
1. GitHubで `v0.1.0` タグ作成
2. X/noteに同日告知（本文テンプレ使用）
3. 24hで反応指標を記録（クリック/保存/問い合わせ数）
