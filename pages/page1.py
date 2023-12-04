import streamlit as st
import json
import base64
from datetime import datetime
import pytz
import pandas as pd

def initialize_session_state():
    if 'posts' not in st.session_state:
        st.session_state.posts = []

def main():
    initialize_session_state()

    st.title("雑談１")

    new_post_content = st.text_area("投稿", height=100)
    new_post_image = st.file_uploader("画像をアップロード", type=["jpg", "jpeg", "png"])

    if st.button("投稿する", key="post_button") and new_post_content:
        new_post_content = check_post_content(new_post_content)
        if "＠" in new_post_content:
            st.warning("禁止ワードが含まれています！")

        image_data = None
        if new_post_image:
            image_data = new_post_image.read()

        save_post(new_post_content, image_data)
        st.success("投稿が保存されました！")

    st.subheader("保存された投稿")

    if not st.session_state.posts:
        st.info("まだ投稿がありません。")
    else:
        for post in st.session_state.posts:
            st.subheader(post['content'])

            # 画像があれば表示
            if 'image' in post and post['image'] is not None:
                st.image(base64.b64decode(post['image']), caption="Uploaded Image", use_column_width=True)

            st.write(post['timestamp'])

            # いいねとバッドのボタン
            like_button_key = f"like_{post['timestamp']}"
            dislike_button_key = f"dislike_{post['timestamp']}"

            likes = st.button(f"👍  {post.get('likes', 0)}", key=like_button_key)
            dislikes = st.button(f"👎  {post.get('dislikes', 0)}", key=dislike_button_key)

            # いいねとバッドの数を更新
            if likes:
                post['likes'] += 1
                st.session_state[dislike_button_key] = False  # バッドボタンを無効化
            elif dislikes:
                post['dislikes'] += 1
                st.session_state[like_button_key] = False  # いいねボタンを無効化

        st.markdown("---")

if __name__ == "__main__":
    main()
