from tkinter.tix import Tree
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px

cur_dir='./csv_data2020'
wage_per_one = '一人当たり賃金（万円）'
all_wage_per_one = '全国_一人当たり賃金（万円）'

syotei='所定内給与額（万円）'
syouyo='年間賞与その他特別給与額（万円）'
wage_list = [wage_per_one, syotei, syouyo]
def show_industry_wage(df_jp_category_broad):
    st.header('産業別の平均賃金（万円）')

    year_list = df_jp_category_broad['集計年'].unique()
    option_year = st.selectbox(
        '集計年',
        (year_list)
    )

    option_wage = st.selectbox(
        '賃金の種類',
        (wage_list),
        key='wage'
    )
    df_mean_catg = df_jp_category_broad[df_jp_category_broad['集計年'] == option_year]
    #df_mean_catg 
    max = df_mean_catg[option_wage].max() + 50

    fig = px.bar(
        df_mean_catg,
        x = option_wage,
        y = '産業大分類名',
        color =  '産業大分類名',
        animation_frame = '年齢',
        range_x = [0,max],
        orientation='h',
        width=800,
        height=500)

    st.plotly_chart(fig)

#産業別業種別
def show_mid_industry_wage(df_jp_category_mid, df_jp_ind_mid):
    year_list = df_jp_category_mid['集計年'].unique()
    st.header('大産業別中産業別の平均賃金（万円）')
    option_wage2 = st.selectbox(
        '賃金の種類',
        (wage_list),
        key='wage2'

    )
    l = df_jp_category_mid['産業大分類名'].unique()
    option_mid_catg = st.selectbox(
        '大分類',
        (l),
        key='broad_list'
    )
    #l2 = df_jp_category_mid[df_jp_category_mid['産業大分類名'] ==option_mid_catg]['業種中分類名'].unique()
    option_year2 = st.selectbox(
        '集計年',
        (year_list),
        key='year'
    )

    df_mean_catg = df_jp_ind_mid[df_jp_ind_mid['集計年'] == option_year2]
    df_mean_catg = df_mean_catg[df_mean_catg['産業大分類名'] == option_mid_catg]
    df_mean_catg = df_mean_catg[df_mean_catg['一人当たり賃金（万円）'] != '-']
    df_mean_catg[option_wage2] = df_mean_catg[option_wage2].astype(float)
    #df_mean_catg
    max = df_mean_catg[option_wage2].max() + 50
    fig = px.bar(
        df_mean_catg,
        x = option_wage2,
        y = '業種中分類名',
        color =  '業種中分類名',
        animation_frame = '年齢',
        range_x = [0,max],
        orientation='h',#horizonal bar
        width=1000,
        height=800)

    st.plotly_chart(fig)