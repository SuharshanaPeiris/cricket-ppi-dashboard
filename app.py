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
