# VBA 編集ワークフロー

xlsm ファイルの VBA を AI と協力して修正・拡張するための手順書。

---

## 前提環境

### 必要なソフトウェア

| ソフトウェア | 用途 |
|------------|------|
| Python 3.9 以上 | スクリプト実行 |
| Microsoft Excel | VBE（Visual Basic Editor）でコードを貼り付けるために必要 |
| oletools | VBA 書き出しスクリプトが使用 |

### インストール

```bash
# VBA 編集に必須
pip3 install oletools

# xlsx-text-ops を併用してセルテキストも操作する場合のみ
pip3 install openpyxl

# 確認
pip3 list | grep -E "oletools|openpyxl"
```

> **xlsx-text-ops との併用**: VBA が参照するセルデータを確認・編集する場合は
> `xlsx-text-ops` スキルを組み合わせると有効（`openpyxl` が必要になる）。
> VBA 編集のみであれば `openpyxl` は不要。

---

## フロー全体図

```
【初回のみ】
環境構築（上記インストール手順）
      ↓
【毎回ここから】
Step 1: バックアップ作成
      ↓
Step 2: VBA 書き出し（export_vba.py）
      ↓
  ┌───┴────────────────┐
  ↓                   ↓
Step 3a: 修正分析     Step 3b: 機能追加検討   ※ 修正分析を先に推奨
  └───┬────────────────┘
      ↓
Step 4: AI がコードを修正
      ↓
Step 5: VBE 貼り付け
      ↓
Step 6: 反映確認（diff）
      ↓
  ┌───┴──────────────┐
  ↓（確認 OK）        ↓（確認 NG）
 完了              Step 2 から再実施
```

### 実行パターン

| 場面 | 開始ステップ |
|------|------------|
| 初回セットアップ | 環境構築から |
| 同じファイルへの追加修正 | Step 1（バックアップ）から |
| 別の xlsm に切り替える場合 | Step 1 から（環境再構築は不要） |

---

## Step 1: バックアップ作成

```bash
cp target.xlsm target_backup_YYYYMMDD.xlsm
```

修正が失敗した場合に備えて、必ず作業前に作成する。

---

## Step 2: VBA 書き出し

```bash
python3 path/to/xlsm-vba-edit/scripts/export_vba.py target.xlsm
```

`{basename}_VBA/` に以下の構造が生成される:

```
target_VBA/
├── ExcelObjects/   ThisWorkbook・シートモジュール (.cls)
├── Forms/          UserForm (.frm)
├── Modules/        標準モジュール (.bas)
└── Classes/        クラスモジュール (.cls)
```

---

## Step 3a: 修正分析（バグ・品質改善）

AI に分析を依頼し、結果を `{basename}_analysis.md` に書き出す。
プロンプトは `vba-edit-recipes.md` の「修正分析プロンプト」を参照。

---

## Step 3b: 機能追加検討

AI にヒアリングさせ、結果を `{basename}_features.md` に書き出す。
プロンプトは `vba-edit-recipes.md` の「機能追加プロンプト」を参照。

修正分析（Step 3a）を先に完了させることを推奨。既存バグが残った状態で機能追加を行うと原因の切り分けが難しくなるため。

---

## Step 4: AI によるコード修正

AI が `_VBA/` フォルダ内のファイルを Edit ツールで直接修正する。
プロンプトは `vba-edit-recipes.md` の「修正依頼プロンプト」を参照。

### 複数修正を同時に適用する場合

1. 優先度の高いものから1件ずつ適用・確認のサイクルを回す
2. 依存関係がある場合（A の修正が B の前提となる等）は順序を守る
3. `_analysis.md` と `_features.md` を同時に適用する場合は統合プロンプトを使用

---

## Step 5: VBE への貼り付け

AI が案内する修正対象モジュールについて、以下の手順を繰り返す:

1. Excel で `target.xlsm` を開く
2. `Alt+F11`（または ツール > マクロ > Visual Basic Editor）で VBE を開く
3. 左ツリーから対象モジュールをダブルクリック
4. `Ctrl+A` で全選択 → `Delete` で全削除
5. `target_VBA/{サブフォルダ}/{モジュール名}` の内容を貼り付け（`Ctrl+V`）
6. 対象モジュールが複数あれば 3〜5 を繰り返す
7. 全モジュールの貼り付け完了後、`Ctrl+S` で保存

---

## Step 6: 反映確認

VBE への貼り付けと保存が完了したら、AI に確認を依頼する:

```
貼り付けと保存が完了しました。確認をお願いします。
```

AI が `export_vba.py` で再書き出しを行い、diff で修正内容と一致しているかを確認して報告する。

---

## トラブルシューティング

### VBE で構文エラーが表示される

| 原因 | 対処 |
|------|------|
| 文字化け（BOM・エンコーディング不一致） | `export_vba.py` で再書き出し → ファイルの文字コードを確認 |
| 改行コードの不一致（CRLF/LF） | AI に「改行コードを CRLF に統一して再出力してください」と依頼 |
| 構文ミス | エラーメッセージを AI に貼り付け、修正を依頼 |

### diff で想定外の差分が出る

VBE が自動補完する `Attribute` 行や空白の正規化により、diff が大きく見える場合がある。

対処: diff の結果全体を AI に渡し、「意図した変更のみかどうか確認してください」と依頼する。

### 反映後に動作が想定と異なる

| 状況 | 対処 |
|------|------|
| 機能が動かない | VBE に貼り付けたファイルが正しいか再確認。`export_vba.py` で再書き出しして比較 |
| 修正ロジックの誤り | 修正分析（Step 3a）に戻り、修正方針を再検討 |
| 別の機能に影響した | `_analysis.md` の「検証チェックリスト」を実施し、影響範囲を特定 |

### バックアップから戻す

```bash
cp target_backup_YYYYMMDD.xlsm target.xlsm
```
