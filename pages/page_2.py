import streamlit as st
import json
from datetime import datetime
import pytz
import urllib.parse

# 禁止ワードのリスト
banned_words = ["馬鹿", "禁止ワード2", "禁止ワード3"]

# ユーザーの投稿内容をチェックする関数
def check_post_content(content):
    # タイトルと投稿内容の禁止ワードの検出
    for banned_word in banned_words:
        if banned_word in content:
            content = content.replace(banned_word, "＠" * len(banned_word))
    return content

def save_post(content, good_count=0, bad_count=0):
    now = datetime.now(pytz.timezone("Asia/Tokyo"))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    post = {"content": content, "timestamp": now_str, "good": good_count, "bad": bad_count}
    with open('posts2.json', 'a') as file:
        file.write(json.dumps(post))
        file.write('\n')

def load_posts():
    with open('posts2.json', 'r') as file:
        lines = file.readlines()
        posts = [json.loads(line.strip()) for line in lines]
        
        # タイムスタンプを日本時間に変換
        for post in posts:
            timestamp = datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S")
            timestamp = pytz.timezone("Asia/Tokyo").localize(timestamp)
            post['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return posts

def main():
    st.title("テスト")

    # 新規投稿の入力
    new_post_content = st.text_area("投稿", height=100)

    # 投稿ボタンが押された場合
    if st.button("投稿する") and new_post_content:
        new_post_content = check_post_content(new_post_content)
        if "＠" in new_post_content:
            st.warning("禁止ワードが含まれています！")

        save_post(new_post_content)
        st.success("投稿が保存されました！")

    # 保存された投稿の表示
    posts = load_posts()
    st.subheader("保存された投稿")

    if not posts:
        st.info("まだ投稿がありません。")
    else:
        for i, post in enumerate(posts):
            st.subheader(f"投稿{i + 1}")
            st.write(post['content'])  # 投稿内容を表示
            st.write(post['timestamp'])  # タイムスタンプを表示
            
            # GoodとBadのカウントを表示
            col1, col2 = st.beta_columns(2)
            with col1:
                good_count = st.button(f"Good ({post['good']})")
            with col2:
                bad_count = st.button(f"Bad ({post['bad']})")
            
            # GoodとBadのカウントを更新
            if good_count:
                posts[i]['good'] += 1
            if bad_count:
                posts[i]['bad'] += 1
            
            st.markdown("---")

    # 投稿の更新を保存
    with open('posts.json', 'w') as file:
        for post in posts:
            file.write(json.dumps(post))
            file.write('\n')

if __name__ == "__main__":
    main()
