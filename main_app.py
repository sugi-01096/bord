import streamlit as st

def main():
    st.title("外部URLへのリンク")
       
        external_url = "https://maichan-bord-tui.streamlit.app/"
        st.print(f"[外部URLにアクセスする]({external_url})")

if __name__ == "__main__":
    main()
