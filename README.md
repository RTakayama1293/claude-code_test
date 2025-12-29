# snj-eda-test

Claude Code on the Web のテスト用EDAプロジェクト

## 概要

北海道食材販売データを使ったEDA（探索的データ分析）の練習リポジトリです。

## データ

- `data/raw/sales.csv`: 販売データ（500件）
- `data/raw/customers.csv`: 顧客データ（100件）

※テスト用の架空データです

## 使い方

1. https://claude.ai/code にアクセス
2. このリポジトリを選択
3. 「data/raw/sales.csv のEDAを実行して」と指示

## ディレクトリ構成

```
.
├── CLAUDE.md                 # Claude Code への指示書
├── README.md
├── requirements.txt
├── .claude/
│   └── settings.json         # フック設定
├── data/
│   ├── raw/                  # 元データ（編集禁止）
│   └── processed/            # 加工済みデータ
├── experiments/
│   └── exp001_baseline/      # 実験ディレクトリ
│       └── outputs/          # 分析出力物
└── src/                      # 共通コード（必要に応じて）
```

## 分析観点（例）

- 月別売上推移
- 商品カテゴリ別売上構成
- toB/toC別の購買傾向
- 地域別分析
- リピート購入の傾向
