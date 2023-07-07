import streamlit as st

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Post:
    def __init__(self, content, author, parent=None):
        self.content = content
        self.author = author
        self.parent = parent

class Thread:
    def __init__(self):
        self.posts = []

    def add_post(self, content, author, parent=None):
        post = Post(content, author, parent)
        self.posts.append(post)

    def edit_post(self, post, new_content):
        if post.author == current_user.username:
            post.content = new_content
        else:
            st.error("この投稿を編集する権限がありません。")

    def delete_post(self, post):
        if post.author == current_user.username:
            self.posts.remove(post)
        else:
            st.error("この投稿を削除する権限がありません。")

    def display_thread(self, posts=None, indent=0):
        if posts is None:
            posts = self.posts

        for post in posts:
            st.write(("  " * indent) + post.content)
            if post.parent:
                self.display_thread([p for p in self.posts if p.parent == post], indent + 1)

# 電子掲示板の作成と使用例
thread = Thread()

# 仮想のユーザーデータベース
user_db = []

# Streamlitアプリのレイアウトとインタラクションの作成
def main():
    st.title("スレッド型掲示板")
    login_or_register()

def login_or_register():
    st.subheader("ログインまたは新規登録")
    login_or_register_choice = st.radio("選択してください:", ("ログイン", "新規登録"))

    if login_or_register_choice == "ログイン":
        login()
    else:
        register()

def login():
    st.subheader("ログイン")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        user = authenticate(username, password)
        if user:
            st.success(f"{user.username}としてログインしました")
            global current_user
            current_user = user
            display_posts(thread.posts)
        else:
            st.error("無効なユーザー名またはパスワードです。")

def register():
    st.subheader("新規登録")
    new_username = st.text_input("新しいユーザー名")
    new_password = st.text_input("新しいパスワード", type="password")

    if st.button("新規登録"):
        if not new_username or not new_password:
            st.error("ユーザー名とパスワードは空にできません。")
        elif user_exists(new_username):
            st.error("ユーザー名は既に存在します。")
        else:
            new_user = User(new_username, new_password)
            user_db.append(new_user)
            st.success("登録が成功しました。ログインしてください。")
            login()

def authenticate(username, password):
    for user in user_db:
        if user.username == username and user.password == password:
            return user
    return None

def user_exists(username):
    for user in user_db:
        if user.username == username:
            return True
    return False

def display_posts(posts):
    for post in posts:
        st.write(f"投稿者: {post.author}")
        st.write(post.content)
        if post.parent:
            st.write("返信先:")
            display_posts([p for p in thread.posts if p.parent == post])
        st.write("---")

if __name__ == "__main__":
    main()
