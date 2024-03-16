import streamlit as st
import plotly.graph_objects as go
from utils.data import filter_multi_feature

class CrossTraining:
    def q1_panel(self):
        with st.expander('Cross Training', True):
            c1, c2 = st.columns(2)
            activities = c1.multiselect(
                'Activities',
                options=self.widget_options['other_activities'],
                default=['yoga', 'cardio']
            )
            strength_metrics = c2.multiselect(
                'Strength Metric',
                options=self.widget_options['strength_metrics'],
                default=['Boulder Grade']
            )

            if activities and strength_metrics:
                c = st.columns(len(strength_metrics))

                for i, sm in enumerate(strength_metrics):
                    chart = self.activity_strength_bar(sm, activities)
                    c[i].plotly_chart(chart, use_container_width=True)
    
    def activity_strength_bar(self, strength_metric, activities):
        strength_attr = self.label_to_col[strength_metric]
        data = filter_multi_feature(
            self.data,
            'other_activities',
            activities
        )[['other_activities', strength_attr, 'cid']]

        grouped = data.explode('other_activities')\
                    .groupby([strength_attr, 'other_activities'])\
                    .count()\
                    .reset_index()
        
        fig = go.Figure(layout={'title_text':strength_metric})
        for activity in activities:
            act_df = grouped.query(f'other_activities == "{activity}"')
            fig.add_trace(
                go.Bar(name=activity, x=act_df[strength_attr], y=act_df['cid'])
            )
            fig.update_xaxes(
                categoryorder='array',
                categoryarray= self.widget_options[strength_attr])
        return fig
    