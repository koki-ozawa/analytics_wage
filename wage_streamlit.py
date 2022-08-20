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
syotei='所定内給与額（万円）'
syouyo='年間賞与その他特別給与額（万円）'
wage_list = [wage_per_one, syotei, syouyo]
#read csv
df_jp_ind = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_全国_全産業.csv', encoding='shift-jis')
df_jp_category_broad = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_全国_大分類.csv', encoding='shift-jis')
df_pref_ind = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_都道府県_全産業.csv', encoding='shift-jis')
df_jp_ind_mid = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_全国_中分類.csv', encoding='shift-jis')
df_jp_category_mid = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_都道府県_中分類.csv', encoding='shift-jis')
df_pref_ind_broad = pd.read_csv('./csv_data2020/雇用_医療福祉_一人当たり賃金_都道府県_大分類.csv', encoding='shift-jis')

select_list = ['2020年：平均賃金ヒートマップ',
                           '集計年別の一人当たり賃金の推移',
                           '年齢階級別の全国一人当たり平均賃金（万円）',
                            '産業別の平均賃金（万円）',
                            '大産業別中産業別の平均賃金（万円）']
show_heatmap_button = False
show_wage_a_year = False
show_all_pre_average = False
show_industry_wage = False 
show_mid_industry_wage = False
with st.sidebar:
    option = st.selectbox('表示したい統計を選んでください',select_list)

    if option == select_list[0]:
        show_heatmap_button = True
    if option == select_list[1]:
        show_wage_a_year = True
        df_pref_mean = df_pref_ind[df_pref_ind['年齢'] == '年齢計']
        #df_pref_mean
        pref_list = df_pref_mean['都道府県名'].unique()
        options = st.multiselect(
            'Check prefecture name you want to compare',
            pref_list,
            default='東京都',
        )
    if option == select_list[2]:
        show_all_pre_average = True
    if option == select_list[3]:
        show_industry_wage = True 
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
    if option == select_list[4]:
        show_mid_industry_wage = True
        year_list = df_jp_category_mid['集計年'].unique()
        option_wage2 = st.selectbox(
            '賃金の種類',(wage_list),key='wage2'
        )
        l = df_jp_category_mid['産業大分類名'].unique()
        option_mid_catg = st.selectbox(
            '大分類',(l),key='broad_list'
        )
        option_year2 = st.selectbox(
            '集計年',(year_list),key='year'
        )

if show_heatmap_button == True:
    sh.show_heatmap(df_pref_ind)
if show_wage_a_year == True:
    sw.show_wage_a_year(df_jp_ind, df_pref_mean, options)
if show_all_pre_average == True:
    sa.show_all_pre_average(df_jp_ind)
if show_industry_wage == True:
    si.show_industry_wage(df_jp_category_broad, option_year, option_wage)
if show_mid_industry_wage == True:
    si.show_mid_industry_wage(df_jp_ind_mid, option_wage2, option_mid_catg ,option_year2 )  

st.text('出典：RESAS（地域経済分析システム）')
st.text('本結果はRESAS（地域経済分析システム）を加工して作成')
