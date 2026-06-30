#!/usr/bin/env python3
"""受講者向け正本ブロックの整合チェック（設計書 → 台本＋スライド）。

設計書(curriculum.md)の冒頭ブロックのうち「オンボーディングで受講者に説明する」
と決めたものは、**台本(scripts/onboarding.md)とスライド(slides/onboarding.md)の
両方**に必ず登場していなければならない（どちらか一方に入れ忘れる＝ドリフト）。

台本とスライドは別レジスタ（話し言葉／投影用）かつ別ビルド（MkDocs／Marp）で、
スライドは pymdownx snippets が効かない＝手動ミラーになる。そこで「テキスト一致」
ではなく「**キー概念マーカー（正規表現）が両方にあるか**」で整合を担保する。

ブロックを増やすときは CHECKS に1行足すだけ。マーカーは“揺れにくい語”を選ぶ。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "docs" / "scripts" / "onboarding.md"
SLIDE = ROOT / "docs" / "slides" / "onboarding.md"

# 受講者向け正本ブロック → 台本・スライド両方に必須のキー概念（正規表現）。
# 各マーカーが SCRIPT と SLIDE の両方に存在しなければ NG。
CHECKS = {
    "前提（営業プロセスの変革）": ["一気通貫", "RFP"],
    "背骨（業務フロー×渡し方）": ["①調べる", "渡し方"],
    "レベル定義・選び方": ["LV3", r"毎回.{0,8}選"],
    "設計の重心": ["手を動か", "身につ"],
}

errors = []
for path in (SCRIPT, SLIDE):
    if not path.exists():
        errors.append(f"[ファイル無し] {path.relative_to(ROOT)} が見つかりません。")

if not errors:
    texts = {p: p.read_text(encoding="utf-8") for p in (SCRIPT, SLIDE)}
    for block, markers in CHECKS.items():
        for m in markers:
            pat = re.compile(m)
            missing = [p.relative_to(ROOT) for p in (SCRIPT, SLIDE) if not pat.search(texts[p])]
            if missing:
                where = " / ".join(str(x) for x in missing)
                errors.append(
                    f"[受講者向け不整合] ブロック「{block}」のキー概念『{m}』が {where} に見当たりません。"
                    f" 台本とスライドの両方に同じ概念を入れてください。"
                )

if errors:
    print("整合チェック失敗（受講者向け正本が台本・スライドに揃っていない）:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("OK: 受講者向け正本ブロックが台本・スライド両方に揃っている")
