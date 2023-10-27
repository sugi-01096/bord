import streamlit as st

def main():
    st.title("外部URLへのリンク")

    # ボタンをクリックして外部URLに飛ぶ
    if st.button("外部URLにアクセス"):
        external_url = "https://maichan-bord-ben.streamlit.app/"
        st.markdown(f"[外部URLにアクセスする]({external_url})")

if __name__ == "__main__":
    main()
