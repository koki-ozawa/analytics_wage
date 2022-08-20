import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px

cur_dir='./csv_data2020'
wage_per_one = '一人当たり賃金（万円）'
all_wage_per_one = '全国_一人当たり賃金（万円）'

def show_industry_wage(df_jp_category_broad, option_year, option_wage):
    st.header('産業別の平均賃金（万円）')

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
def show_mid_industry_wage(df_jp_ind_mid, option_wage, option_mid_catg,option_year ):
    st.header('大産業別中産業別の平均賃金（万円）')

    df_mean_catg = df_jp_ind_mid[df_jp_ind_mid['集計年'] == option_year]
    df_mean_catg = df_mean_catg[df_mean_catg['産業大分類名'] == option_mid_catg]
    df_mean_catg = df_mean_catg[df_mean_catg['一人当たり賃金（万円）'] != '-']
    df_mean_catg[option_wage] = df_mean_catg[option_wage].astype(float)
    #df_mean_catg
    max = df_mean_catg[option_wage].max() + 50
    fig = px.bar(
        df_mean_catg,
        x = option_wage,
        y = '業種中分類名',
        color =  '業種中分類名',
        animation_frame = '年齢',
        range_x = [0,max],
        orientation='h',#horizonal bar
        width=800,
        height=800)

    st.plotly_chart(fig)