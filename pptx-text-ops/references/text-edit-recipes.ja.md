# PPTX テキスト編集レシピ

[English](text-edit-recipes.md)

## レシピ 1: 1 つの run 内の文字列を置換

対象文字列が 1 つの `<a:t>` 内にある場合は、そのテキストノードだけを置換します。

## レシピ 2: 複数 run に分かれた文字列を置換

語句が複数の `<a:r>` に分かれている場合は、`a:rPr` を保持しながら各 `<a:t>` を編集します。

## レシピ 3: スピーカーノート

ノートが対象か確認してから、`ppt/notesSlides/notesSlideN.xml` を編集します。

## レシピ 4: プレースホルダー削除

```bash
python3 pptx-text-ops/scripts/extract.py working_copy.pptx | grep -iE "xxxx|lorem|ipsum|tbd|placeholder"
```

抽出結果で対象を確認し、レイアウト側のプレースホルダーを不用意に編集しないようにします。

## レシピ 5: 翻訳

スライド本文、ノート、コメント、グラフ、マスター、レイアウトのどこまで対象か確認します。翻訳後は文字量が増え、図形からはみ出す可能性があります。

## 検証

- 古いテキストが残っていない。
- 新しいテキストが正しい。
- ノートは意図した場合だけ変更されている。
- PowerPoint または LibreOffice Impress で開ける。
