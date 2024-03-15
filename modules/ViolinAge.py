import streamlit as st
import plotly.graph_objects as go

class ViolinAge:
    def q5_panel(self):
        with st.expander("What grade should you be climbing?", True):
            c1, c2 = st.columns(2)
            grade_opts = [self.col_to_label[i] for i in self.strength_conversion.keys()]
            x_features = (
                'years_climbing',
                'indoor_outdoor',
                'sex',
                'height_binned',
                'weight_binned',
                'wingspan_binned',
                'pullups_maxcount_binned',
                'pushups_maxcount_binned'
            )
            x_opts = [self.col_to_label[i] for i in x_features]
            xlabel = c1.selectbox('Characteristic', options=x_opts)
            grade = c2.selectbox(
                        'Grade',
                        options=grade_opts
                    )
            x_attr = self.label_to_col[xlabel]
            grade_attr = self.label_to_col[grade]
            data = self.data[[x_attr, grade_attr]]
            st.plotly_chart(self.violin(data, x_attr, grade_attr), use_container_width=True)

    def violin(self, df, x, y):
        fig = go.Figure()
        for group in self.widget_options[x]:
            gdf = df.query(f'{x} == "{group}"')
            fig.add_trace(
                go.Violin(
                    x=gdf[x], y=self.widget_options[y], name=group,
                    box_visible=True, meanline_visible=True, opacity=0.6
                )
            )

        fig.update_layout(yaxis_zeroline=False)
        return fig