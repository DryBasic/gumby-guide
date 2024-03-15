import pandas as pd
import streamlit as st
import json
import yaml

@st.cache_data
def load_metadata():
    df = pd.read_csv('data/feature_metadata.csv')
    return df

@st.cache_data
def load_widget_options():
    with open('data/widget_options.json') as f:
        options = json.load(f)
    return options

@st.cache_data
def load_data():
    df = pd.read_csv('data/clean.csv')
    return df

@st.cache_data
def apply_filters(df, filters):
    if filters['sex'] != 'All':
        df = df.query(f'sex == {filters["sex"]}')

    values = load_widget_options()
    
    for attr in filters.keys():
        if attr != 'sex':
            lower, upper = filters[attr]
            isin = []
            started = False
            ended = False
            for v in values[attr]:
                if v == lower:
                    started = True
                if v == upper:
                    ended = True

                if started:
                    isin.append(v)
                if ended:
                    break

            df = df.query(f"{attr} in {isin}")
    
    return df