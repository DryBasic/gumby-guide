import streamlit as st
from utils.data import *
from modules.CrossTraining import CrossTraining
from modules.CorrelationExplorer import CorrelationExplorer
from modules.ViolinAge import ViolinAge
from modules.TrainingTraining import TrainingTraining
from modules.sidebar import HelpfulSidebar

st.set_page_config(
    page_title="Gumby's Guide",
    # page_icon=,
    layout='wide',
    initial_sidebar_state='expanded'
)
config = load_config()
widget_opts = config['widget_options']
strength_conversion = config['strength_conversion']
meta = load_metadata()
data = load_data()


class Dashboard(CrossTraining, CorrelationExplorer, ViolinAge, TrainingTraining):
    def __init__(self) -> None:
        self.widget_options = widget_opts
        self.strength_conversion = strength_conversion
        self.config = config
        self.col_to_label = {col: label for col, label in meta[['DataFrameKey', 'Label']].values}
        self.label_to_col = {label: col for col, label in self.col_to_label.items()}
        
        st.title("The Gumby's Guide to Getting Good")
        filter_pane = st.expander('Global Filters', True)
        c1, _, c2, _, c3 = filter_pane.columns([4, 1, 4, 1, 5])

        global_filters = {}
        global_filters['sex'] = c1.radio('Sex', options=['All', 'M', 'F'], horizontal=True),
        global_filters['years_climbing'] = self.slider(c1, 'years_climbing'),
        for attr in ('hardest_boulder_confident', 'hardest_route_confident'):
            global_filters[attr] = self.slider(c2, attr),
        self.climbers = c3.multiselect(
                'Highlight specific climbers',
                options=widget_opts['cid'],
                help='Does nothing at the moment'
            )
        
        self.data = apply_global_filters(data, global_filters)
        c3.markdown(f'{len(self.data)} Climbers selected')

        self.gf = global_filters

    def slider(self, container, attribute):
        label = self.col_to_label[attribute]
        opts = widget_opts[attribute]
        return container.select_slider(
            label,
            options=opts,
            value=(opts[0], opts[-1])
        )
    
    def debug(self):
        with st.expander('Dataset'):
            # st.code(self.gf)
            st.dataframe(self.data)
            st.download_button(
                label="Download data as CSV",
                data=self.data.to_csv().encode('utf-8'),
                file_name='climbers.csv',
                mime='text/csv',
            )

HelpfulSidebar()
dash = Dashboard()
dash.q1_panel()
dash.q2_panel()
dash.q5_panel()
dash.q4_panel()
dash.debug()


