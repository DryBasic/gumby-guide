import pandas as pd
import streamlit as st
import json
import yaml

@st.cache_data
def load_data():
    df = pd.read_csv('data/clean.csv')
    df.other_activities = [eval(i) if i==i else [] for i in df.other_activities.values]
    return df

@st.cache_data
def load_metadata():
    df = pd.read_csv('data/feature_metadata.csv')
    return df

@st.cache_data
def load_config():
    with open('data/config.json') as f:
        config = json.load(f)
    return config

@st.cache_data
def apply_global_filters(df: pd.DataFrame, filters: dict):
    if filters['sex'][0] != 'All':
        df = df.query(f'sex == "{filters["sex"][0]}"')

    values = load_config()['widget_options']
    
    for attr in filters.keys():
        if attr != 'sex':
            lower, upper = filters[attr][0]
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

@st.cache_data
def filter_multi_feature(df: pd.DataFrame, feature: str, values: list):
    passing = []
    for i, row in df[[feature]].iterrows():
        for v in values:
            if v in row[feature]:
                passing.append(i)

    return df.iloc[passing]

# def convert_strength_to_continuous(strength_metric, )