def main():
    st.title("雑談１")

    new_post_content = st.text_area("投稿", height=100)
    new_post_image = st.file_uploader("画像をアップロード", type=["jpg", "jpeg", "png"])

    if st.button("投稿する") and new_post_content:
        new_post_content = check_post_content(new_post_content)
        if "＠" in new_post_content:
            st.warning("禁止ワードが含まれています！")

        image_data = None
        if new_post_image:
            image_data = new_post_image.read()

        save_post(new_post_content, image_data)
        st.success("投稿が保存されました！")

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

            st.write(post['timestamp'])

            # いいねとバッドのボタン
            likes = st.button(f"👍 いいね {post.get('likes', 0)}", key=f"like_{post['timestamp']}")
            dislikes = st.button(f"👎 バッド {post.get('dislikes', 0)}", key=f"dislike_{post['timestamp']}")

            # Ensure 'likes' and 'dislikes' fields exist in the post
            if 'likes' not in post:
                post['likes'] = 0
            if 'dislikes' not in post:
                post['dislikes'] = 0

            if likes:
                post['likes'] += 1
            if dislikes:
                post['dislikes'] += 1

            st.markdown("---")

if __name__ == "__main__":
    main()
