import streamlit as st
import json
from datetime import datetime
import pytz
import urllib.parse
#3つ目のページ

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

def save_post(content):
    now = datetime.now(pytz.timezone("Asia/Tokyo"))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    post = {"content": content, "timestamp": now_str}
    with open('posts3.json', 'a') as file:
        file.write(json.dumps(post))
        file.write('\n')

def load_posts():
    with open('posts3.json', 'r') as file:
        lines = file.readlines()
        posts = [json.loads(line.strip()) for line in lines]
        
        # タイムスタンプを日本時間に変換
        for post in posts:
            timestamp = datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S")
            timestamp = pytz.timezone("Asia/Tokyo").localize(timestamp)
            post['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return posts

def main():
    st.title("test")

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
        for post in posts:
            st.subheader(post['content'])
            st.write(post['timestamp'])  # タイムスタンプを表示
            st.markdown("---")

if __name__ == "__main__":
    main()
