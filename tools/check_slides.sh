#!/usr/bin/env bash
# スライド手編集後のローカル整合チェック（CIの“速い部分”をまとめて実行）。
#   使い方:  bash tools/check_slides.sh
#   緑なら push してOK（push＝自動デプロイ）。赤ならメッセージに従って直す。
# ※ 見た目（レンダリング）は VS Code の「Marp for VS Code」プレビューで確認するのが速い。
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
fail=0

echo "== 1) 重複・ダブり (check_dup.py) =="
python3 tools/check_dup.py || fail=1

echo "== 2) 受講者向け概念の 台本⇄スライド 整合・全レベル (check_slide_sync.py) =="
python3 tools/check_slide_sync.py || fail=1

echo "== 2b) curriculum定義のサブ回カバレッジ (check_session_coverage.py) =="
python3 tools/check_session_coverage.py || fail=1

echo "== 3) 旧表記の検査 =="
if grep -rnE "L1 初心者|L2 初級|L3 上級|初級〜中級|3つのレベル|初心者ゼロ|半数以上が上級|営業向けAI研修" docs mkdocs.yml --exclude=maintenance.md; then
  echo "  -> NG: 旧表記が残っています（上記の行）。設計書(curriculum.md)の表記に直す。"
  fail=1
else
  echo "OK: 旧表記なし"
fi

# 4) 任意: mkdocs が入っていれば strict build も回す（リンク切れ検出）。無ければスキップ。
if command -v mkdocs >/dev/null 2>&1; then
  echo "== 4) mkdocs build --strict（任意） =="
  TMP="$(mktemp -d)"
  if mkdocs build --strict -d "$TMP" >/dev/null 2>&1; then echo "OK: strict build"; else echo "  -> NG: strict build 失敗"; fail=1; fi
  rm -rf "$TMP"
else
  echo "== 4) mkdocs 未導入のためスキップ（Marpプレビューで見た目を確認） =="
fi

echo ""
if [ "$fail" -eq 0 ]; then
  echo "✅ すべて緑：push して大丈夫です（push＝自動デプロイ）。"
else
  echo "❌ 赤があります：上のメッセージに従って直してから push してください。"
fi
exit $fail
