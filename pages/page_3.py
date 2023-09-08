import streamlit as st
import json

# JSONファイルを読み込む関数
def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Streamlitアプリを作成
st.title("JSONファイルの表示")

# 1つ目のJSONファイルを読み込む
json_file1 = st.file_uploader("1つ目のJSONファイルをアップロードしてください", type=["json"])
if json_file1 is not None:
    data1 = load_json_file(json_file1)
    st.write("1つ目のJSONデータ:")
    st.write(data1)

# 2つ目のJSONファイルを読み込む
json_file2 = st.file_uploader("2つ目のJSONファイルをアップロードしてください", type=["json"])
if json_file2 is not None:
    data2 = load_json_file(json_file2)
    st.write("2つ目のJSONデータ:")
    st.write(data2)
