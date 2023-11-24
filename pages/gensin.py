import streamlit as st
import json
from datetime import datetime
import pytz
import urllib.parse
import pandas as pd

# 禁止ワードをExcelファイルから読み込む
df = pd.read_excel("banned_list.xlsx", sheet_name=0)
#禁止ワードをbanned_words に
banned_words = df['禁止ワード'].tolist()
banned_words = [str(word) for word in banned_words]

# ユーザーの投稿内容をチェックする関数
def check_post_content(content):
    # タイトルと投稿内容の禁止ワードの検出
    for banned_word in banned_words:
        if banned_word in content:
            content = content.replace(banned_word, "＠" * len(banned_word))
    return content


