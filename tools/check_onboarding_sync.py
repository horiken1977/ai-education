#!/usr/bin/env python3
"""受講者向け正本ブロックの整合チェック（設計書 → 台本＋スライド）。

設計書(curriculum.md)の冒頭ブロックのうち「オンボーディングで受講者に説明する」
と決めたものは、**台本(scripts/onboarding.md)とスライド(slides/onboarding.md)の
両方**に必ず提示されていなければならない（どちらか一方に入れ忘れる＝ドリフト）。

台本とスライドは別レジスタ（話し言葉／投影用）かつ別ビルド（MkDocs／Marp）で、
スライドは pymdownx snippets が効かない＝手動ミラーになる。そこで「テキスト一致」
ではなく「**キー概念マーカー（正規表現）が両方にあるか**」で整合を担保する。

── マーカー選定の鉄則（過去に番人が“偽の緑”を出した反省）──────────────
  番人は登録した CHECKS しか見ない。だから **受講者向けブロックは漏れなく登録**する。
  さらにマーカーは「**そのブロックの実体（固有語）でしか一致しない語**」を選ぶ。
  例）× "LV3" だけ → レベル名が別所にあるだけで通ってしまう（卒業条件が無くても緑）。
      ○ "卒業条件" "12週" "7割" "一気通貫" "成果物" … 実体が無いと出てこない語。
  ブロックを増やす/変えるときは、この CHECKS を更新する（= 唯一の受講者向け正本リスト）。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "docs" / "scripts" / "onboarding.md"
SLIDE = ROOT / "docs" / "slides" / "onboarding.md"

# 受講者向け正本ブロック（設計書冒頭）→ 台本・スライド両方に必須の固有マーカー。
# 各マーカーが SCRIPT と SLIDE の両方に無ければ NG。マーカーは“実体でしか一致しない語”。
CHECKS = {
    "前提（営業プロセスの変革）": ["一気通貫", "RFP"],
    "設計の重心": ["手を動か", "成果物"],
    "レベル定義と卒業条件": ["卒業条件", "LV3"],
    "背骨（業務フロー×渡し方）": ["①調べる", "渡し方"],
    "3ヶ月（12週）スケジュール": ["12週", "7割"],
}

errors = []
for path in (SCRIPT, SLIDE):
    if not path.exists():
        errors.append(f"[ファイル無し] {path.relative_to(ROOT)} が見つかりません。")

def visible(text):
    """HTMLコメント（<!-- -->）を除去して“実際に見える中身”だけを残す。
    編集リマインダのコメントや Marp ディレクティブにマーカー語が入っていても、
    それで整合チェックが通ってしまう“偽の緑”を防ぐ（実体でだけ判定する）。"""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


if not errors:
    texts = {p: visible(p.read_text(encoding="utf-8")) for p in (SCRIPT, SLIDE)}
    for block, markers in CHECKS.items():
        for m in markers:
            pat = re.compile(m)
            missing = [p.relative_to(ROOT) for p in (SCRIPT, SLIDE) if not pat.search(texts[p])]
            if missing:
                where = " / ".join(str(x) for x in missing)
                errors.append(
                    f"[受講者向け不整合] ブロック「{block}」のキー概念『{m}』が {where} に見当たりません。"
                    f" 台本とスライドの両方に、このブロックの実体を入れてください。"
                )

if errors:
    print("整合チェック失敗（受講者向け正本が台本・スライドに揃っていない）:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"OK: 受講者向け正本 {len(CHECKS)} ブロックが台本・スライド両方に揃っている")
