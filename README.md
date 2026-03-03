# Ops Audit CLI

AI運用ログを日次で監査し、異常検知と翌日アクションを返すCLIツール。

## 特徴

- **依存ゼロ**: Python標準ライブラリのみで動作
- **10の監査ルール**: エラー率、再試行率、レイテンシ、コストなどを自動検知
- **CI/CD統合**: 終了コードでパイプライン制御可能
- **即座に使える**: pip install一発、設定不要

## クイックスタート

```bash
pip install ops-audit-cli
ops-audit input.json output.json
```

## ドキュメント

- [クイックスタートガイド](QUICKSTART.md) - 5分で始める
- [監査ルール詳細](ops-audit-rules-v1.md) - 10のルールの仕様
- [スキーマ定義](ops-audit-schema-v1.json) - 入出力JSONスキーマ
- [変更履歴](CHANGELOG.md)

## ライセンス

MIT License - 詳細は[LICENSE](LICENSE)を参照

## 作者

AIマニ (@manimanimani23)
- X: https://x.com/kxO1oiVxt536918
- GitHub: https://github.com/manimanimani23
