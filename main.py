import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from utils import PLANETS, get_planet_data, format_hover_text

# 設置頁面配置
st.set_page_config(
    page_title="行星軌跡視覺化",
    page_icon="🌍",
    layout="wide"
)

# 標題
st.title("太陽系行星軌跡視覺化")

# 側邊欄配置
st.sidebar.header("設定")

# 日期選擇
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "開始日期",
        datetime.now(),
        key="start_date"
    )
with col2:
    end_date = st.date_input(
        "結束日期",
        datetime.now() + timedelta(days=180),
        key="end_date"
    )

# 行星選擇
selected_planets = st.sidebar.multiselect(
    "選擇要顯示的行星",
    list(PLANETS.keys()),
    default=['水星', '金星', '火星']
)

# 顯示設定
show_labels = st.sidebar.checkbox("顯示行星標籤", value=True)
show_trajectory = st.sidebar.checkbox("顯示軌跡", value=True)

if start_date >= end_date:
    st.error("結束日期必須在開始日期之後")
else:
    # 建立圖表
    fig = go.Figure()

    # 使用 st.cache 來快取行星資料
    @st.cache_data(ttl=3600)
    def get_cached_planet_data(planet_id, start_date, end_date):
        return get_planet_data(planet_id, start_date.strftime('%Y-%m-%d'), 
                             end_date.strftime('%Y-%m-%d'))

    # 加入太陽
    fig.add_trace(go.Scatter(
        x=[0],
        y=[0],
        mode='markers',
        name='太陽',
        marker=dict(
            size=20,
            color='yellow',
            line=dict(color='orange', width=2)
        ),
        hoverinfo='name'
    ))

    # 繪製每個選定行星的軌跡
    for planet_name in selected_planets:
        planet_id = PLANETS[planet_name]
        eph = get_cached_planet_data(planet_id, start_date, end_date)
        
        if eph is not None:
            hover_text = [format_hover_text(row) for row in eph]
            
            # 添加行星軌跡
            fig.add_trace(go.Scatter(
                x=eph['RA'],
                y=eph['DEC'],
                mode='lines+markers' if show_trajectory else 'markers',
                name=planet_name,
                text=hover_text,
                hoverinfo='name+text',
                marker=dict(size=8),
                line=dict(width=2)
            ))

    # 更新圖表布局
    fig.update_layout(
        title=dict(
            text=f'行星在天球上的軌跡 ({start_date} 至 {end_date})',
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='赤經 (度)',
        yaxis_title='赤緯 (度)',
        hovermode='closest',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        plot_bgcolor='rgb(250,250,250)'
    )

    # 調整座標軸
    fig.update_xaxes(gridcolor='rgb(230,230,230)', zeroline=True, zerolinecolor='rgb(200,200,200)')
    fig.update_yaxes(gridcolor='rgb(230,230,230)', zeroline=True, zerolinecolor='rgb(200,200,200)')

    # 顯示圖表
    st.plotly_chart(fig, use_container_width=True)

    # 添加說明文字
    st.markdown("""
    ### 使用說明
    - 在側邊欄選擇日期範圍和要顯示的行星
    - 將滑鼠移到軌跡上可以查看詳細資訊
    - 可以拖曳和縮放圖表來查看細節
    - 點擊圖例可以隱藏/顯示特定行星的軌跡
    """)

    # 資料來源說明
    st.markdown("""
    ---
    資料來源: NASA JPL Horizons 系統
    """)
