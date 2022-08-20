import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px

cur_dir='./csv_data2020'
wage_per_one = '一人当たり賃金（万円）'
all_wage_per_one = '全国_一人当たり賃金（万円）'
def show_heatmap(df_pref_ind):

    st.header('2020年:一人当たり平均賃金のヒートマップ')
    jp_lat_lon = pd.read_csv(cur_dir+'/pref_lat_lon.csv')
    jp_lat_lon = jp_lat_lon.rename(columns={'pref_name' : '都道府県名'})
    df_pref_map = df_pref_ind[(df_pref_ind['年齢'] == '年齢計') & (df_pref_ind['集計年'] == 2019)]
    df_pref_map = pd.merge(df_pref_map,jp_lat_lon,on='都道府県名')
    tmp = df_pref_map[wage_per_one]
    df_pref_map["weight"] = (tmp - tmp.min()) / (tmp.max() - tmp.min())
    HeatmapData = df_pref_map[['lat', 'lon', 'weight']]
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

    show_df = st.checkbox('Show DataFrame')
    if show_df == True:
        st.write(df_pref_map)