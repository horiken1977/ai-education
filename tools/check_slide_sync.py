#!/usr/bin/env python3
"""スライド⇄台本の整合チェック（全レベル）。

**スライドを正（マスタ）**とし、各レベルの「受講者向けキー概念」が
台本 `scripts/<lv>.md` と スライド `slides/<lv>.md` の**両方**に存在するかを検査する。
片方に無ければ NG（＝どちらかで概念が抜けた＝ドリフト）。

台本とスライドは別レジスタ（話し言葉／投影用）かつ別ビルド（MkDocs／Marp）で、
スライドは pymdownx snippets が効かない＝手動ミラーになる。そこで「テキスト一致」
ではなく「**キー概念マーカー（正規表現）が両方にあるか**」で整合を担保する。

── マーカー選定の鉄則（過去に番人が“偽の緑”を出した反省）──────────────
  番人は登録した LEVELS しか見ない。だから **各レベルの核心概念は漏れなく登録**する。
  マーカーは「**そのレベルの実体（固有語）でしか一致しない語**」を選ぶ。
  例）× "LV3" だけ → レベル名が別所にあるだけで通る。○ "卒業条件" "紙芝居" "裏取り" …
  概念を増やす/変えるときは、この LEVELS を更新する（= 唯一の受講者向け正本リスト）。
  スライド編集時は各 slides/<lv>.md 冒頭の「消さない語」コメントも合わせて更新。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# レベル → 受講者向けキー概念 → 台本・スライド両方に必須の固有マーカー
LEVELS = {
    "onboarding": {
        "前提（営業プロセスの変革）": ["一気通貫", "RFP"],
        "設計の重心": ["手を動か", "成果物"],
        "レベル定義と卒業条件": ["卒業条件", "LV3"],
        "学びの変化（失敗して修正）": ["失敗", "修正"],
        "3ヶ月スケジュール（混在型）": ["混在型", "7割"],
    },
    "l1": {
        "調べる＝AIリサーチ／人が裏取り": ["リサーチ", "裏取り"],
        "ICA・Copilot の使い分け": ["ICA", "Copilot"],
        "ゴール＝チャットAIでPPT": ["PPT"],
        "Genspark でスライド化": ["Genspark"],
        "社外へ渡す前の安全弁（伏字・一般化）": ["伏字"],
        "内省→ブレイクアウト（毎回・今日の問い）": ["今日の問い"],
    },
    "l2": {
        "Bob で紙芝居デモ": ["Bob", "紙芝居"],
        "見せる（画面提示）": ["見せ", "画面提示"],
        "内省→ブレイクアウト（毎回・今日の問い）": ["今日の問い"],
    },
    "l3": {
        "AI の使い分け": ["使い分け"],
        "案件まるごと1周": ["案件", "フォロー"],
        "品質管理（人が最終チェック）": ["品質"],
        "内省→ブレイクアウト（毎回・今日の問い）": ["今日の問い"],
    },
    "extra": {
        "使う側→作る側": ["作る側"],
        "GitHub公開・URLで渡す": ["公開", "URL"],
    },
}


def visible(text):
    """HTMLコメント（<!-- -->）を除去して“実際に見える中身”だけを残す。
    編集リマインダのコメントや Marp ディレクティブにマーカー語が入っていても、
    それで整合チェックが通ってしまう“偽の緑”を防ぐ（実体でだけ判定する）。"""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


errors = []
for lv, checks in LEVELS.items():
    script = DOCS / "scripts" / f"{lv}.md"
    slide = DOCS / "slides" / f"{lv}.md"
    texts, ok = {}, True
    for p in (script, slide):
        if not p.exists():
            errors.append(f"[{lv}] {p.relative_to(ROOT)} が見つかりません。")
            ok = False
        else:
            texts[p] = visible(p.read_text(encoding="utf-8"))
    if not ok:
        continue
    for concept, markers in checks.items():
        for m in markers:
            pat = re.compile(m)
            missing = [str(p.relative_to(ROOT)) for p in (script, slide) if not pat.search(texts[p])]
            if missing:
                errors.append(
                    f"[{lv}｜受講者向け不整合] 「{concept}」のキー概念『{m}』が {' / '.join(missing)} に"
                    f" 見当たりません。台本とスライドの両方に入れてください（スライドが正）。"
                )

if errors:
    print("整合チェック失敗（スライド⇄台本の受講者向け概念が揃っていない）:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
n_lv = len(LEVELS)
n_c = sum(len(c) for c in LEVELS.values())
print(f"OK: 全{n_lv}レベルの受講者向け概念（{n_c}項目）が台本・スライド両方に揃っている")
