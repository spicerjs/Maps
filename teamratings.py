# -*- coding: utf-8 -*-
#streamlit run filename.py
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd
import base64
import numpy as np
import plotly as pl
import plotly.graph_objs as gobj
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)

st.title('Team Ratings')

###read in csv file to be called leagueoutcomes
df = pd.read_csv('Teams.csv', sep=',')

df['League'].fillna(0, inplace=True)
df['League'] = np.where(df['League']==0, df.Country.astype(str) + ' ' + df.Tier.astype(str), df['League'])

st.sidebar.header('Teams and leagues to include')
  

dfmap = df[['Country', 'Position']]
dfmap.Details = np.where(dfmap.Position == 1, 1, 2)
dfmap.Details = np.where(dfmap.Position == '', 3, dfmap.Details)
#dfmap.Country = np.where(dfmap.Country == 'Columbia', 'Colombia', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'England', 'uk', dfmap.Country)
#dfmap.Country = np.where(dfmap.Country == 'Nth America', 'USA', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'S Africa', 'South Africa', dfmap.Country)


data = dict(type = 'choropleth',
            locations = dfmap.Country,
            locationmode = 'country names',
            colorscale= 'Portland',
            z=dfmap.Details,
            showscale = False,
            )
#initializing the layout variable
layout = dict(geo = {'scope':'world'}, 
              width=1000, height= 150,
              margin=dict( l=0, r=0, b=0, t=0, pad=12, autoexpand=True ))

# Initializing the Figure object by passing data and layout as arguments.
col_map = gobj.Figure(data = [data],layout = layout)

#plotting the map
iplot(col_map) 
st.sidebar.plotly_chart(col_map, use_container_width=True)


DEFAULT_CTRY = df[df.Rating == df.Rating.max()]['Country'].values[0]

tiers_option = st.sidebar.checkbox('Exclude lower tier leagues', value=False) 
if tiers_option:
    df = df[df.Tier == 1]
df = df.sort_values(by='Rating', ascending=False)
df = df.reset_index(drop=True) 
df.index = df.index+1

team_search = st.sidebar.checkbox('Only show teams from chosen country', value=False) 
if team_search:
    sorted_unique_country = sorted(df.Country.unique()) 
    DEFAULT = sorted_unique_country.index(DEFAULT_CTRY)
    selected_country = st.sidebar.selectbox('Country', sorted_unique_country, index = DEFAULT)
    df = df[df.Country == selected_country]
    unique_league = sorted(df.League.unique())
    selected_leagues = st.sidebar.multiselect('Leagues to include', unique_league, unique_league)
    df = df[df.League.isin(selected_leagues)]#
    df.Rating = df.Rating.map('{:.3f}'.format)
    st.dataframe(df[['Country', 'League', 'Team', 'Rating']])

else:
    sorted_unique_country = sorted(df.Country.unique()) 
    DEFAULT = sorted_unique_country.index(DEFAULT_CTRY)
    selected_country = st.sidebar.selectbox('Country', sorted_unique_country, index = DEFAULT)
    df1 = df[df.Country == selected_country].sort_values(by='Tier', ascending=True)
    sorted_unique_league = df1.League.unique()
    if tiers_option != 'Yes':
        selected_league = st.sidebar.selectbox('League', sorted_unique_league)
        df1 = df1[df1.League == selected_league]
    sorted_unique_team = sorted(df1.Team.unique())
    TOP_TEAM = df1[df1.Rating == df1.Rating.max()]['Team'].values[0]
    DEFAULT_TEAM = sorted_unique_team.index(TOP_TEAM)
    selected_team = st.sidebar.selectbox('Team', sorted_unique_team, index=DEFAULT_TEAM)
    df.Ranking = df.index.values
    ranking = df.Ranking[df.Team == selected_team].sum()-6
    ranking = max(0,ranking)
    ranking = min(ranking, len(df)-11)
    df = df.sort_values(by='Rating', ascending=False)
    df.Rating = df.Rating.map('{:.3f}'.format)
    st.dataframe(df[['Country', 'League', 'Team', 'Rating']].iloc[ranking:ranking+11])
    

st.write()
st.write(f"[Expected league finishes](https://world-league-predict.herokuapp.com#).")
st.write()
st.write(f"[Big games this coming week](https://sixpointers.herokuapp.com#).")
st.write()         
st.write(f"[https://elosports.wordpress.com/about/](https://elosports.wordpress.com/about/#).")

