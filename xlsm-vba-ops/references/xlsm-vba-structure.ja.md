# XLSM / VBA 内部構造

[English](xlsm-vba-structure.md)

## ファイル形式

`.xlsm` は `.xlsx` と同じ OPC ZIP パッケージで、追加で VBA プロジェクトのバイナリを持ちます。

```text
Book1.xlsm
├── [Content_Types].xml
├── _rels/.rels
├── xl/
│   ├── workbook.xml
│   ├── worksheets/sheet1.xml
│   ├── vbaProject.bin
│   └── ...
└── docProps/
```

VBA ソースは XML ではなく、`xl/vbaProject.bin` 内の OLE Compound File Binary Format に保存されています。

## `vbaProject.bin`

代表的なストリーム:

| ストリーム | 内容 |
|------------|------|
| `VBA/ThisWorkbook` | ThisWorkbook モジュール |
| `VBA/Sheet1` | ワークシートモジュール |
| `VBA/Module1` | 標準モジュール |
| `VBA/_VBA_PROJECT` | プロジェクトメタデータ |
| `VBA/dir` | 圧縮されたモジュール一覧と属性 |

## 書き戻しをしない理由

安全に VBA を書き戻すには、圧縮ソース、OLE 構造、Excel のコンパイル状態を整合させる必要があります。最も確実なのは Excel VBE で貼り付け、Excel に再コンパイルさせる方法です。

## モジュール種別

| 拡張子 | 種別 | 例 |
|--------|------|----|
| `.cls` | クラスまたは Excel オブジェクト | `ThisWorkbook.cls`, `Sheet1.cls` |
| `.bas` | 標準モジュール | `Module1.bas` |
| `.frm` | UserForm | `UserForm1.frm` |
