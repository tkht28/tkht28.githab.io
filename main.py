import streamlit as st
import pandas as pd
import pydeck as pdk

# CSVファイルのアップロード
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # CSVファイルをDataFrameに読み込む
    df = pd.read_csv(uploaded_file)

    # データの一部を表示（確認用）
    st.write("データの確認:", df.head())

    # PyDeckを使用して地図を描画
    st.pydeck_chart(pdk.Deck(
        map_style=None, # 地図のスタイルを設定します
        initial_view_state=pdk.ViewState(
            latitude=38.5, # 地図の中心
            longitude=137.0,
            zoom=4, # 値が大きいほどズームインされ、小さいほどズームアウト
            pitch=20, # カメラの傾き角度
        ), # 初期のview設定
        layers=[
            pdk.Layer(
                'ColumnLayer',
                data=df,
                get_position=['lon', 'lat'],  # 緯度・経度のカラム
                get_elevation='sales',  # 高さのカラム
                elevation_scale=100, # 円の高さ。salesの●倍
                radius=1000, # 円の半径.10000m
                get_fill_color=[180, 0, 200, 140], # 円柱の色をRGBA形式で指定 最後は透明度
                pickable=True, # Trueにすると、円柱をクリックしたときにその情報を取得
                extruded=True, # Trueの場合、円柱が3Dとして描画
            ),
        ],
        tooltip={
            "html": "<b>顧客名:</b> {client_name} <br/>"
                    # "<b>住所:</b> {adress} <br/>"
                    "<b>売上:</b> {sales}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    ))
