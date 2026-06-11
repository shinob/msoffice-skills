# PPTX Text Operations Skill

[English](SKILL.md)

既存の `.pptx` ファイルのテキストだけを編集するスキルです。レイアウト、画像、マスター、テーマ、リレーションシップを保持します。

## 使う場面

- スライド本文の書き換え、翻訳、校正
- スピーカーノートの編集
- 用語統一、プレースホルダー削除
- 既存デッキのレイアウトを維持したい場合

## 対象外

- 新規デッキの作成
- レイアウト、配色、テーマの再設計
- アニメーション編集
- グラフや埋め込みブックの再構築

## 基本ワークフロー

1. 元ファイルをコピーする。
2. `python3 pptx-text-ops/scripts/extract.py working_copy.pptx` で全テキストを確認する。
3. `python3 pptx-text-ops/scripts/unpack.py working_copy.pptx unpacked/` で展開する。
4. `ppt/slides/slideN.xml`、`ppt/notesSlides/notesSlideN.xml` など対象 XML を最小限編集する。
5. `python3 pptx-text-ops/scripts/pack.py unpacked/ edited.pptx` で再梱包する。
6. `extract.py` と目視確認でテキスト抜け・重複・はみ出しを確認する。

## 安全ルール

- `.rels` ファイルは編集しない。
- `r:id` を削除・変更しない。
- XML を正規表現だけで置換しない。
- 長い翻訳や書き換えではテキストはみ出しリスクを確認する。

詳細は [pptx-text-structure.ja.md](references/pptx-text-structure.ja.md) と [text-edit-recipes.ja.md](references/text-edit-recipes.ja.md) を参照してください。
