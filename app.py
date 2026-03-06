import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

st.set_page_config(page_title="🏏 Cricket PPI Dashboard", layout="wide", page_icon="🏏")

@st.cache_data
def load_and_compute_ppi():
    files = {
        'BATSMEN_no_zeros.xlsx': 'batsmen',
        'ALL_ROUNDERS_no_zeros.xlsx': 'allrounders', 
        'BOWLERS_no_zeros.xlsx': 'bowlers',
        'WICKET_KEEPER_no_zeros.xlsx': 'wicketkeepers'
    }
    data = {}
    
    for file, category in files.items():
        try:
            df = pd.read_excel(file)  # Files in repo root
            df['Player'] = df['Player'].astype(str).str.strip()
            
            if category == 'batsmen':
                df['SR'] = (df['Runs'] / df['BF'] * 100).round(2)
                df['Boundary_Pct'] = ((df['4s'] + df['6s']) / df['BF'] * 100).round(2)
                df['PPI'] = (df['SR'] * 0.4 + df['Boundary_Pct'] * 0.3 + df['Runs'] * 0.001).round(2)
                
            elif category == 'allrounders':
                df['SR'] = (df['Runs'] / df['BF'] * 100).round(2)
                df['Bowling_PPI'] = (df.get('Wkts', 0) * 10 - df.get('Econ', 8) * 2).clip(lower=0)
                df['PPI'] = (df['SR'] * 0.3 + df['Bowling_PPI'] * 0.5 + df['Runs'] * 0.001).round(2)
                
            elif category == 'bowlers':
                df['Bowling_Avg'] = (df['Runs'] / df['Wkts'].replace(0,1)).round(2)
                df['PPI'] = (df['Wkts'] * 5 - df.get('Econ', 8) * 3 - df['Bowling_Avg'] * 0.1).clip(lower=0).round(2)
                
            elif category == 'wicketkeepers':
                df['SR'] = (df['Runs'] / df['BF'] * 100).round(2)
                df['Boundary_Pct'] = ((df['4s'] + df['6s']) / df['BF'] * 100).round(2)
                df['PPI']
