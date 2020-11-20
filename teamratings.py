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
import random
import plotly as pl
import plotly.graph_objs as gobj
import pandas as pd
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)


import requests
from io import StringIO

# define parameters for a request
token = '06f4689d01a62991c554d4b5b623a81194ef32e0' 
owner = 'spicerjs'
repo = 'Six-pointers'
path = 'Teams.csv'

# send a request
r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
    owner=owner, repo=repo, path=path),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(token)
            }
    )
# convert string to StringIO object
string_io_obj = StringIO(r.text)
# Load data to df
df = pd.read_csv(string_io_obj, sep=",")

#Reading in the Map file
path = 'Map.csv'
r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
    owner=owner, repo=repo, path=path),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(token)
            }
    )
string_io_obj = StringIO(r.text)
dfmap = pd.read_csv(string_io_obj, sep=",")

st.title('Team Ratings')

###read in csv file to be called leagueoutcomes
df['League'].fillna(0, inplace=True)
df.Tier = df.Tier.astype(int)
df['League'] = np.where(df['League']==0, df.Country.astype(str) + ' ' + df.Tier.astype(str), df['League'])

st.sidebar.header('Teams and leagues to include')
  
dfmap = df[['Country', 'Tier', 'Position', 'Rating']]
dfmap.Country = np.where(dfmap.Country == 'S Korea', 'South Korea', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'N Korea', 'North Korea', dfmap.Country)

def top(ratings, column, n):
    return ratings.sort_values(by=column, ascending=False)[:n]    #function for identifying country's best n teams
dfmap = dfmap.groupby('Country').apply(top, column='Rating', n=8)[['Rating']]
dfmap = dfmap.groupby('Country').mean()
dfmap['Country'] = dfmap.index

#dfmap.Country = np.where(dfmap.Country == 'England', 'uk', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'Dominican Rep', 'Dominican Republic', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'DRCongo', 'Democratic Republic of the Congo', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'Eswatini', 'eSwatini', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'Luxemburg', 'Luxembourg', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'N Ireland', 'Northern Ireland', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'N Macedonia', 'Macedonia', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'Surinam', 'Suriname', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'S Africa', 'South Africa', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'Switz', 'Switzerland', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'UAE', 'United Arab Emirates', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'USA', 'United States', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'Uzbek', 'Uzbekistan', dfmap.Country)



#####import cartopy
#####import cartopy.io.shapereader as shpreader
import geopandas as gpd
import json
import fiona

path = 'leaguesmap.shp'

# send a request
r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
    owner=owner, repo=repo, path=path),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(token)
            }
    )
# convert string to StringIO object
#string_io_obj = StringIO(r.text)
#leaguesmap = gpd.read_file(string_io_obj, sep=",")
leaguesmap = gpd.read_file(r)



#####shpfilename = cartopy.io.shapereader.natural_earth( \
  #####resolution='50m', \
  #####category='cultural', \
  #####name='admin_0_map_units')

#####leaguesmap = gpd.read_file(shpfilename)

#Countries we don't want divided into separate parts
#####leaguesmap = leaguesmap[['SOVEREIGNT', 'SUBUNIT', 'geometry']]
#####leaguesmap = leaguesmap[leaguesmap.SOVEREIGNT != 'Belgium']
#####leaguesmap = leaguesmap[leaguesmap.SOVEREIGNT != 'Bosnia and Herzegovina']
#####leaguesmap = leaguesmap[leaguesmap.SOVEREIGNT != 'Portugal']
#####leaguesmap = leaguesmap[leaguesmap.SOVEREIGNT != 'Republic of Serbia']

#Map of Sovereign nations
#####shpfilename1 = cartopy.io.shapereader.natural_earth( \
  #####resolution='50m', \
  #####category='cultural', \
  #####name='admin_0_countries')

#####countries = gpd.read_file(shpfilename1)
#####countries = countries[['SOVEREIGNT', 'SUBUNIT', 'geometry']]
#whole country outlines we want to add back in
#####countries = countries[
     #####         (countries['SOVEREIGNT'] == "Belgium")
          #####    | (countries['SOVEREIGNT'] == "Bosnia and Herzegovina")
     #####         | (countries['SOVEREIGNT'] == "Portugal")
     #####         | (countries['SOVEREIGNT'] == "Republic of Serbia")
     #####         ] 
#####leaguesmap = pd.concat([leaguesmap, countries])


#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'Hong Kong S.A.R.', 'Hong Kong', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'Macao S.A.R', 'Macao', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'Czechia', 'Czech Rep', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'Bosnia and Herzegovina', 'Bosnia', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'Republic of Serbia', 'Serbia', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'Cabo Verde', 'Cape Verde', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'West Bank', 'Palestine', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'RÃ©union', 'Reunion', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'SÃ£o TomÃ© and Principe', 'Sao Tome and Principe', leaguesmap.SUBUNIT )
#####leaguesmap.SUBUNIT = np.where(leaguesmap.SUBUNIT == 'CuraÃ§ao', 'Curacao', leaguesmap.SUBUNIT )

#####leaguesmap = leaguesmap[['SUBUNIT', 'geometry']]
leaguesmap_json = json.loads(leaguesmap.to_json())

dfmap.Rating = round(dfmap.Rating, 2)

import plotly.express as px
# Choropleth representing the length of region names
fig = px.choropleth(data_frame=dfmap, 
                    geojson=leaguesmap_json, 
                    locations='Country', # name of dataframe column
                    featureidkey='properties.SUBUNIT',  # path to field in GeoJSON feature object with which to match the values passed in to locations
            #        featureidkey='properties.SUBUNIT',  # path to field in GeoJSON feature object with which to match the values passed in to locations
                    color='Rating',
                    color_continuous_scale="greens",
                   )

fig.update_geos(showcountries=True, showcoastlines=True, showland=True)#, fitbounds="locations")
fig.update(layout_coloraxis_showscale=False)
fig.update_layout(width=300, height= 150, margin={"r":0,"t":0,"l":0,"b":0})
st.sidebar.plotly_chart(fig)



DEFAULT_CTRY = df[df.Rating == df.Rating.max()]['Country'].values[0]

tiers_option = st.sidebar.checkbox('Exclude lower tier leagues', value=False) 
if tiers_option:
    df = df[df.Tier == 1]
df = df.sort_values(by='Rating', ascending=False)
df = df.reset_index(drop=True) 
df.index = df.index+1

sorted_unique_country = sorted(df.Country.unique()) 
DEFAULT = sorted_unique_country.index(DEFAULT_CTRY)

single_country = st.sidebar.checkbox('Only show teams from chosen country', value=False) 
if single_country:
    selected_country = st.selectbox('Country', sorted_unique_country, index = DEFAULT)
    df = df[df.Country == selected_country]
#   st.write('Just teams from')
    df.Rating = df.Rating.map('{:.3f}'.format)
    st.dataframe(df[['Team', 'Rating', 'Country', 'League']])

else:    
    team_search = st.sidebar.checkbox('Search for a team?', value=False) 
    if team_search:
        selected_country = st.selectbox('Country', sorted_unique_country, index = DEFAULT)
        df1 = df[df.Country == selected_country].sort_values(by='Tier', ascending=True)
        sorted_unique_team = sorted(df1.Team.unique())
        TOP_TEAM = df1[df1.Rating == df1.Rating.max()]['Team'].values[0]
        DEFAULT_TEAM = sorted_unique_team.index(TOP_TEAM)
        selected_team = st.selectbox('Team', sorted_unique_team, index=DEFAULT_TEAM)
        df.Ranking = df.index.values
        ranking = df.Ranking[df.Team == selected_team].sum()-6
        ranking = max(0,ranking)
        ranking = min(ranking, len(df)-11)
        df = df.sort_values(by='Rating', ascending=False)
        df.Rating = df.Rating.map('{:.3f}'.format)
        st.dataframe(df[['Team', 'Rating', 'Country', 'League']].iloc[ranking:ranking+11])
    
    
    else:
        df.Rating = df.Rating.map('{:.3f}'.format)
        st.dataframe(df[['Team', 'Rating', 'Country', 'League']])

 
    
    

st.write()
st.write(f"[Expected league finishes](https://world-league-predict.herokuapp.com#).")
st.write()
st.write(f"[Big games this coming week](https://sixpointers.herokuapp.com#).")
st.write()         
st.write(f"[https://elosports.wordpress.com/about/](https://elosports.wordpress.com/about/#).")
