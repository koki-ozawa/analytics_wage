import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px

cur_dir='./csv_data2020'
wage_per_one = '一人当たり賃金（万円）'
all_wage_per_one = '全国_一人当たり賃金（万円）'

def show_all_pre_average(df_jp_ind):
    st.header('年齢階級別の全国一人当たり平均賃金（万円）')

    df_mean_bubble = df_jp_ind[df_jp_ind['年齢'] != '年齢計']

    fig = px.scatter(
        df_mean_bubble,
        x='一人当たり賃金（万円）',
        y='年間賞与その他特別給与額（万円）',
        range_x = [150, 700],
        range_y = [0, 150],
        size = '所定内給与額（万円）',
        size_max = 38,
        color = '年齢',
        animation_frame = '集計年',
        animation_group='年齢'
    )

    st.plotly_chart(fig)