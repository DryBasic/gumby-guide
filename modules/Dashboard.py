import streamlit as st
from utils.data import *
from modules.Question1 import CrossTraining

widget_opts = load_widget_options()
meta = load_metadata()
data = load_data()

class Dashboard(CrossTraining):
    def __init__(self) -> None:
        self.widget_options = widget_opts
        self.col_to_label = {col: label for col, label in meta[['DataFrameKey', 'Label']].values}
        
        st.title("The Gumby's Guide to Getting Good")
        filter_pane = st.expander('Global Filters', True)
        c1, _, c2, _, c3 = filter_pane.columns([4, 1, 4, 1, 5])

        global_filters = {}
        global_filters['sex'] = c1.radio('Sex', options=['All', 'M', 'F'], horizontal=True),
        global_filters['years_climbing'] = self.slider(c1, 'years_climbing'),
        for attr in ('hardest_boulder_confident', 'hardest_route_confident'):
            global_filters[attr] = self.slider(c2, attr),
        
        self.climbers = c3.multiselect(
                'Show specific climbers',
                options=widget_opts['cid']
            )

        self.data = apply_filters(data, global_filters)

    def slider(self, container, attribute):
        label = self.col_to_label[attribute]
        opts = widget_opts[attribute]
        return container.select_slider(
            label,
            options=opts,
            value=(opts[0], opts[-1])
        )