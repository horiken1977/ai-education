# KPIダッシュボード

レベル診断（Microsoft Forms）の結果をもとに、**到達レベルの分布が3ヶ月でどう動くか**（LV1が減りLV3・エクストラが増える）を表示します。
運用は **「Formsの結果をCSVで書き出して `data/responses.csv` に置く（上書き）」だけ**。集計はこのページのJavaScriptが自動で行います。

!!! warning "公開リポジトリなので個人情報は載せない"
    このサイトは公開です。CSVに **氏名・メールアドレスを含めない**でください。
    対策：Formsを **匿名（名前を記録しない）** に設定する。集計に必要なのは「[週]」と「[到達]」の2列だけです。

---

## 1. Forms の設計（推奨）
質問タイトルの**先頭に `[タグ]` を付ける**と、ダッシュボードが列を確実に拾えます（Formsの列見出し＝質問文そのままのため）。

| 質問（タイトル例） | 形式 | 選択肢／用途 | ダッシュボード |
|---|---|---|---|
| `[週] 今回の研修回` | 単一選択 | `W1`,`W2`, … `W12`（または実施日） | **横軸（必須）** |
| `[到達] 現時点のあなたの到達レベル` | 単一選択 | `オンボーディング`,`LV1`,`LV2`,`LV3`,`エクストラ` | **集計の主軸（必須）** |
| `[出席] 今回出た回` | 単一選択 | 同上（任意） | 参考 |
| `[自己評価] 今日の手応え` | 単一選択 | `1`〜`5`（任意） | 参考 |
| 自由記述（困りごと・要望） | 記述式 | （任意） | 集計対象外 |

- **設定**：回答受付＝匿名（名前を記録しない）。`[到達]` は卒業条件（[カリキュラム設計書](../design/curriculum.md) §2）を満たした最上位レベルを選んでもらう。
- 選択肢ラベルは **`LV1` など短く固定**（表記ゆれを避けると集計が安定）。
- 1つのFormを毎週使い回し、`[週]` で回を区別 → **エクスポートは常に1ファイル**で済む。

## 2. 運用（毎回これだけ）
1. Forms の「応答」→ **エクスポート**（Excelで開く →「名前を付けて保存」で **CSV UTF-8**）。
2. 書き出したCSVを **`docs/dashboard/data/responses.csv` に上書き**してコミット（push）。
3. 数分後、このページのグラフが自動更新（Formsは累積エクスポートなので毎回まるごと上書きでOK）。

> CSVに氏名・メール列が残っている場合は、コミット前に削除（`[週]`/`[到達]` 列があれば動きます）。

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
function normLevel(v){ if(!v)return null; if(v.includes('オンボ'))return 'オンボーディング';
  for(const L of ['LV1','LV2','LV3']) if(v.includes(L))return L;
  if(v.includes('エクストラ')||v.toLowerCase().includes('extra'))return 'エクストラ'; return null; }
fetch('data/responses.csv').then(r=>r.text()).then(text=>{
  const rows=parseCSV(text).filter(r=>r.some(c=>(c||'').trim()!==''));
  const header=rows.shift()||[];
  const col=kw=>header.findIndex(h=>(h||'').includes(kw));
  const wi=col('[週]'), li=col('[到達]');
  if(wi<0||li<0){ document.getElementById('dashMsg').textContent='CSVに [週] または [到達] の列が見つかりません。質問タイトルにタグを付けてください。'; return; }
  const counts={};
  rows.forEach(r=>{ const w=(r[wi]||'').trim(); const lv=normLevel((r[li]||'').trim());
    if(!w||!lv)return; (counts[w]=counts[w]||{})[lv]=(counts[w][lv]||0)+1; });
  const weeks=Object.keys(counts).sort((a,b)=>((parseInt(a.replace(/\D/g,''))||0)-(parseInt(b.replace(/\D/g,''))||0))||a.localeCompare(b));
  if(!weeks.length){ document.getElementById('dashMsg').textContent='有効な回答がまだありません。'; return; }
  const datasets=LEVELS.map(L=>({label:L,data:weeks.map(w=>counts[w][L]||0),backgroundColor:COLORS[L]}));
  new Chart(document.getElementById('distChart'),{type:'bar',data:{labels:weeks,datasets},
    options:{plugins:{title:{display:true,text:'到達レベルの分布（回ごと・人数）'}},responsive:true,
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
