import streamlit as st

class CrossTraining:
    def q1_panel(self):
        with st.expander('Cross Training'):
            c1, c2 = st.columns(2)
            c1.multiselect(
                'Activities',
                options=self.widget_options['other_activities']
            )
            c2.multiselect(
                'Strength Metric',
                options=self.widget_options['strength_metrics']
            )