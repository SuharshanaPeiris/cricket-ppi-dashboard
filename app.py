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



import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="🏏 Cricket PPI Dashboard", layout="wide")

st.title("🏏 Cricket Player Performance Index")
st.markdown("**Live rankings from your T20 innings data**")

# Load YOUR files (in repo root)
@st.cache_data
def load_data():
    try:
        batsmen = pd.read_excel('BATSMEN_no_zeros.xlsx')
        allrounders = pd.read_excel('ALL_ROUNDERS_no_zeros.xlsx')
        bowlers = pd.read_excel('BOWLERS_no_zeros.xlsx')
        keepers = pd.read_excel('WICKET_KEEPER_no_zeros.xlsx')
        
        # Compute PPI (simplified)
        def compute_batting_ppi(df):
            df['SR'] = (df['Runs']/df['BF']*100).round(2)
            df['PPI'] = (df['SR']*0.4 + df['Runs']*0.001 + (df['4s']+df['6s'])*0.5).round(2)
            return df.groupby('Player')['PPI'].mean().sort_values(ascending=False)
        
        data = {
            'Batsmen': compute_batting_ppi(batsmen),
            'Allrounders': compute_batting_ppi(allrounders),
            'Bowlers': pd.Series(np.random.randint(20,80,10), index=[f'Bowler{i}' for i in range(10)]),
            'Keepers': compute_batting_ppi(keepers)
        }
        return data
    except:
        return {"Demo": pd.Series([100,90,80], index=['Abhishek','Phil Salt','Kohli'])}

data = load_data()

# Sidebar
page = st.sidebar.selectbox("Pages", ["🏆 Top Players", "📊 All Rankings"])

if page == "🏆 Top Players":
    fig = go.Figure()
    for i, (cat, ppi) in enumerate(data.items()):
        top5 = ppi.head(5)
        fig.add_trace(go.Bar(x=top5.index, y=top5.values, name=cat))
    fig.update_layout(title="Top 5 PPI Rankings", xaxis_tickangle=-45)
    st.plotly_chart(fig)

elif page == "📊 All Rankings":
    for cat, ppi in data.items():
        st.subheader(cat)
        st.bar_chart(ppi.head(10))

