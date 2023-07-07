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
            st.error("You are not authorized to edit this post.")

    def delete_post(self, post):
        if post.author == current_user.username:
            self.posts.remove(post)
        else:
            st.error("You are not authorized to delete this post.")

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
user_db = [
    User("user1", "password1"),
    User("user2", "password2"),
    User("user3", "password3")
]

# Streamlitアプリのレイアウトとインタラクションの作成
def main():
    st.title("Threaded Bulletin Board")
    login()

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.success(f"Logged in as {user.username}")
            global current_user
            current_user = user
            display_posts(thread.posts)
        else:
            st.error("Invalid username or password.")

def authenticate(username, password):
    for user in user_db:
        if user.username == username and user.password == password:
            return user
    return None

def display_posts(posts):
    for post in posts:
        st.write(f"Author: {post.author}")
        st.write(post.content)
        if post.parent:
            st.write("Reply to:")
            display_posts([p for p in thread.posts if p.parent == post])
        st.write("---")

if __name__ == "__main__":
    main()
