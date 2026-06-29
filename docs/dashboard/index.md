# KPIダッシュボード

各回のレベル診断（Microsoft Forms）結果をもとに、**レベル分布の推移**を表示します。
3ヶ月で「L1（初心者）が減り、L3（上級）が増える」ことが目標です。

!!! info "データの更新方法"
    1. レベル診断 Forms の回答を CSV エクスポート
    2. 週次集計を `docs/dashboard/data/levels.csv` に1行追記してコミット（`week,L1,L2,L3`）
    3. このページのグラフに自動反映されます
    
    現在のデータは初期サンプル（W1）です。運用開始後、実データに置き換えてください。

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

## 目標ライン（3ヶ月後）
| 指標 | 目標 |
|---|---|
| L1（初心者）人数 | **0人** |
| L3（上級）比率 | **受講者の50%超** |
| 週次AI利用率 | 80%以上が「週3回以上利用」 |
| 横展開 | L3卒業者が1人1資産以上をチームへ共有 |

!!! warning "外部CDNが使えない環境では"
    社内ネットワークで jsdelivr（Chart.js のCDN）がブロックされる場合は、Chart.js を `docs/assets/` に同梱するか、GitHub Actions で CSV からグラフ画像（PNG/SVG）を生成して埋め込む方式に切り替えてください（[GitHub運用設計](../design/github-ops.md) §7 参照）。
