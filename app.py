import streamlit as st
from modules.sidebar import HelpfulSidebar
from modules.Dashboard import Dashboard

st.set_page_config(
    page_title="Gumby's Guide",
    # page_icon=,
    layout='wide',
    initial_sidebar_state='expanded'
)
HelpfulSidebar()

dash = Dashboard()
dash.q1_panel()
dash.q2_panel()
dash.q5_panel()
dash.q4_panel()
dash.debug()