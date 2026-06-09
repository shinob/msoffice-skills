# XLSM / VBA Internal Structure

## ファイル形式

`.xlsm` は ZIP アーカイブ（XLSX と同じ OPC 形式）。VBA は XML ではなくバイナリで格納される。

```
Book1.xlsm (ZIP)
├── [Content_Types].xml
├── _rels/.rels
├── xl/
│   ├── workbook.xml
│   ├── worksheets/sheet1.xml
│   ├── vbaProject.bin   ← VBA コード（OLE Compound Document）
│   └── ...
└── docProps/
```

## vbaProject.bin の構造

`vbaProject.bin` は OLE Compound File Binary Format（CFB/CFBF）と呼ばれるバイナリ形式。

内部に以下のストリームが含まれる：

| ストリーム | 内容 |
|-----------|------|
| `VBA/ThisWorkbook` | ThisWorkbook モジュールのバイナリ |
| `VBA/Sheet1` | Sheet1 モジュールのバイナリ |
| `VBA/Module1` | 標準モジュールのバイナリ |
| `VBA/_VBA_PROJECT` | プロジェクトメタデータ |
| `VBA/dir` | モジュール一覧・属性（圧縮） |

各モジュールストリームにはコンパイル済み p-code とソーステキストの両方が含まれる。ソーステキスト部分は MS-OVBA 圧縮アルゴリズムで圧縮されている。

## oletools / olevba の動作

`oletools` の `VBA_Parser` は以下を行う：

1. ZIP から `vbaProject.bin` を取り出す
2. OLE ストリームを解析して `VBA/dir` を読む
3. 各モジュールストリームのオフセットを確認し、圧縮ソースを展開する
4. プレーンテキストの VBA ソースコードを返す

## なぜ書き戻しが難しいか

- ソーステキストを書き換えると p-code と不整合になる（Excel が自動再コンパイルを試みる）
- OLE ストリームの再パッキング（MS-OVBA 圧縮、CFB 構造の再構築）が必要
- `oletools` は読み取り専用; `olefile` で書き込みは可能だが実装が複雑
- 最も確実な方法は Excel の VBE（Visual Basic Editor）で直接貼り付けること

## モジュールの種類と拡張子

| 拡張子 | 種類 | 例 |
|--------|------|-----|
| `.cls` | クラスモジュール | `ThisWorkbook.cls`, `Sheet1.cls` |
| `.bas` | 標準モジュール | `Module1.bas` |
| `.frm` | UserForm | `UserForm1.frm` |
