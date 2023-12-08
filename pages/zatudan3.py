import streamlit as st
import json
import base64  # 追加
from datetime import datetime
import pytz
import pandas as pd

# 禁止ワードをExcelファイルから読み込む
df = pd.read_excel("banned_list.xlsx", sheet_name=0)
# 禁止ワードをbanned_words に
banned_words = df['禁止ワード'].tolist()
banned_words = [str(word) for word in banned_words]

# ユーザーの投稿内容をチェックする関数
def check_post_content(content):
    # タイトルと投稿内容の禁止ワードの検出
    for banned_word in banned_words:
        if banned_word in content:
            content = content.replace(banned_word, "＠" * len(banned_word))
    return content

def save_post(content, image):
    now = datetime.now(pytz.timezone("Asia/Tokyo"))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # 画像データをBase64にエンコード
    image_data = None
    if image:
        image_data = base64.b64encode(image).decode('utf-8')

    post = {"content": content, "image": image_data, "timestamp": now_str}
    with open('posts91.json', 'a') as file:
        file.write(json.dumps(post))
        file.write('\n')

def load_posts():
    with open('posts91.json', 'r') as file:
        lines = file.readlines()
        posts = [json.loads(line.strip()) for line in lines]

        # タイムスタンプを日本時間に変換
        for post in posts:
            timestamp = datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S")
            timestamp = pytz.timezone("Asia/Tokyo").localize(timestamp)
            post['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return posts

def main():
    st.title("雑談３")

    # 新規投稿の入力
    new_post_content = st.text_area("投稿", height=100)
    new_post_image = st.file_uploader("画像をアップロード", type=["jpg", "jpeg", "png"])

    # 投稿ボタンが押された場合
    if st.button("投稿する") and new_post_content:
        new_post_content = check_post_content(new_post_content)
        if "＠" in new_post_content:
            st.warning("禁止ワードが含まれています！")

        # 画像がアップロードされていれば、バイナリデータに変換して保存
        image_data = None
        if new_post_image:
            image_data = new_post_image.read()

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
            # 画像があれば表示
            if 'image' in post and post['image'] is not None:
                st.image(base64.b64decode(post['image']), caption="Uploaded Image", use_column_width=True)
            st.write(post['timestamp'])  # タイムスタンプを表示
            st.markdown("---")

if __name__ == "__main__":
    main()
