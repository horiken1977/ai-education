#!/usr/bin/env python3
"""アンケートCSV(responses.csv)から、公開に不要な列を除去する（公開リポジトリ対策）。

Forms のエクスポートには メール／名前／自由記述コメント が含まれる。ダッシュボードが
使うのは「完了時刻（日付）」と「到達レベル」だけなので、公開前にこれらを落とす。
使い方（毎回のエクスポート後）:
    python3 tools/sanitize_responses.py   → responses.csv を上書きサニタイズ
除去対象は列見出しに次の語を含む列: メール / 名前 / 書いてください（＝自由記述）。
"""
import csv
import pathlib

CSV = pathlib.Path(__file__).resolve().parent.parent / "docs" / "dashboard" / "data" / "responses.csv"
DROP_KEYWORDS = ["メール", "名前", "書いてください"]

rows = list(csv.reader(CSV.open(encoding="utf-8-sig", newline="")))
if not rows:
    raise SystemExit("responses.csv が空です")
header = rows[0]
drop = [i for i, c in enumerate(header) if any(k in (c or "") for k in DROP_KEYWORDS)]
keep = [i for i in range(len(header)) if i not in drop]
out = [[(r[i] if i < len(r) else "") for i in keep] for r in rows]
with CSV.open("w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(out)
print("除去した列:", [header[i] for i in drop] or "なし")
print(f"残した列: {[header[i] for i in keep]}")
print(f"{len(rows) - 1} 行を保持")
