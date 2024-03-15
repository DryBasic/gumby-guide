import streamlit as st
from modules.Question1 import Question1

class Dashboard(Question1):
    def __init__(self) -> None:
        
        filter_pane = st.expander('Global Filters', True)
        c1, _, c2, _ = filter_pane.columns([4, 1, 4, 5])

        self.global_filters = dict(
            sex=c1.radio('Sex', options=['All', 'M', 'F'], horizontal=True),
            years_climbing=c1.slider('Years Climbing', max_value=8),
            boulder_grade=c2.slider('Hardest Boulder Grade'),
            rope_grade=c2.slider('Hardest Rope Grade')
        )