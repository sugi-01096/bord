import streamlit as st
import json

def save_post(title, content):
    post = {"title": title, "content": content}
    with open('posts.json', 'a') as file:
        json.dump(post, file)
        file.write('\n')

def load_posts():
    with open('posts.json', 'r') as file:
        return [json.loads(line) for line in file]

def main():
    st.title("")  # Removed the title here

    # 新規投稿の入力
    new_post_title = st.text_input("タイトル")
    new_post_content = st.text_area("新規投稿", height=100)

    # 投稿ボタンが押された場合
    if st.button("投稿する") and new_post_title and new_post_content:
        save_post(new_post_title, new_post_content)
        st.success("投稿が保存されました！")

    # 保存された投稿の表示
    posts = load_posts()
    st.subheader("保存された投稿")

    if not posts:
        st.info("まだ投稿がありません。")
    else:
        for post in posts:
            st.text(post["title"])
            st.text(post["content"])
            st.markdown("---")

if __name__ == "__main__":
    main()
