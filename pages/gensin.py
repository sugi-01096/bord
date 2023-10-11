import streamlit as st
import json
from datetime import datetime
import pytz
import urllib.parse

# 禁止ワードのリストをファイルから読み込む
def load_banned_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# toxic.txtから禁止ワードリストを読み込む
banned_words = load_banned_words("toxic.txt")

# ユーザーの投稿内容をチェックする関数
def check_post_content(content):
    # タイトルと投稿内容の禁止ワードの検出
    for banned_word in banned_words:
        if banned_word in content:
            content = content.replace(banned_word, "＠" * len(banned_word))
    return content

# 以降のコードは変更なし
