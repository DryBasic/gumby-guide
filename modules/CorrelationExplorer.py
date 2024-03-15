import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from copy import deepcopy

class CorrelationExplorer:
    def q2_panel(self):
        with st.expander('Correlation Explorer', True):
            c1, c2, _, c3 = st.columns([1, 1, 0.1, 4])
            opts = [self.col_to_label[i] for i in self.config['correx_features']]
            x = c1.selectbox('x', options=opts, index=1)
            y = c2.selectbox('y', options=opts, index=0)

            c1, c2 = st.columns([1.25, 3])
            if x != y:
                c1.plotly_chart(self.scatter(x, y), use_container_width=True)
            c2.plotly_chart(self.correlation_pareto(), use_container_width=True)

    def scatter(self, x_label, y_label):
        x_attr = self.label_to_col[x_label]
        y_attr = self.label_to_col[y_label]
        data = self.data[[x_attr, y_attr]]

        if x_attr in self.strength_conversion:
            data[x_label] = [self.strength_conversion[x_attr][i] for i in data[x_attr].values]
        else:
            data[x_label] = data[x_attr]
        if y_attr in self.strength_conversion:
            data[y_label] = [self.strength_conversion[y_attr][i] for i in data[y_attr].values]
        else:
            data[y_label] = data[y_attr]

        title = f"corr({x_label}, {y_label})={round(data[x_label].corr(data[y_label]),2)}"
        fig = go.Figure(layout={'title_text':title})
        fig.add_trace(
            go.Scatter(
                x=data[x_label], y=data[y_label],
                mode='markers', marker={'opacity':0.5}
            )
        )
        return fig

    def compute_correlations(self):
        data = deepcopy(self.data)
        b = 'hardest_boulder_confident'
        r = 'hardest_route_confident'

        data[b] = [self.strength_conversion[b][i] for i in data[b]]
        data[r] = [self.strength_conversion[r][i] for i in data[r]]
        corrs = []
        for feature in self.config['correx_features']:
            if feature not in (b, r):
                corrs.append([b, self.col_to_label[feature], data[b].corr(data[feature])])
                corrs.append([r, self.col_to_label[feature], data[r].corr(data[feature])])

        df = pd.DataFrame(corrs, columns=['group', 'feature', 'corr']).sort_values('corr')
        return df


    def correlation_pareto(self):
        b = 'hardest_boulder_confident'
        r = 'hardest_route_confident'
        corr_df = self.compute_correlations()

        b_corr = corr_df.query(f'group == "{b}"')
        r_corr = corr_df.query(f'group == "{r}"')
        fig = go.Figure(layout={'title_text': 'Correlations with Bouldering vs Route Performance'})
        fig.add_traces([
            go.Bar(
                name='Boulder Grade',
                x=b_corr['feature'], y=b_corr['corr']
            ),
            go.Bar(
                name='Rope Grade',
                x=r_corr['feature'], y=r_corr['corr']
            ),
        ])
        return fig