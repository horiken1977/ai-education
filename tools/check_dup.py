#!/usr/bin/env python3
"""更新ごとの整合チェック：データソースの重複・表示のダブりを検出する番人。

検出するもの:
  1) データ重複  … レベル定義の表が、設計書のマスタ以外に“直書き”されている
                   （正：curriculum.md のマスタを snippets で取り込む）
  2) 表示ダブり  … 同じページ内に同じ見出し(H1/H2)が2回以上
  3) ナビ重複    … mkdocs.yml の nav に同じファイルパスが2回以上

docs/slides/ は Marp デッキ（別媒体・反復構造あり）なので対象外。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

# レベル定義の正本（マスタ）。ここ“だけ”に表があってよい
MASTER = DOCS / "design" / "curriculum.md"
CANON_LEVELS = [
    "オンボーディング",
    "LV1 チャットAI使い倒し",
    "LV2 Bobでデモ",
    "LV3 使い分け",
    "エクストラ",
]

errors = []


def md_files():
    for p in DOCS.rglob("*.md"):
        if "slides" in p.relative_to(DOCS).parts:
            continue  # Marp デッキは対象外
        yield p


def strip_code_fences(text):
    """``` で囲まれたコードブロックを除外（見出し誤検知を防ぐ）。"""
    parts = text.split("```")
    return "".join(parts[i] for i in range(0, len(parts), 2))


# --- 1) データ重複：レベル定義表の単一ソース ---
for lvl in CANON_LEVELS:
    pat = re.compile(r"\|\s*\*\*" + re.escape(lvl))  # 表セル「| **<レベル名>」
    hits = [p for p in md_files() if pat.search(p.read_text(encoding="utf-8"))]
    extra = [str(p.relative_to(ROOT)) for p in hits if p != MASTER]
    if extra:
        errors.append(
            f"[データ重複] レベル定義「{lvl}」の表が {extra} にも直書きされています。"
            f" 設計書(design/curriculum.md)のマスタを snippets で取り込んでください。"
        )

# --- 2) 表示ダブり：ページ内の見出し重複（H1/H2） ---
for p in md_files():
    body = strip_code_fences(p.read_text(encoding="utf-8"))
    heads = re.findall(r"^(#{1,2})\s+(.+?)\s*$", body, re.MULTILINE)
    seen = {}
    for level, title in heads:
        key = (level, title.strip())
        seen[key] = seen.get(key, 0) + 1
    dups = [f"{lv} {t}" for (lv, t), n in seen.items() if n > 1]
    if dups:
        errors.append(f"[表示ダブり] {p.relative_to(ROOT)} に同じ見出しが重複: {dups}")

# --- 3) ナビ重複：mkdocs.yml の nav に同じパスが複数 ---
if MKDOCS.exists():
    paths = re.findall(r":\s*([\w\-./]+\.md)\s*$", MKDOCS.read_text(encoding="utf-8"), re.MULTILINE)
    dup_paths = sorted({x for x in paths if paths.count(x) > 1})
    if dup_paths:
        errors.append(f"[ナビ重複] mkdocs.yml の nav に同じパスが複数あります: {dup_paths}")

if errors:
    print("整合チェック失敗（重複・ダブり）:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("OK: データ重複・表示ダブり・ナビ重複なし")
