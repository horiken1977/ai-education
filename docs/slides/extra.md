---
marp: true
theme: ibm
paginate: true
header: 'AIレベルアップセッション — エクストラ（希望者）'
---

<!--
編集メモ（スライドには映りません）── エクストラの「消さない語」＝番人 tools/check_slide_sync.py が監視。
言い回しは自由。ただし次の語をスライドから消すとCIが赤：作る側 / 公開 / URL
語ごと変えるときは check_slide_sync.py の LEVELS[extra] と 台本 scripts/extra.md も更新。編集後: bash tools/check_slides.sh
-->

<!-- _class: lead -->
# エクストラ Bobでミニアプリ
## 定義：AIを“使う側”から“作る側”へ

**このレベルが終わったら…**
業務課題を解くミニアプリをBobで作り、**GitHubで公開してURLで渡せる**

<small>営業フロー上の担当：⑥作る／対象：希望者（LV2クリア）</small>

---

## LV2との違い

| | できること |
|---|---|
| LV2 | 紙芝居デモを**画面提示** |
| **エクストラ** | 実際に動かして**URLで渡す**（デモの“その先”） |

> 対象：希望者（LV2クリア）。並行枠／オフィスアワーで自分のペースに。

---

## 安全（公開＝誰でも見える）

- お客様の**実データ・社外秘は入れない**（架空データのみ）
- 機密は公開しない
- 公開・セキュリティに迷ったら**公開前に情シス／TAへ確認**

---

## エクストラの実施の流れ（4ステップ）

<style scoped>.flow .node { font-size: .78em; }</style>

<div class="flow">
  <span class="node">①課題を選ぶ<br><small>誰が・どの画面で</small></span>
  <span class="node swap">②Bobで作る<br><small>動く最小版(MVP)</small></span>
  <span class="node">③公開する<br><small>GitHubでURL</small></span>
  <span class="node goal">④共有する<br><small>反応を1つ記録</small></span>
</div>

```text
① 課題を選ぶ   → 何を・誰が・どの画面で（1枚で言える）
② Bobで作る    → 動く最小版（MVP）。対話で反復、コードは書かない
③ 公開する     → GitHubに上げて URL を出す（Pages）
④ 共有する     → お客様/チームにURL。反応を1つ記録
```

---

## ② Bobへの最初の一言

```text
◯◯業務を助ける簡単なWebアプリを作りたい。
使う人：__／やりたいこと：__／画面：__
まずは動く最小版（MVP）で。データは架空でOK。
```

> 完璧を目指さない。**動く最小版をまず1つ。**

---

<!-- _class: lead -->
## ここまで来たら、あなたは「作る側」

**“資料を送る”より“触れるものを送る”。**

🎯 成果物：お客様/チームに渡せる **公開URLのミニアプリ 1つ**（架空データ）

作ったURLは共有ライブラリへ。次の“作る人”を増やそう！
