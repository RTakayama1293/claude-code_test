"""
商品別ワードクラウド分析
- カテゴリ別に色分け
- ①販売回数ベース ②総販売額ベース
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from wordcloud import WordCloud
import numpy as np

# 日本語フォント設定
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
plt.rcParams['font.family'] = ['Noto Sans CJK JP', 'sans-serif']

OUTPUT_DIR = '/home/user/claude-code_test/experiments/exp001_baseline/outputs'

# データ読み込み
sales = pd.read_csv('/home/user/claude-code_test/data/raw/sales.csv')

# カテゴリ別の色を定義
CATEGORY_COLORS = {
    '水産物': '#1f77b4',   # 青
    '畜産物': '#d62728',   # 赤
    '農産物': '#2ca02c',   # 緑
    '酒類': '#9467bd',     # 紫
}

# 商品別集計
product_stats = sales.groupby(['product_name', 'product_category']).agg({
    'order_id': 'count',        # 販売回数
    'total_amount': 'sum'       # 総販売額
}).reset_index()
product_stats.columns = ['product_name', 'category', 'count', 'total_sales']

# 商品→カテゴリのマッピング
product_to_category = dict(zip(product_stats['product_name'], product_stats['category']))

# カラー関数（カテゴリに基づいて色を返す）
def color_func_factory(product_to_category, category_colors):
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        category = product_to_category.get(word, '酒類')
        return category_colors.get(category, '#333333')
    return color_func

color_func = color_func_factory(product_to_category, CATEGORY_COLORS)

# ① 販売回数ベースのワードクラウド用データ
count_freq = dict(zip(product_stats['product_name'], product_stats['count']))

# ② 総販売額ベースのワードクラウド用データ（スケーリング）
sales_freq = dict(zip(product_stats['product_name'], product_stats['total_sales'] / 1000))

# ワードクラウド生成
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# ① 販売回数ベース
wc_count = WordCloud(
    font_path=FONT_PATH,
    width=800,
    height=600,
    background_color='white',
    color_func=color_func,
    prefer_horizontal=0.7,
    min_font_size=12,
    max_font_size=120,
    relative_scaling=0.5
).generate_from_frequencies(count_freq)

axes[0].imshow(wc_count, interpolation='bilinear')
axes[0].set_title('商品別ワードクラウド（販売回数ベース）', fontsize=14, fontweight='bold')
axes[0].axis('off')

# ② 総販売額ベース
wc_sales = WordCloud(
    font_path=FONT_PATH,
    width=800,
    height=600,
    background_color='white',
    color_func=color_func,
    prefer_horizontal=0.7,
    min_font_size=12,
    max_font_size=120,
    relative_scaling=0.5
).generate_from_frequencies(sales_freq)

axes[1].imshow(wc_sales, interpolation='bilinear')
axes[1].set_title('商品別ワードクラウド（総販売額ベース）', fontsize=14, fontweight='bold')
axes[1].axis('off')

# 凡例を追加
legend_elements = [plt.Line2D([0], [0], marker='s', color='w',
                              markerfacecolor=color, markersize=15, label=cat)
                   for cat, color in CATEGORY_COLORS.items()]
fig.legend(handles=legend_elements, loc='lower center', ncol=4,
           fontsize=12, frameon=True, title='商品カテゴリ')

plt.tight_layout()
plt.subplots_adjust(bottom=0.12)
plt.savefig(f'{OUTPUT_DIR}/07_wordcloud_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

print("ワードクラウド生成完了！")
print(f"出力: {OUTPUT_DIR}/07_wordcloud_comparison.png")

# 商品別統計を表示
print("\n【商品別統計】")
print(product_stats.sort_values('total_sales', ascending=False).to_string(index=False))
