---
marp: true
theme: ibm
paginate: true
header: '図解パーツ早見表（講師用・コピペ集）'
---

<!--
これは受講者向けスライドではなく、講師が図解を作るときの「コピペ集」です。
Marpで開くと「見本」と「そのコピペ用コード」が並びます（slides-indexには載せていません）。
部品の実体は docs/slides/ibm.css の末尾「図解ユーティリティ」。
基本ルール：<div class="flow"> の中に <span class="node"> を並べるだけ。矢印(→/↓)は自動。
-->

<!-- _class: lead -->
# 図解パーツ早見表

**`flow` の中に `node` を並べるだけ。矢印は自動で入ります。**

このデッキの各ページ：上＝見本／下＝そのままコピペするコード。

---

## 1. 横フロー（基本）

<div class="flow">
  <span class="node">素材</span>
  <span class="node">指示</span>
  <span class="node accent">AIに作らせる</span>
  <span class="node">人が確認</span>
</div>

```html
<div class="flow">
  <span class="node">素材</span>
  <span class="node">指示</span>
  <span class="node accent">AIに作らせる</span>
  <span class="node">人が確認</span>
</div>
```

- `accent` ＝ 青塗りで強調 ／ 何もつけなければ薄青の四角

---

## 2. 従来 vs AI＋（対比フロー）

<div class="flow-set">
  <div class="flow-label now">従来</div>
  <div class="flow">
    <span class="node plain">わかる</span>
    <span class="node plain">やってみる</span>
    <span class="node plain">できる</span>
  </div>
  <div class="flow-label next">AI＋</div>
  <div class="flow">
    <span class="node accent">やってみる</span>
    <span class="node accent">まちがう</span>
    <span class="node accent">修正する</span>
  </div>
</div>

```html
<div class="flow-set">
  <div class="flow-label now">従来</div>
  <div class="flow">
    <span class="node plain">わかる</span>
    <span class="node plain">やってみる</span>
    <span class="node plain">できる</span>
  </div>
  <div class="flow-label next">AI＋</div>
  <div class="flow">
    <span class="node accent">やってみる</span>
    <span class="node accent">まちがう</span>
    <span class="node accent">修正する</span>
  </div>
</div>
```

- `plain` ＝ グレー（従来・Before側） ／ `flow-label now / next` ＝ 見出し

---

## 3. 縦フロー（.col）

<div class="flow col">
  <span class="node">お客様の課題を調べる</span>
  <span class="node accent">AIと対話して仮説を立てる</span>
  <span class="node">ペーパー＋デモを準備</span>
</div>

```html
<div class="flow col">
  <span class="node">お客様の課題を調べる</span>
  <span class="node accent">AIと対話して仮説を立てる</span>
  <span class="node">ペーパー＋デモを準備</span>
</div>
```

- `flow col` にすると縦並び＋矢印は「↓」。長いラベルは縦フロー向き。

---

## 4. 円ノード（短い語だけ）

<div class="flow">
  <span class="node circle">録画</span>
  <span class="node circle accent">要約</span>
  <span class="node circle">議事録</span>
</div>

```html
<div class="flow">
  <span class="node circle">録画</span>
  <span class="node circle accent">要約</span>
  <span class="node circle">議事録</span>
</div>
```

- `circle` ＝ 円。**2〜3文字の短い語向け**（長い語ははみ出すので四角に）。

---

## 5. ゴール（緑）＋区切り記号（＋ / ⇄）

<div class="flow">
  <span class="node plus">素材</span>
  <span class="node">指示</span>
  <span class="node swap">AIに作らせる</span>
  <span class="node goal">人が確認</span>
</div>

```html
<div class="flow">
  <span class="node plus">素材</span>
  <span class="node">指示</span>
  <span class="node swap">AIに作らせる</span>
  <span class="node goal">人が確認</span>
</div>
```

- `goal` ＝ 緑（ゴール・人が確認の工程） ／ `plus`・`swap` ＝ そのノードの**右に出る記号**を `＋`・`⇄` に変える（既定は `→`）

---

## 6. 部品の早見表

| やりたいこと | 書き方 |
|---|---|
| 四角ノード | `<span class="node">…</span>` |
| 強調（青塗り） | `<span class="node accent">…</span>` |
| ゴール／人が確認（緑） | `<span class="node goal">…</span>` |
| 従来・グレー | `<span class="node plain">…</span>` |
| 枠だけ（白地） | `<span class="node ghost">…</span>` |
| 円（短い語） | `<span class="node circle">…</span>` |
| 区切りを＋にする | `<span class="node plus">…</span>`（このノードの右が＋） |
| 区切りを⇄にする | `<span class="node swap">…</span>`（このノードの右が⇄） |
| 横に並べる | `<div class="flow"> … </div>`（→自動） |
| 縦に並べる | `<div class="flow col"> … </div>`（↓自動） |
| 2本を対比 | `<div class="flow-set">` ＋ `<div class="flow-label now/next">` |
| ノード内で改行 | `…<br>…` |

> 迷ったら **このページの上の見本ページをコピペ**して語だけ差し替えるのが速いです。
