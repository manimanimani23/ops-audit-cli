# First Public Release Bundle (2026-02-27)

目的: `ROADMAP.md` フェーズ2「収益化プロトタイプの公開とテスト」を、承認後すぐ実行できる“公開即時パッケージ”にする。

## 1. GitHub公開（承認後に実行）

### 1-1. 最小公開スコープ
- `projects/agent-economy/ops-audit-schema-v1.json`
- `projects/agent-economy/ops-audit-rules-v1.md`
- `projects/agent-economy/README.md`
- `projects/agent-economy/ops_audit_cli.py`
- `projects/agent-economy/testdata/*.json`
- `projects/agent-economy/out_*.json`

### 1-2. 公開前チェック（Go/No-Go）
- [ ] 個人情報・識別子がファイルに含まれていない
- [ ] `python ops_audit_cli.py --input testdata/stable.json --output out_stable.json` が成功
- [ ] `python ops_audit_cli.py --input testdata/warn.json --output out_warn.json` が成功
- [ ] `python ops_audit_cli.py --input testdata/mixed.json --output out_mixed.json` が成功
- [ ] Known Limits（CAPTCHA/2FAは自動化対象外）をREADMEに明記

### 1-3. リリースノート本文（コピペ用）
```
Initial public beta for Daily Ops Audit Endpoint.

Added
- JSON schema for audit input
- 10 explicit audit rules
- CLI analyzer and 3 test scenarios (stable / warn / mixed)

Validated
- Expected behavior matched on all 3 scenarios

Known limits
- Human verification steps (CAPTCHA/2FA) are intentionally out of automation scope
```

## 2. X投稿文（告知用・短文）

### Post 1（公開告知）
AI運用監査の最小実装を公開準備しました。  
入力スキーマ固定 + 監査ルール明文化 + 3ケース検証（stable/warn/mixed）まで完了。  
次は公開後の実運用データで、失敗率と人手介入率を下げにいきます。

### Post 2（価値訴求）
AI運用の改善は「モデルを替える」前に、監査を固定する方が速いです。  
失敗率 / 人手介入率 / 単位成果コストの3点を毎日見るだけで、赤字化リスクがかなり下がります。

## 3. note記事の導入文（下書き投入用）

タイトル案:  
**AI運用を黒字化する最小構成：監査ループを先に作る**

導入文:  
多機能なエージェントを作るほど、運用は不安定になりがちです。  
そこで先に固定すべきなのは機能数ではなく、監査の型です。  
本稿では、入力スキーマ・監査ルール・Go/No-Go判定の3点だけで、
「再現できる改善ループ」を作る方法を実例ベースで整理します。

## 4. 30分実行ランブック（承認後）
1. GitHubへ最小公開スコープを反映
2. リリースノートを作成
3. X Post 1を投稿
4. noteへ導入文を投入して下書き保存
5. 反応確認後、4〜6時間以内にX Post 2を投稿

## 5. 完了条件
- GitHub: 公開または公開直前のPR状態
- X: 告知1本以上
- note: 下書き1本保存

## 6. blocker
- 公開実行には「公開先ポリシーの最終承認」が必要（必要な人手: 最終承認1回）。
