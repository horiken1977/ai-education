# 営業向けAI研修プログラム（リポジトリ）

営業職向けAI教育プログラム（IBM Consulting Advantage + Copilot）の **設計書・講師台本・配布教材・テンプレート・KPIダッシュボード** を一元管理するリポジトリです。
中身は [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) で HTML サイトとしてビルドされ、GitHub Pages（社内限定）で公開されます。

## このリポジトリの歩き方
- 教材・台本など**サイトの中身はすべて `docs/` 配下の Markdown**です。日々の更新は `docs/` だけ触ります。
- サイトの構成（ナビ）は [`mkdocs.yml`](mkdocs.yml) で管理します。
- `main` ブランチに変更がマージされると、GitHub Actions が自動でビルドして公開します。

## ディレクトリ構成
```
docs/
├─ index.md                トップ（プログラム概要・使い方）
├─ design/                 設計書（カリキュラム / GitHub運用）
├─ scripts/                講師台本（共通ガイド + L1/L2/L3）
├─ materials/              配布教材（架空サンプル）
├─ templates/              プロンプトテンプレ・チェックリスト集
├─ dashboard/              KPIダッシュボード（CSV + 表示ページ）
└─ assets/                 画像・追加CSS
```

## 編集のしかた
### A. ブラウザだけで（非エンジニア向け）
1. 該当の `.md` ファイルを開き、右上の鉛筆アイコンで編集。
2. 「Propose changes」→ Pull Request を作成。
3. レビュー承認後にマージ → 自動で公開。

### B. ローカルでプレビューしたいとき
```bash
pip install -r requirements.txt
mkdocs serve      # http://localhost:8000 で確認
```

## 運用ルール（重要）
- **実顧客情報・個人情報・社外秘は絶対にコミットしない**。配布教材・サンプルはすべて架空データ。
- `main` への直接 push は禁止。変更は必ず Pull Request 経由（レビュー必須）。
- セッションの準備・ふりかえりは Issue（`.github/ISSUE_TEMPLATE/`）で管理。

詳細は [docs/design/github-ops.md](docs/design/github-ops.md) を参照。
