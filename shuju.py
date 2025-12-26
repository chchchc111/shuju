# -*- coding: utf-8 -*-
"""
销售仪表板 - 纯Python实现（Streamlit）
运行方式：终端执行 streamlit run sales_dashboard.py
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# --------------------------
# 1. 页面基础配置
# --------------------------
st.set_page_config(
    page_title="销售仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式（模拟Tailwind效果）
st.markdown("""
    <style>
    /* 筛选标签样式 */
    .filter-tag {
        background-color: #dc2626;
        color: white;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        display: inline-block;
        margin: 0 4px 4px 0;
    }
    /* 指标卡片样式 */
    .metric-card {
        font-size: 24px;
        font-weight: 600;
        color: #1f2937;
    }
    .metric-label {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 4px;
    }
    /* 星级评分 */
    .star {
        color: #facc15;
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 2. 模拟数据源
# --------------------------
# 小时销售额数据
hourly_data = pd.DataFrame({
    "小时数": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "销售额": [29925.22, 28930.79, 24824.65, 33069.74, 29360.38,
              29694.77, 24025.07, 23281.16, 24790.80, 37809.06, 21875.74]
})

# 产品类型销售额数据
product_data = pd.DataFrame({
    "产品类型": ["健康美容", "家居生活", "时尚配饰", "电子配件", "运动旅行", "食品饮料"],
    "销售额": [46851.18, 51297.06, 51719.90, 51750.03, 52497.93, 53471.28]
})

# 核心指标数据
total_sales = 307587  # 总销售额
avg_rating = 7.0      # 平均评分
avg_per_order = 307.59 # 每单平均销售额

# --------------------------
# 3. 左侧筛选侧边栏
# --------------------------
with st.sidebar:
    st.header("请筛选数据:")
    
    # 城市筛选
    st.subheader("请选择城市:")
    selected_cities = st.multiselect(
        "",
        options=["太原", "临汾", "大同"],
        default=["太原", "临汾", "大同"]
    )
    # 显示已选城市标签
    for city in selected_cities:
        st.markdown(f'<span class="filter-tag">{city} ✕</span>', unsafe_allow_html=True)
    
    # 顾客类型筛选
    st.subheader("请选择顾客类型:")
    selected_customer = st.multiselect(
        "",
        options=["会员用户", "普通用户"],
        default=["会员用户", "普通用户"]
    )
    for ctype in selected_customer:
        st.markdown(f'<span class="filter-tag">{ctype} ✕</span>', unsafe_allow_html=True)
    
    # 性别筛选
    st.subheader("请选择性别:")
    selected_gender = st.multiselect(
        "",
        options=["男性", "女性"],
        default=["男性", "女性"]
    )
    for gender in selected_gender:
        st.markdown(f'<span class="filter-tag">{gender} ✕</span>', unsafe_allow_html=True)

# --------------------------
# 4. 主内容区
# --------------------------
# 标题
st.markdown("""
    <h1 style="display: flex; align-items: center;">
        <div style="width: 24px; height: 24px; display: flex; margin-right: 8px;">
            <div style="width: 8px; height: 100%; background: #2563eb;"></div>
            <div style="width: 8px; height: 100%; background: #22c55e;"></div>
            <div style="width: 8px; height: 100%; background: #facc15;"></div>
        </div>
        销售仪表板
    </h1>
""", unsafe_allow_html=True)

# 核心指标行
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<p class="metric-label">总销售额:</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-card">RMB ¥{total_sales:,}</p>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="metric-label">顾客评分的平均值:</p>', unsafe_allow_html=True)
    # 星级评分（7星实心 + 3星空心）
    stars = "".join(['<span class="star">★</span>' for _ in range(7)]) + \
            "".join(['<span class="star" style="color:#e5e7eb">★</span>' for _ in range(3)])
    st.markdown(f'<div style="display: flex; align-items: center;">'
                f'<span class="metric-card mr-2">7.0</span>{stars}</div>', 
                unsafe_allow_html=True)

with col3:
    st.markdown('<p class="metric-label">每单的平均销售额:</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-card">RMB ¥{avg_per_order:.2f}</p>', unsafe_allow_html=True)

st.divider()

# 图表区域
chart_col1, chart_col2 = st.columns(2)

# 按小时销售额图表
with chart_col1:
    st.subheader("按小时数划分的销售额")
    fig_hourly = px.bar(
        hourly_data,
        x="小时数",
        y="销售额",
        color_discrete_sequence=["#0056b3"],
        height=400
    )
    # 优化图表样式
    fig_hourly.update_layout(
        xaxis_title="小时数",
        yaxis_title="销售额",
        yaxis_tickformat=",.0f",
        yaxis=dict(
            tickvals=[0, 10000, 20000, 30000, 40000],
            ticktext=["0", "1万", "2万", "3万", "4万"]
        ),
        showlegend=False,
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

# 按产品类型销售额图表
with chart_col2:
    st.subheader("按产品类型划分的销售额")
    fig_product = px.bar(
        product_data,
        y="产品类型",
        x="销售额",
        color_discrete_sequence=["#0056b3"],
        orientation="h",
        height=400
    )
    # 优化图表样式
    fig_product.update_layout(
        xaxis_title="销售额",
        yaxis_title="产品类型",
        xaxis_tickformat=",.0f",
        xaxis=dict(
            tickvals=[0, 10000, 20000, 30000, 40000, 50000],
            ticktext=["0", "1万", "2万", "3万", "4万", "5万"]
        ),
        showlegend=False,
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_product, use_container_width=True)
