import streamlit as st

st.set_page_config(
    page_title="Site Developer Details",
    page_icon="🙂"
)

st.header("Abir Sinha")

st.sidebar.success("Member 1")

tab1, tab2 = st.tabs(["GitHub", "LinkedIn"])


with tab1:
    st.header("My Github Link is :-")
    st.write("[Github Link](https://github.com/AbirSinha8294)")

with tab2:
    st.header("My LinkedIn is :- ")
    st.write("[LinkedIn Link](https://www.linkedin.com/in/abir-sinha-57b654204/)")