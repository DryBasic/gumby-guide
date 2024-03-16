import streamlit as st
from utils.data import *
from modules.CrossTrainingDist import CrossTrainingDist
from modules.CrossTrainingGroup import CrossTrainingGroup
from modules.CorrelationExplorer import CorrelationExplorer
from modules.ViolinDist import ViolinDist
from modules.TrainingTraining import TrainingTrainingDist
from modules.HelpfulSidebar import HelpfulSidebar

st.set_page_config(
    page_title="Gumby's Guide",
    # page_icon=,
    layout='wide',
    initial_sidebar_state='expanded'
)
config = load_config()
widget_opts = config['widget_options']
conversion = config['conversion']
meta = load_metadata()
data = load_data()


class Dashboard(CrossTrainingDist, CrossTrainingGroup, CorrelationExplorer, ViolinDist, TrainingTrainingDist):
    def __init__(self) -> None:
        self.widget_options = widget_opts
        self.conversion = conversion
        self.config = config
        self.col_to_label = {col: label for col, label in meta[['DataFrameKey', 'Label']].values}
        self.label_to_col = {label: col for col, label in self.col_to_label.items()}
        
        st.title("The Gumby's Guide to Getting Good")
        filter_pane = st.expander('Global Filters', True)
        c1, _, c2, _, c3 = filter_pane.columns([4, 1, 4, 1, 5])

        global_filters = {}
        global_filters['sex'] = c1.radio('Sex', options=['All', 'M', 'F'], horizontal=True),
        global_filters['indoor_outdoor'] = c1.radio('Gym Bro or Crag Dad?', horizontal=False,
                                                     options=self.widget_options['indoor_outdoor'])
        #global_filters['years_climbing'] = self.slider(c1, 'years_climbing'),

        for attr in ('hardest_boulder_confident', 'hardest_route_confident', 'years_climbing'):
            global_filters[attr] = self.slider(c2, attr, categorical=True)
        for attr in ('height', 'weight', 'wingspan'):
            global_filters[attr] = self.slider(c3, attr, categorical=False)

        
        self.data = apply_global_filters(data, global_filters)
        c3.markdown(f'{len(self.data)} Climbers selected')

        self.gf = global_filters

    def slider(self, container, attribute, categorical=True):
        label = self.col_to_label[attribute]
        opts = widget_opts[attribute]

        if categorical:
            return container.select_slider(
                label,
                options=opts,
                value=(opts[0], opts[-1])
            )
        else:
            array = np.array([float(i) for i in opts if i==i])
            min = array.min()
            max = array.max()
            return container.slider(
                label,
                min_value = min,
                max_value = max,
                value = (min, max)
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
dash.crosstrain_dist()
dash.crosstrain_group()
dash.correx()
dash.violin_dist()
dash.trainingtraining_dist()
dash.debug()


