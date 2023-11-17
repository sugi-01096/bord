import streamlit as st
import json
from datetime import datetime
import pytz
import urllib.parse
import pandas as pd


# ユーザーの投稿内容をチェックする関数
def check_post_content(content):
    # タイトルと投稿内容の禁止ワードの検出
    

def save_post(content, image):
    now = datetime.now(pytz.timezone("Asia/Tokyo"))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    post = {"content": content, "timestamp": now_str, "image": image}
    with open('posts1.json', 'a') as file:
        file.write(json.dumps(post))
        file.write('\n')

def load_posts():
    with open('posts1.json', 'r') as file:
        lines = file.readlines()
        posts = [json.loads(line.strip()) for line in lines]
        
        # タイムスタンプを日本時間に変換
        for post in posts:
            timestamp = datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S")
            timestamp = pytz.timezone("Asia/Tokyo").localize(timestamp)
            post['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return posts

def main():
    st.title("雑談１")

    # 新規投稿の入力
    new_post_content = st.text_area("投稿", height=100)

    # 画像のアップロード
    uploaded_image = st.file_uploader("画像をアップロード", type=["jpg", "jpeg", "png"])

    # 投稿ボタンが押された場合
    if st.button("投稿する") and new_post_content:
        new_post_content = check_post_content(new_post_content)
        if "＠" in new_post_content:
            st.warning("禁止ワードが含まれています！")

        # 画像がアップロードされた場合、バイナリデータとして保存
        image_data = None
        if uploaded_image is not None:
            image_data = uploaded_image.read()

        save_post(new_post_content, image_data)
        st.success("投稿が保存されました！")

    # 保存された投稿の表示
    posts = load_posts()
    st.subheader("保存された投稿")

    if not posts:
        st.info("まだ投稿がありません。")
    else:
        for post in posts:
            st.subheader(post['content'])
            st.image(post['image']) if 'image' in post else None
            st.write(post['timestamp'])  # タイムスタンプを表示
            st.markdown("---")

if __name__ == "__main__":
    main()
