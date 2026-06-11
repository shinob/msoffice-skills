# PPTX テキスト構造リファレンス

[English](pptx-text-structure.md)

## PPTX は ZIP パッケージ

`.pptx` は ZIP パッケージです。XML を確認する前に展開します。

```bash
python3 pptx-text-ops/scripts/unpack.py presentation.pptx unpacked/
```

主なファイル:

```text
ppt/slides/slideN.xml              表示されるスライド本文
ppt/notesSlides/notesSlideN.xml    スピーカーノート
ppt/comments/commentN.xml          コメント
ppt/charts/chartN.xml              グラフラベルやキャッシュ文字列
ppt/slideMasters/                  マスター。明示された場合のみ編集
ppt/slideLayouts/                  レイアウト。明示された場合のみ編集
```

## テキストの場所

多くのテキストは DrawingML の `<a:t>` に入っています。

```xml
<a:txBody>
  <a:p>
    <a:r>
      <a:t>スライド本文</a:t>
    </a:r>
  </a:p>
</a:txBody>
```

書式やリンクにより、見た目上 1 つの語句が複数 run に分かれることがあります。

## ノート、マスター、レイアウト

スピーカーノートは `ppt/notesSlides/notesSlideN.xml` にあります。マスターやレイアウトは継承元なので、明示的に必要な場合だけ編集します。

## リレーションシップ

テキストのみの変更では `.rels` ファイルを編集しません。
