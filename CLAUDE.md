# CLAUDE.md

## プロジェクト概要
- **目的**: 北海道食材販売データのEDA（探索的データ分析）練習
- **データ**: 2024年の架空販売データ（テスト用）
- **評価指標**: データの特徴把握、売上傾向の可視化、顧客セグメント分析

## データセット情報

### 販売データ (data/raw/sales.csv)
| カラム名 | 型 | 説明 | 備考 |
|----------|-----|------|------|
| order_id | int | 注文ID | 一意識別子 |
| order_date | date | 注文日 | YYYY-MM-DD形式 |
| customer_id | str | 顧客ID | C0001形式 |
| customer_type | str | 顧客種別 | toB / toC |
| region | str | 地域 | 関東/関西/北海道/その他 |
| product_category | str | 商品カテゴリ | 水産物/畜産物/農産物/酒類 |
| product_name | str | 商品名 | |
| quantity | int | 数量 | |
| unit_price | int | 単価（円） | |
| total_amount | int | 売上金額（円） | quantity × unit_price |
| channel | str | 販売チャネル | 直販/EC/卸 |
| is_repeat | int | リピート購入フラグ | 0/1、約10%欠損 |

### 顧客データ (data/raw/customers.csv)
| カラム名 | 型 | 説明 | 備考 |
|----------|-----|------|------|
| customer_id | str | 顧客ID | C0001形式 |
| customer_type | str | 顧客種別 | toB / toC |
| industry | str | 業種（toBのみ） | ホテル/レストラン/小売/その他、toCはnull |
| prefecture | str | 都道府県 | |
| first_order_date | date | 初回注文日 | |
| total_orders | int | 累計注文回数 | |

## 技術スタック
- Python 3.x
- pandas, numpy, matplotlib, seaborn
- scikit-learn（必要に応じて）

## ディレクトリルール
- **data/raw/**: 元データ、**編集禁止**
- **data/processed/**: 加工済みデータ
- **experiments/exp001_baseline/outputs/**: 分析出力物
- 図表は PNG 形式で保存

## コーディング規約
- 日本語コメント可
- 型ヒント推奨
- 可視化の日本語表示対応（japanize-matplotlib または font設定）

## EDA標準フロー
1. データ読み込み・基本統計量確認
2. 欠損値・データ型の確認
3. 売上の時系列推移（月別・週別）
4. 商品カテゴリ別・チャネル別の売上分析
5. 顧客種別（toB/toC）の比較
6. 地域別分析
7. 相関分析・クロス集計
8. 結果をMarkdownレポートにまとめる

## ドメイン知識（北海道食材商社）
- **水産物**: カニ、ウニ、サケ、タコ等。季節性あり（年末需要大）
- **畜産物**: エゾシカ、あか牛。通年だがジビエは秋冬に需要増
- **農産物**: じゃがいも、アスパラ、メロン等。季節商品多い
- **酒類**: 日本酒、ワイン。ギフト需要で年末・中元時期に増加
- **toB顧客**: ホテル・レストラン・百貨店等。大口・継続取引
- **toC顧客**: EC経由の個人。単発購入が多いがリピーター獲得が課題

## 禁止事項
- data/raw/ 配下のファイル編集・削除
- 分析途中での安易な外れ値除外（まず原因を確認）
