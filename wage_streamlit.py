from tkinter.tix import Tree
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px
import show_heatmap as sh
import show_wage_a_year as sw
import show_ave_wage as sa
import show_industry as si

st.title('日本の賃金データのダッシュボード')
cur_dir='./csv_data2020'
wage_per_one = '一人当たり賃金（万円）'
all_wage_per_one = '全国_一人当たり賃金（万円）'
#read csv
df_jp_ind = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_全国_全産業.csv', encoding='shift-jis')
df_jp_category_broad = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_全国_大分類.csv', encoding='shift-jis')
df_pref_ind = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_都道府県_全産業.csv', encoding='shift-jis')
df_jp_ind_mid = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_全国_中分類.csv', encoding='shift-jis')
df_jp_category_mid = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_都道府県_中分類.csv', encoding='shift-jis')
df_pref_ind_broad = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_都道府県_大分類.csv', encoding='shift-jis')

with st.sidebar:
    #Show Heatmap
    show_heatmap_button = st.button('2020年：平均賃金ヒートマップ')
    show_wage_a_year = st.button('集計年別の一人当たり賃金の推移')
    show_all_pre_average = st.button('年齢階級別の全国一人当たり平均賃金（万円）')
    show_industry_wage = st.button('産業別の平均賃金（万円）')
    show_mid_industry_wage = st.button('大産業別中産業別の平均賃金（万円）')

if show_heatmap_button == True:
    sh.show_heatmap(df_pref_ind)
if show_wage_a_year == Tree:
    sw.show_wage_a_year(df_jp_ind, df_pref_ind)
if show_all_pre_average == True:
    sa.show_all_pre_average(df_jp_ind)
if show_industry_wage == True:
    si.show_industry_wage(df_jp_category_broad)
if show_mid_industry_wage == True:
    si.show_mid_industry_wage(df_jp_category_mid, df_jp_ind_mid)  

st.text('出典：RESAS（地域経済分析システム）')
st.text('本結果はRESAS（地域経済分析システム）を加工して作成')
