import streamlit as st

def HelpfulSidebar():

    with st.sidebar:
        with st.expander('Feature Descriptions'):
            st.selectbox('Feature', options=[])
            

        with st.expander('Yosemite to Ewbank Conversion'):
            st.image('assets/yosemite_ewbank.jpg')

        