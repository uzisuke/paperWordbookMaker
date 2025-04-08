# Paper Wordbook Maker

このスクリプトは、英語のPDF論文から章ごとにテキストを抽出し、OpenAI GPTを使って重要語彙（専門用語や難解な表現など）をリストアップします。
英文で読むことに心理的障壁が高くなっている論文を少しでも読みやすくします。

このスクリプトは、英語のPDF論文から章ごとにテキストを抽出し、OpenAI GPTを使って重要語彙（専門用語や難解な表現など）をリストアップします。

## 🔧 機能概要

- PDFファイルを読み込み、章単位でテキストを分割
- 各章の内容をGPTに送り、重要語彙と日本語訳を抽出
- 結果を `output.txt` にMarkdown形式で保存

## 📦 必要なライブラリ

以下をインストールしてください：

```bash
pip install pymupdf openai tqdm
```

## 🚀 使い方
1. pdf_path に対象のPDFファイルのパスを指定します

2. OpenAI APIキーを openai.api_key に設定します

3. スクリプトを実行します：

```bash
python main.py
```
4. `output.txt` に語彙リストが出力されます

## 📄 出力例

```markdown
    ## Chapter 1
    - sophisticated (洗練された)
    - paradigm shift (パラダイムシフト)
    ...
    ---
```

## ⚠️ 注意
PDFはテキスト抽出可能な形式である必要があります（画像PDFは非対応）

OpenAI APIの使用には課金が発生します