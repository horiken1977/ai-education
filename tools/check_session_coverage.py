#!/usr/bin/env python3
"""サブ回カバレッジの番人（curriculum §4スケジュールが正本）。

`docs/design/curriculum.md` の `[start:schedule]`〜`[end:schedule]` 区画から
サブ回トークン `LV<n>-<x>`（例: LV1-a, LV3-d）を抽出し、その各サブ回について
**台本 `docs/scripts/l<n>.md` と スライド `docs/slides/l<n>.md` の両方に
対応する見出し**（`#` で始まる行に `LV<n>-<x>` を含む）が在るかを検査する。

なぜ必要か（既存 `check_slide_sync.py` の穴）：
  既存番人は**レベル単位の概念マーカー**しか見ないため、
  「curriculum にサブ回を定義したのに台本・スライドが未作成」という抜けを
  緑のまま通してしまっていた（LV1-c/LV2-b,c/LV3-b,c,d が長らく未整備だった原因）。
  本番人は **curriculum のサブ回定義＝正本** を起点に、台本とスライド両方の
  “実在する見出し” を要求することで、定義と教材のドリフトを構造的に塞ぐ。

仕様メモ：
  - サフィックス（a〜d）の無い回（例 W9「LV2 実戦」）は対象外＝仕様どおり。
  - 見出し行（`#`）でのみ判定する。本文中に token を書いただけでは通さない
    （＝“章・節としての教材”が在ることを要求する）。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CURRICULUM = DOCS / "design" / "curriculum.md"

TOKEN = re.compile(r"LV(\d)-([a-d])")


def extract_schedule_tokens(text):
    """schedule スニペット区画から LV<n>-<x> を重複なく順序保持で抽出。"""
    m = re.search(
        r"\[start:schedule\](.*?)\[end:schedule\]", text, flags=re.DOTALL
    )
    if not m:
        return None
    region = m.group(1)
    seen, tokens = set(), []
    for lv, sfx in TOKEN.findall(region):
        key = f"LV{lv}-{sfx}"
        if key not in seen:
            seen.add(key)
            tokens.append((key, lv, sfx))
    return tokens


def has_heading(path, token):
    """`#` で始まる見出し行に token を含むか。"""
    if not path.exists():
        return None
    pat = re.compile(r"^#+ .*" + re.escape(token))
    for line in path.read_text(encoding="utf-8").splitlines():
        if pat.search(line):
            return True
    return False


def main():
    if not CURRICULUM.exists():
        print(f"NG: 正本 {CURRICULUM.relative_to(ROOT)} が見つかりません。")
        return 1
    text = CURRICULUM.read_text(encoding="utf-8")
    tokens = extract_schedule_tokens(text)
    if tokens is None:
        print(
            "NG: curriculum.md に [start:schedule]〜[end:schedule] 区画が見つかりません。"
        )
        return 1

    errors = []
    for token, lv, _sfx in tokens:
        script = DOCS / "scripts" / f"l{lv}.md"
        slide = DOCS / "slides" / f"l{lv}.md"
        missing = []
        for label, p in (("台本 " + str(script.relative_to(ROOT)), script),
                         ("スライド " + str(slide.relative_to(ROOT)), slide)):
            found = has_heading(p, token)
            if found is None:
                missing.append(f"{label}（ファイルが無い）")
            elif not found:
                missing.append(label)
        if missing:
            errors.append(
                f"[{token}] の見出しが {' / '.join(missing)} に見当たりません。"
                f" curriculum §4で定義したサブ回は台本・スライド両方に章を作ってください。"
            )

    if errors:
        print("サブ回カバレッジ検査 失敗（curriculum定義に教材が追いついていない）:")
        for e in errors:
            print("  -", e)
        return 1
    print(
        f"OK: curriculum §4の全サブ回（{len(tokens)}回）が台本・スライド両方に揃っている"
        f"（{', '.join(t[0] for t in tokens)}）"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
