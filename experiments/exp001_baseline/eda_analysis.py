"""
北海道食材販売データ EDA分析スクリプト
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# 日本語フォント設定（Noto Sans CJK JP）
plt.rcParams['font.family'] = ['Noto Sans CJK JP', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = '/home/user/claude-code_test/experiments/exp001_baseline/outputs'

# データ読み込み
sales = pd.read_csv('/home/user/claude-code_test/data/raw/sales.csv')
customers = pd.read_csv('/home/user/claude-code_test/data/raw/customers.csv')

# 日付型変換
sales['order_date'] = pd.to_datetime(sales['order_date'])
sales['month'] = sales['order_date'].dt.to_period('M')

print("=" * 60)
print("1. 基本統計量")
print("=" * 60)
print(f"\n【販売データ概要】")
print(f"レコード数: {len(sales)}")
print(f"期間: {sales['order_date'].min()} ～ {sales['order_date'].max()}")
print(f"\n【数値カラムの統計量】")
print(sales[['quantity', 'unit_price', 'total_amount']].describe())

print("\n" + "=" * 60)
print("2. 欠損値・データ型の確認")
print("=" * 60)
print("\n【データ型】")
print(sales.dtypes)
print("\n【欠損値数】")
print(sales.isnull().sum())
print(f"\nis_repeat欠損率: {sales['is_repeat'].isnull().sum() / len(sales) * 100:.1f}%")

print("\n" + "=" * 60)
print("3. 売上の時系列推移（月別）")
print("=" * 60)
monthly_sales = sales.groupby('month').agg({
    'total_amount': 'sum',
    'order_id': 'count'
}).rename(columns={'order_id': 'order_count'})
print("\n【月別売上】")
print(monthly_sales)

# 月別売上グラフ
fig, ax1 = plt.subplots(figsize=(12, 6))
months = [str(m) for m in monthly_sales.index]
ax1.bar(months, monthly_sales['total_amount'] / 10000, color='steelblue', alpha=0.7, label='Sales (10K JPY)')
ax1.set_xlabel('Month')
ax1.set_ylabel('Sales (10K JPY)', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.set_xticklabels(months, rotation=45)

ax2 = ax1.twinx()
ax2.plot(months, monthly_sales['order_count'], color='darkorange', marker='o', linewidth=2, label='Order Count')
ax2.set_ylabel('Order Count', color='darkorange')
ax2.tick_params(axis='y', labelcolor='darkorange')

plt.title('Monthly Sales and Order Count (2024)')
fig.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/01_monthly_sales.png', dpi=100)
plt.close()

print("\n" + "=" * 60)
print("4. 商品カテゴリ別・チャネル別の売上分析")
print("=" * 60)

# カテゴリ別
category_sales = sales.groupby('product_category').agg({
    'total_amount': ['sum', 'mean', 'count']
}).round(0)
category_sales.columns = ['total', 'avg', 'count']
category_sales = category_sales.sort_values('total', ascending=False)
print("\n【商品カテゴリ別売上】")
print(category_sales)

# チャネル別
channel_sales = sales.groupby('channel').agg({
    'total_amount': ['sum', 'mean', 'count']
}).round(0)
channel_sales.columns = ['total', 'avg', 'count']
channel_sales = channel_sales.sort_values('total', ascending=False)
print("\n【チャネル別売上】")
print(channel_sales)

# カテゴリ別グラフ
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].barh(category_sales.index, category_sales['total'] / 10000, color='teal')
axes[0].set_xlabel('Sales (10K JPY)')
axes[0].set_title('Sales by Product Category')

axes[1].barh(channel_sales.index, channel_sales['total'] / 10000, color='coral')
axes[1].set_xlabel('Sales (10K JPY)')
axes[1].set_title('Sales by Channel')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/02_category_channel_sales.png', dpi=100)
plt.close()

print("\n" + "=" * 60)
print("5. 顧客種別（toB/toC）の比較")
print("=" * 60)

customer_type_sales = sales.groupby('customer_type').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'quantity': 'mean'
}).round(0)
customer_type_sales.columns = ['total_sales', 'avg_sales', 'order_count', 'avg_quantity']
print("\n【顧客種別比較】")
print(customer_type_sales)

# 顧客種別×カテゴリ
cross_type_category = pd.pivot_table(
    sales, values='total_amount', index='product_category',
    columns='customer_type', aggfunc='sum'
)
print("\n【顧客種別×商品カテゴリ 売上クロス表】")
print(cross_type_category)

# 顧客種別グラフ
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 売上構成比
type_totals = customer_type_sales['total_sales']
axes[0].pie(type_totals, labels=type_totals.index, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
axes[0].set_title('Sales Share by Customer Type')

# カテゴリ別の顧客種別比較
cross_type_category.plot(kind='bar', ax=axes[1], color=['#ff9999', '#66b3ff'])
axes[1].set_xlabel('Product Category')
axes[1].set_ylabel('Sales (JPY)')
axes[1].set_title('Sales by Category and Customer Type')
axes[1].legend(title='Customer Type')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/03_customer_type_analysis.png', dpi=100)
plt.close()

print("\n" + "=" * 60)
print("6. 地域別分析")
print("=" * 60)

region_sales = sales.groupby('region').agg({
    'total_amount': ['sum', 'mean', 'count']
}).round(0)
region_sales.columns = ['total', 'avg', 'count']
region_sales = region_sales.sort_values('total', ascending=False)
print("\n【地域別売上】")
print(region_sales)

# 地域別×顧客種別
cross_region_type = pd.pivot_table(
    sales, values='total_amount', index='region',
    columns='customer_type', aggfunc='sum'
)
print("\n【地域別×顧客種別 売上クロス表】")
print(cross_region_type)

# 地域別グラフ
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(region_sales.index, region_sales['total'] / 10000, color='seagreen')
axes[0].set_xlabel('Region')
axes[0].set_ylabel('Sales (10K JPY)')
axes[0].set_title('Sales by Region')

cross_region_type.plot(kind='bar', ax=axes[1], color=['#ff9999', '#66b3ff'])
axes[1].set_xlabel('Region')
axes[1].set_ylabel('Sales (JPY)')
axes[1].set_title('Sales by Region and Customer Type')
axes[1].legend(title='Customer Type')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/04_region_analysis.png', dpi=100)
plt.close()

print("\n" + "=" * 60)
print("7. 相関分析・追加分析")
print("=" * 60)

# 数値列の相関
numeric_cols = ['quantity', 'unit_price', 'total_amount']
print("\n【数値列の相関係数】")
print(sales[numeric_cols].corr().round(3))

# 商品別売上TOP10
product_sales = sales.groupby('product_name')['total_amount'].sum().sort_values(ascending=False)
print("\n【商品別売上TOP10】")
print(product_sales.head(10))

# リピート率分析
repeat_analysis = sales[sales['is_repeat'].notna()].groupby('customer_type')['is_repeat'].mean()
print("\n【顧客種別リピート率】")
print(repeat_analysis.round(3))

# 商品TOP10グラフ
fig, ax = plt.subplots(figsize=(10, 6))
product_sales.head(10).plot(kind='barh', ax=ax, color='purple')
ax.set_xlabel('Sales (JPY)')
ax.set_title('Top 10 Products by Sales')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/05_product_top10.png', dpi=100)
plt.close()

# 月別カテゴリ売上ヒートマップ
monthly_category = pd.pivot_table(
    sales, values='total_amount', index='product_category',
    columns='month', aggfunc='sum', fill_value=0
)

fig, ax = plt.subplots(figsize=(14, 5))
im = ax.imshow(monthly_category.values / 10000, cmap='YlOrRd', aspect='auto')
ax.set_xticks(range(len(monthly_category.columns)))
ax.set_xticklabels([str(m) for m in monthly_category.columns], rotation=45)
ax.set_yticks(range(len(monthly_category.index)))
ax.set_yticklabels(monthly_category.index)
ax.set_title('Monthly Sales by Category (10K JPY)')
plt.colorbar(im, ax=ax, label='Sales (10K JPY)')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/06_monthly_category_heatmap.png', dpi=100)
plt.close()

print("\n" + "=" * 60)
print("分析完了！グラフを outputs/ に保存しました")
print("=" * 60)

# サマリー統計
print("\n【サマリー】")
print(f"総売上: {sales['total_amount'].sum():,.0f}円")
print(f"総注文数: {len(sales)}件")
print(f"平均注文単価: {sales['total_amount'].mean():,.0f}円")
print(f"ユニーク顧客数: {sales['customer_id'].nunique()}人")
print(f"最も売れたカテゴリ: {category_sales.index[0]}")
print(f"最も売れた商品: {product_sales.index[0]}")
