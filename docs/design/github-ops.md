# 営業向けAI研修プログラム GitHub運用設計

> プログラム一式（設計書・講師台本・配布教材・テンプレ・KPIダッシュボード）を **GitHub で一元管理し、MkDocs Material で HTML サイトとして社内公開** するための設計。
> 関連：[カリキュラム設計書](curriculum.md) ／ [講師台本（L1/L2/L3）](../scripts/index.md)

## 確定した方針
- **サイト構築**：MkDocs Material（Markdownを書く → GitHub Actions が自動でHTMLビルド → GitHub Pages 公開）
- **公開範囲**：社内限定（運営・講師・**受講者**が閲覧）
- **編集体験**：日々の更新は **Markdownを書くだけ**。HTMLは触らない。
- **単一の正**：教材・運営情報・データすべてを1リポジトリに集約し、Gitで履歴管理する。

---

## 1. 全体アーキテクチャ

```
┌─────────────────────── GitHub リポジトリ（Private/Internal）───────────────────────┐
│                                                                                    │
│  docs/*.md（教材・台本・設計）   ──┐                                                │
│  docs/dashboard/data/*.csv（KPI）  │   git push（main）                            │
│  mkdocs.yml / workflow             ▼                                                │
│                          ┌──────────────────────┐                                  │
│                          │ GitHub Actions       │  mkdocs build                    │
│                          │ （自動ビルド）        │ ───────────────►  site/（HTML）   │
│                          └──────────────────────┘                                  │
│                                     │ deploy-pages                                  │
│                                     ▼                                               │
│                       ┌──────────────────────────────┐                             │
│                       │ GitHub Pages（アクセス制御付き）│ ◄── 社内メンバーのみ閲覧   │
│                       └──────────────────────────────┘                             │
│                                                                                    │
│  Issues / Projects … セッション運営・宿題・改善要望をタスク管理                       │
└────────────────────────────────────────────────────────────────────────────────────┘
        ▲
        │ 週次の運営入力（レベル診断結果）
  Microsoft Forms ──エクスポート(CSV)──► リポジトリにコミット ──► ダッシュボードに反映
```

**役割分担の考え方**
- **コンテンツの正本・履歴・公開**＝GitHub（このリポジトリ）
- **データ収集（レベル診断）**＝Microsoft Forms のまま（受講者に優しく、既存運用を壊さない）
- **データの可視化**＝Forms の結果をCSVでリポジトリに取り込み、サイト内ダッシュボードで表示
  → 「閲覧・管理はGitHub上のHTMLで完結」しつつ、収集の手間は増やさない折衷。

---

## 2. リポジトリ構成（ディレクトリ設計）

```
ai-sales-training/                    ← リポジトリ root
├─ mkdocs.yml                         サイト設定（ナビ・テーマ）
├─ requirements.txt                   MkDocs依存（mkdocs-material）
├─ README.md                          運用者向け：編集・公開の手順
├─ .gitignore
├─ CODEOWNERS                         レビュー必須者の指定
├─ .github/
│  ├─ workflows/deploy.yml            push時に自動ビルド＆公開
│  └─ ISSUE_TEMPLATE/
│     ├─ session.md                   セッション準備・実施テンプレ
│     └─ improvement.md               教材・運用の改善要望テンプレ
└─ docs/                              ← サイトの中身（ここだけ触れば良い）
   ├─ index.md                        トップ：プログラム概要・サイトの歩き方
   ├─ design/
   │  ├─ curriculum.md                カリキュラム設計書（既存）
   │  └─ github-ops.md                本設計書（既存）
   ├─ scripts/                        講師台本
   │  ├─ l1.md
   │  ├─ l2.md
   │  └─ l3.md
   ├─ materials/                      配布教材（架空サンプル）
   │  ├─ l1-transcript.md            L1：会議トランスクリプトサンプル
   │  ├─ l2-meeting-transcript.md     L2：会議文字起こし
   │  ├─ l2-deal-list.md              L2：案件リスト
   │  └─ l3-brief.md                  L3：案件ブリーフ
   ├─ templates/
   │  └─ index.md                     プロンプトテンプレ・チェックリスト集
   ├─ dashboard/
   │  ├─ index.md                     KPIダッシュボード（グラフ表示ページ）
   │  └─ data/levels.csv              週次レベル分布データ（運営が更新）
   └─ assets/                         画像・追加CSS
```

**設計意図**
- 既存3ファイルは `docs/design/` と `docs/scripts/` にそのまま配置（パスを少し直すだけ）。
- 教材・テンプレ・ダッシュボードを **章立て**にして、サイト左ナビでレベル別に辿れるようにする。
- 「編集者は `docs/` 配下のMarkdownだけ触る」が鉄則。設定ファイルは初回構築後ほぼ不変。

---

## 3. セットアップ（コピペで使える設定一式）

### 3-1. `requirements.txt`
```
mkdocs-material
```

### 3-2. `mkdocs.yml`
```yaml
site_name: 営業向けAI研修プログラム
site_description: 営業職向けAI教育（IBM Consulting Advantage + Copilot）
docs_dir: docs
theme:
  name: material
  language: ja
  features:
    - navigation.sections      # レベル別にセクション表示
    - navigation.top
    - navigation.footer
    - search.suggest
    - content.code.copy        # コードブロックにコピーボタン（プロンプト配布に便利）
    - toc.integrate
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
plugins:
  - search:
      lang: ja
markdown_extensions:
  - admonition                 # 「!!! note」で注意書きボックス
  - attr_list
  - md_in_html                 # ダッシュボードのHTML/JS埋め込み用
  - tables
  - toc:
      permalink: true
  - pymdownx.superfences
  - pymdownx.highlight
nav:
  - ホーム: index.md
  - 設計:
      - カリキュラム設計書: design/curriculum.md
      - GitHub運用設計: design/github-ops.md
  - 講師台本:
      - L1 初心者: scripts/l1.md
      - L2 初級〜中級: scripts/l2.md
      - L3 上級: scripts/l3.md
  - 配布教材:
      - L1 会議トランスクリプト: materials/l1-transcript.md
      - L2 会議文字起こし: materials/l2-meeting-transcript.md
      - L2 案件リスト: materials/l2-deal-list.md
      - L3 案件ブリーフ: materials/l3-brief.md
  - テンプレート集: templates/index.md
  - KPIダッシュボード: dashboard/index.md
```

### 3-3. `.github/workflows/deploy.yml`（push時に自動ビルド＆公開）
```yaml
name: Deploy docs
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt
      - run: mkdocs build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

### 3-4. `.gitignore`
```
site/
.cache/
__pycache__/
*.pyc
.DS_Store
```

> これだけで「Markdownをpush → 数分後にHTMLサイトが更新」が回ります。ローカル確認は `pip install -r requirements.txt && mkdocs serve` で `http://localhost:8000`。

---

## 4. 公開範囲とアクセス制御（社内限定の実現方法）

「社内の人だけがHTMLを見られる」をどう実現するかは **GitHubプランで変わります**。ここは事前確認が必須です。

| プラン | 実現方法 | 受講者の閲覧 |
|---|---|---|
| **GitHub Enterprise Cloud** | リポジトリを **Internal**（Org/Enterprise全員が閲覧可）にし、Pages の **アクセス制御**を有効化。SAML SSO ログイン者のみ閲覧。 | ◎ 推奨構成。組織メンバーがSSOで閲覧 |
| **GitHub Team** | Private リポジトリは可。ただし **Private Pages のアクセス制御は Enterprise Cloud 限定**のため、Pagesを使うとサイトが公開になる点に注意。→ フォールバック採用 | △ フォールバックで対応 |
| **Free / Pro** | 同上。Pagesは公開前提。 | △ フォールバックで対応 |

### Enterprise Cloud でない場合のフォールバック（社内限定を保つ）
公開Pagesにしたくない場合は、**HTMLを社内インフラに配信**します（教材の正本はGitHubのまま）。
- **案A（推奨フォールバック）**：GitHub Actions でビルドした `site/`（HTML一式）を **SharePoint / 社内Webサーバ / Azure Static Web Apps（認証付き）** に配信。閲覧は社内認証でガード。
- **案B**：受講者にはサイトを **PDF/静的HTMLでエクスポート**して Teams で配布。編集・履歴管理はGitHubで継続。
- **案C**：受講者は GitHub上で **レンダリングされたMarkdown**を直接閲覧（HTMLサイトは運営・講師のみ）。

### 受講者アクセスの前提（要確認・コスト観点）
- Enterprise Cloud 構成では、**受講者全員に GitHub アカウント（Org/Enterpriseメンバー）と席（シート）** が必要。10〜20名×繰り返し参加ぶんの席数・管理コストを情シスと確認。
- 受講者にアカウント付与が重い場合は、上記フォールバック案B/Cが現実的。

> **まず情シス/GitHub管理者に「現在のプラン」と「Private Pagesのアクセス制御が使えるか」を確認**してから、本番構成（Pages公開 or フォールバック）を確定する。設計はどちらでも `docs/` 配下は共通なので、後から切替可能。

---

## 5. 週次の運用フロー（誰が・どう更新するか）

### ブランチ戦略（軽量・少人数向け）
- `main` = 公開中の本番。**直接pushしない**。
- 更新は作業ブランチ（例 `update/l2-template`）→ **Pull Request** → レビュー → マージで自動公開。
- `main` に **ブランチ保護**（PRレビュー必須・1名承認）を設定し、品質と事故防止を担保。

### 標準サイクル（カリキュラムの週次運用に同期）
| タイミング | 作業 | 場所 |
|---|---|---|
| 月 | レベル診断Forms配布／前回宿題リマインド | Forms・Teams |
| 火〜水 | 当週セッションの準備（台本確認・配布教材更新があればPR） | GitHub PR |
| 木/金 | 本番セッション実施 | Teams |
| 翌日 | 診断結果CSVを `dashboard/data/levels.csv` に追記コミット／気づきを台本に反映（PR）／良かった資産を `templates/` に昇格 | GitHub PR |

### 編集の実務（非エンジニアでも回せる）
- 小さな修正は **GitHub Web UI で直接編集**（ファイルを開いて鉛筆アイコン → 変更 → PR作成）。ローカル環境構築は不要。
- 体裁プレビューは PR の **Actionsビルド成功**で確認、またはローカル `mkdocs serve`。

---

## 6. 研修「運営」そのものをGitHubで管理する

教材だけでなく、**運営タスク**もGitHubに寄せると一元化できます。

### Issues（セッション単位の管理）
- **1セッション＝1 Issue**。`ISSUE_TEMPLATE/session.md` に準備チェックリストを定義：
  ```
  ## セッション
  - レベル: L1 / L2 / L3
  - 開催日:
  - サイクル: 第○サイクル
  ## 事前準備
  - [ ] 配布教材リンク確認
  - [ ] 参加者ログイン・権限確認（TAフォロー）
  - [ ] レベル診断Forms配布
  ## 実施後ふりかえり
  - 出席/レベル分布:
  - うまくいった点 / 詰まった点:
  - 次回への改善（→該当台本にPR）:
  ```
- **ラベル**：`level:L1` `level:L2` `level:L3`、`cycle:1〜4`、`status:準備中/完了`。

### Projects（12週スケジュールの可視化）
- カンバン or タイムラインで **12週グリッド**（設計書§2）を管理。Milestone＝各サイクル/月。
- 「初心者ゼロ・半数上級」の進捗を Issue/Project 上でも追える。

### 改善要望
- 教材・運用の改善は `improvement.md` テンプレでIssue化 → PRで反映 → 履歴が残る（誰がいつ何を改善したか）。

---

## 7. KPIダッシュボードのGitHub完結

設計書§6の「レベル分布の推移グラフ」を、サイト内ページとして表示します。

### データの流れ
1. レベル診断（**Microsoft Forms**）の回答を **CSVエクスポート**。
2. 週次集計を `docs/dashboard/data/levels.csv` に追記して **コミット**。
   ```csv
   week,L1,L2,L3
   1,12,4,1
   2,9,6,2
   3,6,8,3
   ```
3. ダッシュボードページがCSVを読み、**折れ線グラフ**で「初心者が減り上級が増える」推移を表示。

### `docs/dashboard/index.md`（Chart.js を埋め込む例）
````markdown
# KPIダッシュボード

各回のレベル診断（Microsoft Forms）結果をもとに、レベル分布の推移を表示します。

<canvas id="levelChart" height="120"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
fetch('data/levels.csv')
  .then(r => r.text())
  .then(csv => {
    const rows = csv.trim().split('\n').slice(1).map(l => l.split(','));
    const labels = rows.map(r => 'W' + r[0]);
    const mk = (i, label, color) => ({
      label, data: rows.map(r => Number(r[i])), borderColor: color, tension: .3
    });
    new Chart(document.getElementById('levelChart'), {
      type: 'line',
      data: { labels, datasets: [
        mk(1, 'L1 初心者', '#e53935'),
        mk(2, 'L2 初級〜中級', '#fb8c00'),
        mk(3, 'L3 上級', '#43a047'),
      ]},
      options: { plugins: { title: { display: true, text: 'レベル分布の推移' } } }
    });
  });
</script>
````
> `mkdocs.yml` で `md_in_html` を有効化しているので、MarkdownページにそのままHTML/JSを埋め込めます。外部CDN（jsdelivr）が社内ネットワークで許可されているか確認；不可ならChart.jsを `docs/assets/` に同梱。

### 代替案（外部JS禁止の環境）
GitHub Actions で CSV から **グラフ画像（PNG/SVG）を自動生成**（matplotlib等）して `assets/` にコミット → ページに画像として埋め込む。閲覧側はJS不要。

---

## 8. バージョン管理・スナップショット

- **タグ／リリース**：各サイクル終了時に `v1-cycle1` のようにタグを切り、その時点の教材一式をスナップショット化。「どのサイクルでどの版を使ったか」を再現可能に。
- **CHANGELOG**：主要な教材改訂を `docs/index.md` 末尾か `CHANGELOG.md` に記録（PRと紐付く）。
- Git履歴そのものが監査ログになるため、「いつ・誰が・なぜ」変えたかが常に追える。

---

## 9. セキュリティ・運用ルール（重要）

研修教材の性質上、**実顧客情報を絶対にコミットしない**ことが最優先です。

- 配布教材・サンプルは **すべて架空データ**（設計原則と一致）。実名・実案件・金額は置かない。
- `CODEOWNERS` ＋ ブランチ保護で **PRレビュー必須**。第三者の目で混入を防ぐ。
- レビュー観点に「個人情報・社外秘・実顧客名の混入なし」を明文化（`improvement.md`／PRテンプレに項目化）。
- リポジトリは **Private/Internal** 固定。Public化は禁止（誤操作防止のため設定で制御）。
- 受講者がアップする成果物に実データを含めない運用ルールを、各台本冒頭の「安全ルール」と一致させる。

---

## 10. 導入ステップ（移行手順）

1. **プラン確認**：情シス/GitHub管理者に「Enterprise Cloud か」「Private Pagesのアクセス制御可否」を確認 → §4で本番構成を確定。
2. **リポジトリ作成**：Org内に Private/Internal で `ai-sales-training` を作成。
3. **既存資産を配置**：`営業向けAI教育カリキュラム設計書.md` → `docs/design/curriculum.md`、`講師台本_全3レベル.md` → 台本3ファイルに分割し `docs/scripts/` へ。相互リンクのパスを調整。
4. **設定ファイル追加**：§3の `mkdocs.yml` / `requirements.txt` / `deploy.yml` / `.gitignore` をコミット。
5. **Pages有効化**：Settings → Pages → Source = GitHub Actions。アクセス制御を社内限定に設定（or フォールバック構成）。
6. **初回ビルド確認**：mainにpush → Actions成功 → サイト表示を確認。
7. **アクセス付与**：運営・講師・（必要なら）受講者を Team に追加。
8. **運用整備**：ブランチ保護、Issue/PRテンプレ、Projectボード（12週）を作成。
9. **ダッシュボード開始**：`dashboard/data/levels.csv` と表示ページを用意し、初回診断から運用開始。

---

## 付録：このGitHub運用が効く理由
- **単一の正本**：教材・運営・データが1か所に集約され、「最新どれ？」問題が消える。
- **履歴と再現性**：毎サイクルの改訂が追え、過去版を即復元できる（研修は回すほど教材が育つ前提と相性が良い）。
- **編集の民主化**：Markdownだけ書けば公開される。非エンジニアの講師もWeb UIで貢献できる。
- **運営の可視化**：Issue/Projectで「初心者ゼロ・半数上級」への進捗がチームに見える。
- **配布が一瞬**：プロンプトはコピーボタン付きHTMLで配れ、台本・教材・KPIが同じ場所に揃う。
