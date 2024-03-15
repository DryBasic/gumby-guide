import streamlit as st
from utils.data import load_metadata

def HelpfulSidebar():

    meta = load_metadata()

    with st.sidebar:
        with st.expander('Feature Descriptions', True):
            feature = st.selectbox(
                'Feature',
                options=list(meta['Label'].values)
            )
            st.text_area(
                'Description',
                value=meta.query(f'Label == "{feature}"')['Desc'].values[0],
            )
            

        with st.expander('Yosemite to Ewbank Conversion', True):
            st.image('assets/yosemite_ewbank.jpg')


        