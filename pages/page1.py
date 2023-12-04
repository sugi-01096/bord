import streamlit as st
import json
import base64
from datetime import datetime
import pytz
import pandas as pd

# ...

# ユーザーの投稿内容をチェックする関数
def check_post_content(content):
    # ...

# 投稿データにいいねとバッドの情報を追加する関数
def update_post_reaction(post, reaction):
    if reaction == 'like':
        post['likes'] = post.get('likes', 0) + 1
    elif reaction == 'dislike':
        post['dislikes'] = post.get('dislikes', 0) + 1

# ...

# 投稿を保存する関数
def save_post(content, image):
    # ...

    post = {"content": content, "image": image_data, "timestamp": now_str, "likes": 0, "dislikes": 0}
    with open('posts1.json', 'a') as file:
        file.write(json.dumps(post))
        file.write('\n')

# ...

# 保存された投稿の表示
def display_posts(posts):
    # ...

    for post in posts:
        st.subheader(post['content'])
        # ...

        # 表示時にいいねとバッドのボタンを追加
        like_btn = st.button(f"👍 ({post['likes']})", key=f"like_{post['timestamp']}")
        dislike_btn = st.button(f"👎 ({post['dislikes']})", key=f"dislike_{post['timestamp']}")

        if like_btn:
            update_post_reaction(post, 'like')
        if dislike_btn:
            update_post_reaction(post, 'dislike')

        # 表示時にいいねとバッドの合計を表示
        st.write(f"Total Likes: {post['likes']}, Total Dislikes: {post['dislikes']}")
        st.write(post['timestamp'])
        st.markdown("---")

# ...

def main():
    st.title("雑談１")

    # ...

    # 保存された投稿の表示
    posts = load_posts()
    st.subheader("保存された投稿")

    if not posts:
        st.info("まだ投稿がありません。")
    else:
        display_posts(posts)

# ...
