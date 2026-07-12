# KPIダッシュボード

各回の**末尾で答えるアンケート（Microsoft Forms）**をもとに、**到達レベルの分布がセッションを重ねてどう動くか**（LV1が減りLV3・エクストラが増える）を表示します。**回は「完了時刻（日付）」で自動判定**するので、受講者に週番号（W1/W2…）を選ばせる必要はありません（間違い防止）。このアンケートが到達レベル記録＝KPIを兼ねます。
運用は **「Formsの結果をCSVで書き出して `data/responses.csv` に上書き」だけ**。集計はこのページのJavaScriptが自動で行います。

!!! warning "公開リポジトリなので個人情報は載せない"
    このサイトは公開です。CSVに **氏名・メールアドレスを含めない**でください（列があっても空/`anonymous`ならOK）。
    対策：Formsを **匿名（名前・メールを記録しない）** に設定する。集計に使うのは **日付**と**到達レベル**の2列だけです。

---

## 管理者メニュー（教材・設計書・記録へのリンク）

!!! note "ここが管理者用の入口です"
    受講者の左ナビ（ホーム／スライド／セッションの学び の3つだけ）には出していません（受講者用と混在させないため）。設計書・台本・教材などは**この右ペインの目次（見出し）から辿ってください**。以下のページはすべて **nav非表示・直URL到達可** です。

### 設計書（`docs/design/`）
- [カリキュラム設計書](../design/curriculum.md) … **レベル定義の正本**（`--8<-- [start:levels]`）。ここだけを直す。
- [整合を保つ仕組み（メンテ規約）](../design/maintenance.md) … 番人・重複チェック・旧表記禁止の運用。
- [GitHub運用設計](../design/github-ops.md) … push＝自動デプロイ／CI／Pages。
- [講義モード](../design/lecture-mode.md) … 当日の進め方。

### 講師台本（`docs/scripts/`＝分刻みの正）
- [台本ガイド（共通）](../scripts/index.md)
- [オンボーディング](../scripts/onboarding.md) ／ [LV1](../scripts/l1.md) ／ [LV2](../scripts/l2.md) ／ [LV3](../scripts/l3.md) ／ [エクストラ](../scripts/extra.md)

### スライド（`docs/slides/`＝各回の正）
- [スライド一覧（索引）](../slides-index.md) … 各レベルのスライドへ。編集手順は下の §6 参照。

### 配布教材・トランスクリプト（`docs/materials/`）
- [LV1 トランスクリプト（配布用）](../materials/l1-transcript.md)
- [LV1 リサーチ対象](../materials/lv1-research-target.md) ／ [LV2 デモテーマ](../materials/lv2-demo-theme.md) ／ [LV3 ブリーフ](../materials/l3-brief.md)

!!! warning "生の録画・トランスクリプトは公開サイトにありません"
    講義の**生録画・生トランスクリプト（実名・機密）は `records/`＝gitignore のローカル専用**で、公開サイトには載りません（リンク不可）。公開できるのは、そこから作った**匿名の学びノート**（下記）だけです。

### テンプレート集
- [テンプレート集](../toolkit/index.md) … 各回の配布テンプレ（Genspark伏字発注書テンプレ等）。

### セッションの学び（復習・公開）
- [学びノート索引](../review/index.md) … 録画から作った**匿名・構造化**の復習ノート。氏名/顧客/機密は排除。

---

## 1. Forms の設計（実アンケートに自動対応）
特別なタグは不要です。ダッシュボードが**列名（質問文）で自動検出**します。必要なのは次の2つだけ：

| 使う情報 | どの列を見るか（自動検出） | 必要な中身 |
|---|---|---|
| **回（横軸）** | `完了時刻`（無ければ `開始時刻`） | Formsが自動で持つ日時。**日付でその回を判定**（W番号入力は不要） |
| **到達レベル（積み上げ）** | `…どのレベル…` を含む質問（例：`現在ご自身はどのレベルにあると思いますか？`） | 単一選択。`オンボーディング`／`Lv1`／`Lv2`／`Lv3`／`エクストラ` が判別できる表記 |

- **到達レベルの選択肢**は `オンボーディング（レベル０）` `Lv1（レベル１）` … のような表記でOK（ダッシュボードは `オンボ*`／`Lv1〜3`＝`レベル１〜３`／`エクストラ` を吸収）。**新しい表記を足したら** JSの `normLevel` を1行足す。
- **匿名設定**（名前・メールを記録しない）。`メール` 列が `anonymous`・`名前` が空なら公開してもOK。
- **同じ Forms を毎回使い回す**（オンボ含む）。回はアンケートの**回答日**で自動的に分かれるので、受講者は日付も週番号も入力不要。
- 到達レベルは卒業条件（[カリキュラム設計書](../design/curriculum.md) §2）を満たした最上位を選んでもらう。

## 2. 運用（毎回これだけ）
1. Forms の「応答」→ **エクスポート**（Excelで開く →「名前を付けて保存」で **CSV UTF-8**）。※普通の「CSV」だと Shift_JIS で文字化けするので必ず **CSV UTF-8**。
2. 書き出したCSVを **`docs/dashboard/data/responses.csv` にリネームして上書き**。※ダッシュボードは常にこの固定名を読むので、Forms側のファイル名は問わない。
3. **`python3 tools/sanitize_responses.py` を実行**（メール・名前・自由記述コメント列を除去＝公開リポジトリ対策）。集計に使う日付・到達は残る。
4. コミット（push）→ 数分後、このページのグラフが自動更新（Formsは累積エクスポートなので毎回まるごと上書きでOK）。

> **公開注意**：`responses.csv` は公開され誰でもダウンロード可。**手順3のサニタイズを必ず実行**（メール・名前・自由記述コメントは公開しない）。Formsは匿名設定に。

---

## 3. 到達レベルの分布（回ごと）
<canvas id="distChart" height="120"></canvas>
<p id="dashMsg" style="color:#da1e28"></p>

## 4. 最新回の分布 ＆ 目標との比較
<div id="targetBox"></div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const LEVELS=['オンボーディング','LV1','LV2','LV3','エクストラ'];
const COLORS={'オンボーディング':'#a8a8a8','LV1':'#0f62fe','LV2':'#8a3ffc','LV3':'#24a148','エクストラ':'#ff832b'};
const TARGET={'LV2':10,'LV3':70,'エクストラ':20};
function parseCSV(t){
  t=t.replace(/^﻿/,''); const rows=[]; let row=[],cur='',q=false;
  for(let i=0;i<t.length;i++){const c=t[i];
    if(q){ if(c==='"'){ if(t[i+1]==='"'){cur+='"';i++;} else q=false; } else cur+=c; }
    else { if(c==='"')q=true; else if(c===','){row.push(cur);cur='';}
      else if(c==='\n'){row.push(cur);rows.push(row);row=[];cur='';}
      else if(c==='\r'){} else cur+=c; }
  }
  if(cur!==''||row.length){row.push(cur);rows.push(row);}
  return rows;
}
// 到達レベルのラベル正規化（"Lv1（レベル１）" "オンボーディング（レベル０）" 等を吸収）
function normLevel(v){ if(!v)return null; const s=(''+v).toLowerCase();
  if(v.includes('オンボ')||s.includes('レベル０')||s.includes('レベル0')||s.includes('lv0'))return 'オンボーディング';
  if(s.includes('lv1')||v.includes('レベル１')||s.includes('レベル1'))return 'LV1';
  if(s.includes('lv2')||v.includes('レベル２')||s.includes('レベル2'))return 'LV2';
  if(s.includes('lv3')||v.includes('レベル３')||s.includes('レベル3'))return 'LV3';
  if(v.includes('エクストラ')||s.includes('extra'))return 'エクストラ'; return null; }
// 回答日時（"7/3/26 0:30:47" 等）→ セッション日 "YYYY-MM-DD"。回は日付で判定（W番号不要）
function toDate(v){ const p=(''+(v||'')).trim().split(/[ T]/)[0];
  let m=p.match(/^(\d{1,2})\/(\d{1,2})\/(\d{2,4})$/);
  if(m){ let y=+m[3]; if(y<100)y+=2000; return y+'-'+String(+m[1]).padStart(2,'0')+'-'+String(+m[2]).padStart(2,'0'); }
  m=p.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/);
  if(m){ return m[1]+'-'+String(+m[2]).padStart(2,'0')+'-'+String(+m[3]).padStart(2,'0'); }
  return p||null; }
fetch('data/responses.csv').then(r=>r.text()).then(text=>{
  const rows=parseCSV(text).filter(r=>r.some(c=>(c||'').trim()!==''));
  const header=rows.shift()||[];
  const find=(...kws)=>header.findIndex(h=>kws.some(k=>(h||'').includes(k)));
  let di=find('完了時刻'); if(di<0)di=find('開始時刻'); if(di<0)di=find('日付','日時','[週]');
  let li=find('どのレベル'); if(li<0)li=find('到達','[到達]');
  const msg=document.getElementById('dashMsg');
  if(di<0||li<0){ msg.textContent='CSVに「日付（完了時刻/開始時刻）」または「到達レベル（現在ご自身はどのレベル…）」の列が見つかりません。'; return; }
  const counts={};
  rows.forEach(r=>{ const w=toDate(r[di]); const lv=normLevel((r[li]||'').trim());
    if(!w||!lv)return; (counts[w]=counts[w]||{})[lv]=(counts[w][lv]||0)+1; });
  const weeks=Object.keys(counts).sort();  // ISO日付なので文字列ソートで時系列
  if(!weeks.length){ msg.textContent='有効な回答がまだありません（日付・到達レベルの入った行が必要）。'; return; }
  const datasets=LEVELS.map(L=>({label:L,data:weeks.map(w=>counts[w][L]||0),backgroundColor:COLORS[L]}));
  new Chart(document.getElementById('distChart'),{type:'bar',data:{labels:weeks,datasets},
    options:{plugins:{title:{display:true,text:'到達レベルの分布（セッション日ごと・人数）'}},responsive:true,
      scales:{x:{stacked:true},y:{stacked:true,title:{display:true,text:'人数'}}}}});
  const last=weeks[weeks.length-1], c=counts[last], total=LEVELS.reduce((s,L)=>s+(c[L]||0),0)||1;
  const pct=L=>Math.round((c[L]||0)/total*100);
  let html=`<p><b>最新回（${last}）</b> n=${total}</p><table><tr><th>レベル</th><th>人数</th><th>割合</th><th>目標</th></tr>`;
  LEVELS.forEach(L=>{ const t=TARGET[L]?TARGET[L]+'%':'—'; html+=`<tr><td>${L}</td><td>${c[L]||0}</td><td>${pct(L)}%</td><td>${t}</td></tr>`; });
  html+='</table>';
  document.getElementById('targetBox').innerHTML=html;
}).catch(e=>{ document.getElementById('dashMsg').textContent='CSVの読み込みに失敗しました：'+e; });
</script>

---

## 5. 目標ライン（3ヶ月後）
| レベル | 目標 |
|---|---|
| LV2（Bobでデモまで） | **1割** |
| LV3（使い分けまで） | **7割** |
| エクストラ（AIアプリ） | **2割（2〜3人）** |

!!! note "外部CDNが使えない環境では"
    社内で jsdelivr（Chart.js のCDN）が遮断される場合は、Chart.js を `docs/assets/` に同梱するか、グラフ画像をActionsで生成する方式に切り替えます。

---

## 6. 運営者向け：教材（スライド等）を直したいとき

!!! note "スライドを手編集する運用"
    **スライド**＝`docs/slides/*.md`（Marp）。文言は VS Code 拡張「Marp for VS Code」で見ながら編集できます。

    1. 編集したら **`bash tools/check_slides.sh`**（重複・受講者向け整合・旧表記を一括チェック）。
    2. **緑なら** commit → push（＝自動デプロイ）。**赤なら**表示メッセージに従って直す。
    3. 設計書への逆反映・台本への反映・CI・公開まで一気に任せるなら、スキル **`/slide-sync`** を使う。

    - オンボの「消してはいけない語」は `slides/onboarding.md` 冒頭の**非表示コメント**に明記（番人が台本⇄スライドの取りこぼしを検出）。
    - 詳しい規約・チェックリストは [設計の整合を保つ仕組み（メンテ規約）](../design/maintenance.md)。
