# pdf_transcription

フォルダに置いた PDF からテキストを取り出し、PDF ごとにテキストファイルに保存するツール。

```
【page:1】 ---
第４回デジタル社会推進会議  議事録
１ 開催日時
令和５年６月６日（火）８：４５～８：５５
…
-------------
【page:2】 ---
…
```

## 特徴

- フォルダ内の PDF をまとめて処理する
- ページごとに番号の見出しと区切り線を付けて出力する
- 壊れた PDF や読めない PDF は飛ばして、残りの処理を続ける

## 必要なもの

- [uv](https://docs.astral.sh/uv/)（Python とライブラリの管理）

## セットアップ

```bash
git clone https://github.com/takk-o/pdf_transcription.git
cd pdf_transcription
uv sync
```

## 使い方

1. 文字を取り出したい PDF を `pdf/` フォルダに置く
2. 実行する

```bash
uv run pdf_transcription.py
```

3. `text/<PDF のファイル名>.txt` に保存される（UTF-8）

フォルダを変える場合は `--input` と `--output` で指定する。

```bash
uv run pdf_transcription.py --input ~/Downloads/minutes --output ~/Documents/minutes_text
```

### 取り出し方の切り替え

既定では [pdfminer.six](https://github.com/pdfminer/pdfminer.six) を使う。うまく取り出せない PDF は `--engine pypdf` で [pypdf](https://github.com/py-pdf/pypdf) に切り替えて試す。

```bash
uv run pdf_transcription.py --engine pypdf
```

## 注意

- テキストとして文字が埋め込まれている PDF が対象。スキャンした画像だけの PDF からは文字を取り出せない（OCR が必要）。
- 文字コードに変換できない文字は `(cid:7962)` のような番号で出力される。
- 段組みや表は、PDF の作り方によって読み順が崩れることがある。

## 動作確認に使った PDF

政府が公開している会議の議事録で確認した（リポジトリには含めていない）。

- 第 4 回デジタル社会推進会議 議事録（デジタル庁）
- 第 25 回消費者教育推進会議 議事録（消費者庁）

## 技術メモ

- テキストの取り出し：pdfminer.six の `extract_pages()`（既定）、または pypdf の `page.extract_text()`

## 経緯

2024 年 1 月に作成し、2026 年 11 月に公開用に整理した。動作確認環境：Python 3.12、pypdf 6、pdfminer.six。

## ライセンス

[MIT License](LICENSE)
