import streamlit as st
import plotly.graph_objects as go
from utils.data import filter_multi_feature

class TrainingTrainingDist:
    def trainingtraining_dist(self):
        multi = self.config['multi_features'][1:]
        with st.expander('Hanging, Strength, and Endurance', True):
            pick = st.selectbox(
                'toplevel',
                options=[self.col_to_label[i] for i in multi],
                label_visibility='collapsed'
            )
            c1, c2 = st.columns(2)
            multi_opts = self.widget_options[self.label_to_col[pick]]
            multi_picks = c1.multiselect(
                'Grips/Exercises',
                options=multi_opts,
                default=(multi_opts[1], multi_opts[2])
            )
            strength_metrics = c2.multiselect(
                'Strength Metric',
                options=self.widget_options['strength_metrics'],
                default=['Boulder Grade'],
                key='Q4'
            )

            if multi_picks and strength_metrics:
                c = st.columns(len(strength_metrics))

                for i, sm in enumerate(strength_metrics):
                    chart = self.exercise_strength_bar(
                        feature=self.label_to_col[pick],
                        strength_metric=sm,
                        activities=multi_picks
                    )
                    c[i].plotly_chart(chart, use_container_width=True)
    
    def exercise_strength_bar(self, feature, strength_metric, activities):
        strength_attr = self.label_to_col[strength_metric]
        data = filter_multi_feature(
            self.data,
            feature,
            activities
        )[[feature, strength_attr, 'cid']]

        grouped = data.explode(feature)\
                    .groupby([strength_attr, feature])\
                    .count()\
                    .reset_index()
        fig = go.Figure(layout={'title_text':strength_metric})
        for activity in activities:
            act_df = grouped.query(f'{feature} == "{activity}"')
            fig.add_trace(
                go.Bar(name=activity, x=act_df[strength_attr], y=act_df['cid'])
            )
            fig.update_xaxes(
                categoryorder='array',
                categoryarray= self.widget_options[strength_attr])
        return fig
    