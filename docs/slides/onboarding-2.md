---
marp: true
theme: ibm
paginate: true
header: 'AIレベルアップセッション — オンボーディング（第2回・図解版）'
---

<!--
編集メモ（スライドには映りません）
── このファイルは「第2回オンボーディング」＝前回(onboarding.md)の講義パートを図解でスリム化した版。
   前回のスライド(onboarding.md)は実施記録としてそのまま残す（これは別ファイル）。
── 図解は ibm.css の部品クラスで書く（円・四角・矢印）。書き方の早見表＝ slides/flow-parts.md（Marpで開くと見本＋コピペ用コード）。
   最小例： <div class="flow"><span class="node">素材</span><span class="node accent">AIに作らせる</span><span class="node">人が確認</span></div>
   → flow の中に node を並べるだけで矢印(→)が自動で入る。縦は flow col、円は node circle、強調は node accent、従来グレーは node plain。
── 番人 check_slide_sync.py は LEVELS 登録レベル(onboarding/l1…)だけを見る＝この onboarding-2 は監視対象外。ただし前回同様、核心語（一気通貫/RFP/手を動か/成果物/卒業条件/LV3/失敗/修正/混在型/7割）は意味として残してある。
── 旧表記（旧研修名や旧レベル呼称の類）は使わない。docs全体grepの番人が検出するため、禁止語そのものはここに書かない（curriculum.md が正）。
── 編集後は必ず: bash tools/check_slides.sh（赤が無ければ push＝自動デプロイ）
-->

<!-- _class: lead -->
# オンボーディング（第2回）

**前回のおさらいを“図解で速く” → すぐ手を動かす**

---
<!-- _class: lead -->
## 今日の地図：全体の流れ

<div class="flow">
  <span class="node accent">オンボ</span>
  <span class="node">LV1</span>
  <span class="node">LV2</span>
  <span class="node">LV3</span>
  <span class="node">エクストラ</span>
</div>

> いまここ＝**オンボ**。今日は「渡し方の型」を体で覚えます。

---

## ① 営業プロセスが変わる

<style scoped>
.flow-set .node { font-size: 0.78em; padding: 0.4em 0.6em; }
</style>

<div class="flow-set">
  <div class="flow-label now">従来</div>
  <div class="flow">
    <span class="node plain">依頼ベース</span>
    <span class="node plain">狭い仮説</span>
    <span class="node plain">提案の往復</span>
    <span class="node plain">RFPで競争</span>
  </div>
  <div class="flow-label next">AI＋</div>
  <div class="flow">
    <span class="node accent">AIで調査</span>
    <span class="node accent">仮説で先回り</span>
    <span class="node">1〜2回で合意</span>
    <span class="node">一気通貫で受注</span>
  </div>
</div>

> 後手の**RFP**競争から、**仮説起点で先回り**する営業へ。

---
<!-- _class: lead -->

## ② 本取り組みの進め方

<div class="flow">
  <span class="node">手を動かす</span>
  <span class="node accent">毎回“成果物”を持ち帰る</span>
  <span class="node">毎週の実務で反復</span>
</div>

- 教わる場ではありません。上達エンジンは講義だけでなく **実務利用（反復）＋学び合い**

> だから説明は最小限。今日もすぐ触ります。

---
<!-- _class: lead -->

## ③ レベルと卒業条件

| レベル | 一言ゴール | 卒業条件（できること） |
|---|---|---|
| オンボ | 素材を渡す型＋地図 | 録画→議事録を自力で作れる |
| LV1 | チャットAI使い倒し | リサーチ/メール/壁打ちを週次常用 |
| LV2 | Bobでデモ | 紙芝居デモを1本作れる |
| LV3 | 使い分け | 案件まるごとを1周回せる |
| エクストラ | 作る側へ | ミニアプリを作り公開できる |

---
<!-- _class: lead -->

## ④ 学びの変化

積極的に **失敗しよう**。**うまくいくまで修正すればいい**だけ。

<div class="flow-set">
  <div class="flow-label now">従来</div>
  <div class="flow">
    <span class="node plain">わかる</span>
    <span class="node plain">やってみる</span>
    <span class="node plain">できる</span>
    <span class="node plain">習慣化</span>
  </div>
  <div class="flow-label next">AI＋</div>
  <div class="flow">
    <span class="node accent">やってみる</span>
    <span class="node accent">まちがう</span>
    <span class="node accent">修正する</span>
    <span class="node">できる</span>
    <span class="node">習慣化</span>
  </div>
</div>

> **わからなくてもいい** — まず問いを投げてみよう

---
<!-- _class: lead -->

## ⑤ 3ヶ月の流れ（途中で変わる可能性あり）

<div class="flow">
  <span class="node">前半：LV1中心</span>
  <span class="node">中盤：LV2</span>
  <span class="node accent">後半：LV3</span>
</div>

- **混在型**：毎回どのレベルに出るかを**自分で選ぶ**（行き来OK）
- 3ヶ月後のゴール分布（想定）：**LV2 1割 ／ LV3 7割 ／ エクストラ 2割**

---
<!-- _class: lead -->

## 背骨：AIへの渡し方の型

<div class="flow">
  <span class="node">素材</span>
  <span class="node">指示</span>
  <span class="node accent">AIに<br>作らせる</span>
  <span class="node">人が確認</span>
</div>

> 毎回この4ステップ。**青（AIの担当）以外は人がやる**。ここを体で覚えるのが今日のゴール。

---
<!-- _class: lead -->

## はじめのお約束

<div class="flow">
  <span class="node circle">録画</span>
  <span class="node circle accent">文字<br>起こし</span>
  <span class="node circle">議事録</span>
</div>

- マインドセットは **「自分の仕事をなくす」**
- お客様名・個人情報・社外秘は **そのまま入力しない**（伏字か配布データ）
- 会議は **Teamsで録画 → Copilotで文字起こし**（メモは不要）
- **お客様との打ち合わせは、録画の前に必ず同意を得る**

> 「記録のために録画させてください。私たちの記録のためだけに使います。」

---
<!-- _class: lead -->

# とにかくやってみよう！

- 会議の「録画」を議事録に
- ゴール：**Teams会議の録画トランスクリプトを、議事録・報告・次アクションに“自力で”整える**

---
<!-- _class: lead -->

## まずはこちら（5分）

以下手順を画面を真似しながらやってみてください 👇

```text
① Teamsの管理画面を開く
② 左ペイン「チャット」から録画された会議を選択する（WeeklyMTGでもSIRでもOKです）
③ 録画データをスクロールで探し、「要約の表示」をクリックする
④ 新しく開いたウィンドウで「Copilot」をクリックする
⑤ チャットボットに会議の要約を指示する（指示文は自分で考えてみてください）
```

> どんな要約が出てきたかを以下のご自身の名前のBoxNoteに記録してください
> https://ibm.box.com/s/ksh1r5s67i2w5j0o6cvtn9z41li24vei

---
<!-- _class: lead -->

## 次にこちら（5分）

今度は、以下を Copilot に貼って実行してください 👇

```text
この会議の transcript を根拠に、
①会議日付・時間
②出席者
③利用された資料
④議論の論点・議論内容
⑤決定事項
⑥未決事項
⑦次アクション・担当者候補 ・期限（テーブル形式）
⑧内確認・根回し事項
を整理してください。
不明な項目は「要確認」。事実を勝手に作らないこと。
```

> どんな要約が出てきたかを以下のご自身の名前のBoxNoteに記録してください
> https://ibm.box.com/s/ksh1r5s67i2w5j0o6cvtn9z41li24vei

---
<!-- _class: lead -->

## ブレイクアウト① 数人で議論（10分議論・5分共有）

1. どういう指示をしたらどんなアウトプットが出たか
2. どういう指示をすると良さそうか

---
<!-- _class: lead -->
## まとめ

<div class="flow">
  <span class="node plain">わかる</span>
  <span class="node accent">できる</span>
  <span class="node">身につく</span>
</div>

今日は **“できる”の入口**

🎯 学びの共有（5分）
🎯 ご自身の学びの記録（プロンプトのコピペや気付きなどをBoxNotesに）（5分）
> https://ibm.box.com/s/ksh1r5s67i2w5j0o6cvtn9z41li24vei

---
<!-- _class: lead -->
## QAタイム

質問なんでもどうぞ

---
<!-- _class: lead -->

## 情報共有の方法

1. 質問や対話はSlackに集約（パンクするからメールは禁止）
2. 読んだらスタンプおねがいします
3. 録画や学習記録はBox
https://ibm.box.com/s/2x7uknewe9rne3ltgd6vva1680tphz31

---
<!-- _class: lead -->
## アンケートのお願い

以下のアンケートにお応えください（1分で終わります）

> https://forms.cloud.microsoft/r/vfxwGZs57r
