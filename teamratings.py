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
import pandas as pd
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
dfmap.Country = np.where(dfmap.Country == 'Columbia', 'Colombia', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'England', 'uk', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'Nth America', 'USA', dfmap.Country)
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


all_tiers_option = ['Yes', 'No']
tiers_option = st.sidebar.selectbox('Only include top division from each country?', all_tiers_option)
if tiers_option == 'Yes':
    df = df[df.Tier == 1]
#    df = df[df.TeamWiki.str.contains("xx") == False]
df = df.sort_values(by='Rating', ascending=False)
df = df.reset_index(drop=True) 
df.index = df.index+1

search_team_option = ['Yes','No']
team_search = st.sidebar.selectbox('Search Team?', search_team_option)
if team_search == 'Yes':
    sorted_unique_country = sorted(df.Country.unique()) 
    selected_country = st.sidebar.selectbox('Country', sorted_unique_country)
    df1 = df[df.Country == selected_country]
    sorted_unique_league = sorted(df1.League.unique())
    if tiers_option != 'Yes':
        selected_league = st.sidebar.selectbox('League', sorted_unique_league)
        df1 = df1[df1.League == selected_league]
    sorted_unique_team = sorted(df1.Team.unique())
    selected_team = st.sidebar.selectbox('Team', sorted_unique_team)
    df.Ranking = df.index.values
    ranking = df.Ranking[df.Team == selected_team].sum()-6
    ranking = max(0,ranking)
    ranking = min(ranking, len(df)-11)
    df = df.sort_values(by='Rating', ascending=False)
    df.Rating = df.Rating.map('{:.3f}'.format)
    st.dataframe(df[['Country', 'League', 'Team', 'Rating']].iloc[ranking:ranking+11])
    

else:
    all_countries = st.sidebar.selectbox('All countries?', search_team_option)
    if all_countries == 'No':
        sorted_unique_country = sorted(df.Country.unique()) 
        selected_country = st.sidebar.selectbox('Country', sorted_unique_country)
        df = df[df.Country == selected_country]
        unique_league = sorted(df.League.unique())
        selected_leagues = st.sidebar.multiselect('Leagues to include', unique_league, unique_league)
        df = df[df.League.isin(selected_leagues)]
 
#    st.header('Team Ratings')
    df.Rating = df.Rating.map('{:.3f}'.format)
    st.dataframe(df[['Country', 'League', 'Team', 'Rating']])

  
st.markdown("""

""")


