# -*- coding: utf-8 -*-
#streamlit run filename.py
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Team Ratings')

###read in csv file to be called leagueoutcomes
df = pd.read_csv('Teams.csv', sep=',')


st.sidebar.header('User Input Features')

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
    st.write(selected_team + ' is ' + str(ranking))
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
    st.dataframe(df[['Country', 'League', 'Team', 'Rating']])
  
st.markdown("""
The coverage of leagues is global but not completely comprehensive.
In Europe and South America, top two leagues (and sometimes additional tiers) in all UEFA/Comnebol countries except Andorra, Bolivia, Faroe Islands, Gibraltar, Kosova, Luxembourg and San Marino where only top league included.  
Elsewhere, top two tiers for Costa Rica and Mexico, China, Hong Kong, Indonesia, Iran, Japan, Malaysia, Qatar, Saudi Arabia, South Korea, UAE, and Vietnam, and Algeria, Morocco, South Africa, and Tunisia.
""")



