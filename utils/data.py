import pandas as pd; import numpy as np
import streamlit as st
import json

@st.cache_data
def load_data():
    df = pd.read_csv('data/clean.csv')
    cfg = load_config()
    for feature in cfg['multi_features']:
        df[feature] = [eval(i) if i==i else [] for i in df[feature].values]
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
    cfg = load_config()
    values = load_config()['widget_options']

    categorical = (
        'hardest_boulder_confident',
        'hardest_route_confident',
        'years_climbing'
    )
    continuous = cfg['continuous_features']
    for attr in filters.keys():
            
        if attr == 'sex':
            # I have no idea why this output is a tuple...
            if filters['sex'][0] != 'All':
                df = df.query(f'sex == "{filters["sex"][0]}"')
        elif attr == 'indoor_outdoor':
            value = filters[attr]
            df = df.query(f'indoor_outdoor == "{value}"')

        elif attr in continuous:
            lower, upper = filters[attr]
            df = df.query(f'{lower} <= {attr} <= {upper}')
        
        elif attr in categorical:
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

@st.cache_data
def filter_multi_feature(df: pd.DataFrame, feature: str, values: list):
    passing = []
    for i, row in df[[feature]].iterrows():
        for v in values:
            if v in row[feature]:
                passing.append(i)

    return df.loc[passing]
