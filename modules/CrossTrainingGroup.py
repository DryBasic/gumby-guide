import streamlit as st
import plotly.graph_objects as go
from utils.data import filter_multi_feature

class CrossTrainingGroup:
    def crosstrain_group(self):
        with st.expander('Cross Training Impact', True):
            c1, c2, c3 = st.columns(3)
            activities = c1.multiselect(
                'Activities',
                options=self.widget_options['other_activities'],
                default=['yoga', 'cardio', 'running', 'biking']
            )
            strength_metric = c2.selectbox(
                'Strength Metric',
                options=self.widget_options['strength_metrics'][:-2],
            )
            grouper = c3.selectbox(
                'Group By',
                options=self.config['crossG_features']
            )

            if activities and strength_metric:
                chart = self.activity_grouped_bar(strength_metric, activities, grouper)
                st.plotly_chart(chart, use_container_width=True)
    
    def activity_grouped_bar(self, strength_metric, activities, grouper):
        strength_attr = self.label_to_col[strength_metric]
        grouper_attr = self.label_to_col[grouper]
        data = filter_multi_feature(
            self.data,
            'other_activities',
            activities
        )[['other_activities', strength_attr, grouper_attr]]
        data['scont'] = [self.conversion[strength_attr][i] for i in data[strength_attr]]

        grouped = data.explode('other_activities')\
                    .groupby(['other_activities', grouper_attr])['scont']\
                    .mean()\
                    .reset_index()
        
        fig = go.Figure(layout={'title_text':f"Average {strength_metric}"})
        for activity in activities:
            act_df = grouped.query(f'other_activities == "{activity}"')
            fig.add_trace(
                go.Bar(name=f"{activity}", x=act_df[grouper_attr], y=act_df['scont'])
            )
            fig.update_xaxes(
                categoryorder='array',
                categoryarray= self.widget_options[strength_attr])
        return fig
    