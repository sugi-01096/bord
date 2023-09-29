import streamlit as st

def main():
    st.title("外部URLへのリダイレクト")

    external_url = "https://maichan-bord-tui.streamlit.app/"

    # JavaScriptを使用して外部URLにリダイレクト
    st.write(f'<script>window.location.href = "{external_url}";</script>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
