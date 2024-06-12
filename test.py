import streamlit as st

col1, col2 = st.columns(2)
container1 = st.container()
container2 = st.container()

with col1:
    with container1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    with container2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")
