import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px

def show_heatmap():

    view = pdk.ViewState(
        longitude=139.691648,
        latitude=35.689185,
        zoom=4,
        pitch=40.5
    )

    layer = pdk.Layer(
        "HeatmapLayer",
        data=HeatmapData,
        opacity=0.4,
        get_position=["lon", "lat"],
        threshold=0.1,
        get_weight= "weight",
        pickable=True
    )

    layer_map = pdk.Deck(
        layers = layer,
        initial_view_state=view
    )

    st.pydeck_chart(layer_map)

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

st.header('2020年:一人当たり平均賃金のヒートマップ')

jp_lat_lon = pd.read_csv(cur_dir+'/pref_lat_lon.csv')
jp_lat_lon = jp_lat_lon.rename(columns={'pref_name' : '都道府県名'})

df_pref_map = df_pref_ind[(df_pref_ind['年齢'] == '年齢計') & (df_pref_ind['集計年'] == 2019)]
df_pref_map = pd.merge(df_pref_map,jp_lat_lon,on='都道府県名')
tmp = df_pref_map[wage_per_one]
df_pref_map["weight"] = (tmp - tmp.min()) / (tmp.max() - tmp.min())
HeatmapData = df_pref_map[['lat', 'lon', 'weight']]

show_heatmap = st.checkbox('Show Heatmap')
if show_heatmap == True:
    show_heatmap()

show_df = st.checkbox('Show DataFrame')
if show_df == True:
    st.write(df_pref_map)

st.header('集計年別の一人当たり賃金の推移')
df_mean = df_jp_ind[df_jp_ind['年齢'] == '年齢計']
df_mean = df_mean.rename(columns={wage_per_one: all_wage_per_one })
#df_mean

df_pref_mean = df_pref_ind[df_pref_ind['年齢'] == '年齢計']
#df_pref_mean
pref_list = df_pref_mean['都道府県名'].unique()

'''option = st.selectbox(
    '都道府県名',
    (pref_list)
)'''
options = st.multiselect(
    'Check prefecture name you want to compare',
    pref_list,
    default='東京都',
)
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

st.header('産業別の平均賃金（万円）')

year_list = df_jp_category_broad['集計年'].unique()
option_year = st.selectbox(
    '集計年',
    (year_list)
)
syotei='所定内給与額（万円）'
syouyo='年間賞与その他特別給与額（万円）'
wage_list = ['一人当たり賃金（万円）',  '所定内給与額（万円）', '年間賞与その他特別給与額（万円）']
wage_list = [wage_per_one, syotei, syouyo]

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

st.text('出典：RESAS（地域経済分析システム）')
st.text('本結果はRESAS（地域経済分析システム）を加工して作成')
