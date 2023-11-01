import streamlit as st
import json
import pandas as pd
from datetime import datetime
import pytz
import urllib.parse

# 禁止ワードをExcelファイルから読み込む
df = pd.read_excel("banned_list.xlsx", sheet_name=0)
#禁止ワードをbanned_words に
banned_words = df['禁止ワード'].tolist()
banned_words = [str(word) for word in banned_words]

banned_words = load_banned_words()

# ユーザーの投稿内容をチェックする関数
def check_post_content(title, content):
    # タイトルと投稿内容の禁止ワードの検出
    for banned_word in banned_words:
        if banned_word in title or banned_word in content:
            st.warning("禁止ワードが含まれています！")
            return None, None
    return title, content

# 以下のコードは変更なし
def save_post(title, content):
    now = datetime.now(pytz.timezone("Japan"))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    post = {"title": title, "content": content, "timestamp": now_str}
    with open('posts.json', 'a') as file:
        file.write(json.dumps(post))
        file.write('\n')

def load_posts():
    with open('posts.json', 'r') as file:
        lines = file.readlines()
        posts = [json.loads(line.strip()) for line in lines]

        # タイムスタンプを日本時間に変換
        for post in posts:
            timestamp = datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S")
            timestamp = pytz.timezone("Japan").localize(timestamp)
            post['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return posts

def main():
    st.title("掲示板アプリ")

    # 新規投稿の入力
    new_post_title = st.text_input("ページ")
    new_post_content = st.text_area("管理者以外記述厳禁", height=100)

    # 投稿ボタンが押された場合
    if st.button("投稿する") and new_post_title and new_post_content:
        new_post_title, new_post_content = check_post_content(new_post_title, new_post_content)
        if new_post_title is not None:
            save_post(new_post_title, new_post_content)
            st.success("投稿が保存されました！")

    # 保存された投稿の表示
    posts = load_posts()
    st.subheader("保存された投稿")

    if not posts:
        st.info("まだ投稿がありません。")
    else:
        for post in posts:
            # 各タイトルにリンクを付けて表示
            post_url = f"<a href='https://maichan-bord-{urllib.parse.quote(post['title'])}.streamlit.app'>{post['title']}</a>"
            st.subheader(post['content'])
            st.write(post['timestamp'])  # タイムスタンプ
            st.markdown(post_url, unsafe_allow_html=True)
            st.markdown("---")

if __name__ == "__main__":
    main()
