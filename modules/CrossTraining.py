import streamlit as st
import plotly.graph_objects as go
from utils.data import filter_multi_feature

class CrossTraining:
    def q1_panel(self):
        with st.expander('Cross Training'):
            c1, c2 = st.columns(2)
            activities = c1.multiselect(
                'Activities',
                options=self.widget_options['other_activities']
            )
            strength_metrics = c2.multiselect(
                'Strength Metric',
                options=self.widget_options['strength_metrics']
            )

            if activities and strength_metrics:
                c = st.columns(len(activities))

                for i, sm in enumerate(strength_metrics):
                    chart = self.activity_strength_bar(sm, activities)
                    c[i].plotly_chart(chart)
    
    def activity_strength_bar(self, strength_metric, activities):

        data = filter_multi_feature(
            self.data,
            'other_activites',
            activities
        )[['other_activities', strength_metric]]

        if strength_metric in self.strength_conversion:
            data['y'] = [self.strength_conversion[i] for i in data[strength_metric]]
        else:
            data['y'] = data[strength_metric]

        fig = go.Figure()
        fig.add_trace(
            go.Bar()
        )

        return fig