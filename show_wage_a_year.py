from tkinter.tix import Tree
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px

cur_dir='./csv_data2020'
wage_per_one = '一人当たり賃金（万円）'
all_wage_per_one = '全国_一人当たり賃金（万円）'

def show_wage_a_year(df_jp_ind,df_pref_mean, options):

    st.header('集計年別の一人当たり賃金の推移')
    df_mean = df_jp_ind[df_jp_ind['年齢'] == '年齢計']
    df_mean = df_mean.rename(columns={wage_per_one: all_wage_per_one })
    #df_mean

    #選択した都道府県のデータを抽出
    colname=[]
    for i,op in enumerate(options):
        colname.append(op)
        #op
        if i == 0:
            df_pref_options = df_pref_mean[df_pref_mean['都道府県名'] == op]
            df_pref_options.rename(columns={ '一人当たり賃金（万円）':op}, inplace=True)
            df_pref_options.set_index('集計年', inplace=True)
            continue
        #df_pref_options[op] = 
        tmp = df_pref_mean[df_pref_mean['都道府県名'] == op]
        tmp = tmp[['集計年',wage_per_one]]
        tmp.rename(columns={ '一人当たり賃金（万円）':op}, inplace=True)
        tmp.set_index('集計年', inplace=True)
        df_pref_options[op] = tmp[op]
    #df_pref_options 
    df_mean_line = pd.merge(df_mean, df_pref_options, on='集計年')
    select_column = ['集計年', '全国_一人当たり賃金（万円）'] + colname
    #df_mean_line = df_mean_line[['集計年', '全国_一人当たり賃金（万円）', '一人当たり賃金（万円）']]
    df_mean_line = df_mean_line[select_column]
    df_mean_line = df_mean_line.set_index('集計年')
    #df_mean_line
    st.line_chart(df_mean_line)
    show_df = st.checkbox('Show above DataFrame')
    if show_df == True:
        st.write(df_mean_line)