import streamlit as st
import plotly.graph_objs as go
import pandas as pd

st.set_page_config(layout="wide")

# 配色、流量渠道
colors = {
    'Direct': '#0085ff', 'Referral': '#8bc34a', 'Organic Search': '#ff4a4a',
    'Paid Search': '#673ab7', 'Organic Social': '#ff80b0', 'Paid Social': '#a574ff',
    'Email': '#00c0ff', 'Display Ads': '#ff66ff'
}
channels = list(colors.keys())
months = ['Oct 24','Nov 24','Dec 24','Jan 25','Feb 25','Mar 25']

# 示例数据（可替换）
DATA = {
    'ShangYnag': {
        'Direct':[190000,180000,160000,180000,150000,185000],
        'Referral':[40000,30000,35000,40000,38000,50000],
        'Organic Search':[220000,175000,180000,205000,170000,185000],
        'Paid Search':[15000,12000,14000,18000,17000,20000],
        'Organic Social':[9000,7000,8000,10000,9000,12000],
        'Paid Social':[400,300,400,500,400,800],
        'Email':[3500,3000,3500,3500,3000,4200],
        'Display Ads':[500,400,400,400,400,400]
    },
    'GreenBrush': {
        'Direct':[1800,2500,2200,2600,1900,1200],
        'Referral':[700,600,800,900,750,900],
        'Organic Search':[3000,4500,4800,6000,4000,3500],
        'Paid Search':[200,300,250,280,230,260],
        'Organic Social':[0,0,0,0,0,0],'Paid Social':[0,0,0,0,0,0],
        'Email':[0,0,0,0,0,0],'Display Ads':[0,0,0,0,0,0]
    },
    'TaikiUSA': {
        'Direct':[20000,0,0,0,0,0],'Referral':[1000,0,0,0,0,0],
        'Organic Search':[5000,0,0,0,0,0],'Paid Search':[300,0,0,0,0,0],
        'Organic Social':[0,0,0,0,0,0],'Paid Social':[0,0,0,0,0,0],
        'Email':[0,0,0,0,0,0],'Display Ads':[0,0,0,0,0,0]
    }
}
SHARE = {
    'ShangYnag':{
        'total':'2.7M','period':'Oct 2024 – Mar 2025',
        'Direct':38.63,'Referral':10.22,'Organic Search':42.04,'Paid Search':3.32,
        'Organic Social':4.8,'Paid Social':0.1,'Email':0.76,'Display Ads':0.11
    },
    'GreenBrush':{
        'total':'36.7K','period':'Oct 2024 – Mar 2025',
        'Direct':18.29,'Referral':4.7,'Organic Search':73.65,'Paid Search':2.47,
        'Organic Social':0,'Paid Social':0,'Email':0,'Display Ads':0
    },
    'TaikiUSA':{
        'total':'24.9K','period':'Oct 2024 – Mar 2025',
        'Direct':78.63,'Referral':3.9,'Organic Search':16.87,'Paid Search':1.15,
        'Organic Social':0,'Paid Social':0,'Email':0,'Display Ads':0.45
    }
}
GEO = {
    'ShangYnag': [
        ['United States','98.58%','7.9K','0%','100%'],
        ['Peru','0.77%','62','100%','0%'],
        ['Romania','0.6%','48','100%','0%'],
        ['India','0.02%','2','100%','0%'],
        ['Mexico','0.02%','2','100%','0%']
    ],
    'GreenBrush': [
        ['China','17.33%','878','100%','0%'],
        ['Malaysia','10.33%','523','9.26%','90.74%'],
        ['United States','9.81%','497','100%','0%'],
        ['Poland','6.93%','351','100%','0%'],
        ['Israel','5.55%','281','100%','0%']
    ],
    'TaikiUSA': [
        ['United States','26.89%','444','100%','0%'],
        ['Brazil','18.9%','312','100%','0%'],
        ['Malaysia','18.17%','300','100%','0%'],
        ['Paraguay','7.63%','126','100%','0%'],
        ['Egypt','5.88%','97','100%','0%']
    ]
}

site_map = {
    "ShangYnag (sy-beauty.com)":'ShangYnag',
    "GreenBrush (greenbrushes.com)":'GreenBrush',
    "TaikiUSA (taikibeauty.com)":'TaikiUSA'
}

# ============ 页面主逻辑 ============

# 选择网站
site_label = st.sidebar.selectbox("选择竞对网站", list(site_map.keys()))
site = site_map[site_label]

# ======= 左侧图表区 =======
st.subheader(f"流量渠道趋势（{site_label}）")
fig = go.Figure()
for ch in channels:
    fig.add_trace(go.Scatter(
        x=months, y=DATA[site][ch], mode='lines+markers',
        name=ch, line=dict(color=colors[ch], width=2), marker=dict(size=7)
    ))
fig.update_layout(
    xaxis=dict(title='',tickmode='linear'),
    yaxis=dict(title='',rangemode='tozero',tickformat=','),
    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
    margin=dict(l=20,r=20,t=10,b=20),
    height=420,
)
fig.update_xaxes(fixedrange=False)
fig.update_yaxes(fixedrange=False)
st.plotly_chart(fig, use_container_width=True)

# ======= 下载按钮 =======
st.download_button(
    label="导出PNG图片",
    data=fig.to_image(format="png"),
    file_name=f"{site}_traffic_trend.png",
    mime="image/png"
)

# ======= 右侧信息栏 =======
col1, col2 = st.columns([2,1])
with col2:
    st.markdown(f"### {SHARE[site]['total']}")
    st.markdown(f"<span style='color: #888;'>{SHARE[site]['period']}</span>",unsafe_allow_html=True)
    # 百分比彩条
    bar_html = "<div style='display:flex;height:13px;border-radius:3px;overflow:hidden;margin-bottom:12px;'>"
    for ch in channels:
        width = max(SHARE[site][ch], 0.5)  # 最小0.5%，避免0宽看不见
        bar_html += f"<div style='width:{width}%;background:{colors[ch]}' title='{ch}'></div>"
    bar_html += "</div>"
    st.markdown(bar_html, unsafe_allow_html=True)
    # 渠道占比
    for ch in channels:
        st.markdown(f"<div style='display:flex;align-items:center;font-size:13px;margin-bottom:4px;'>"
                    f"<div style='width:12px;height:12px;background:{colors[ch]};margin-right:7px;border-radius:2px;'></div>"
                    f"<span style='flex:1'>{ch}</span><strong>{SHARE[site][ch]}%</strong></div>", unsafe_allow_html=True)

    # ======= 地域分布 =======
    st.markdown("#### Geo Distribution")
    geo_df = pd.DataFrame(GEO[site], columns=['Country','占比','Visits','Desktop','Mobile'])
    st.dataframe(geo_df, use_container_width=True, hide_index=True)

with col1:
    st.info("提示：可以鼠标拖动、滚轮缩放区间，查看细节；点击右上角 'Download plot as png' 也可以直接导出。")

