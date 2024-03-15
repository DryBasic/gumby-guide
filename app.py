import streamlit as st
from modules.sidebar import HelpfulSidebar
from modules.Dashboard import Dashboard

st.set_page_config(
    page_title="",
    # page_icon=,
    layout='wide',
    initial_sidebar_state='expanded'
)
HelpfulSidebar()

dash = Dashboard()
dash.q1_panel()
