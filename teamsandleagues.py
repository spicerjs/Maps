# -*- coding: utf-8 -*-
#Streamlit run filename.py
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


st.title('Predicted League Outcomes')

###read in csv file to be called leagueoutcomes
df = pd.read_csv('Teams.csv', sep=',')
df.TitleProb = np.where(df.TitleProb == 0, np.nan, df.TitleProb)

dfmap = pd.read_csv('Map.csv', sep=',')
DEFAULT_CTRY = dfmap[dfmap.importance == dfmap.importance.max()]['Country'].values[0]

st.sidebar.header('Choose League')

dfmap = df[['Country', 'Tier', 'Position']]
dfmap = dfmap[dfmap.Position == 1]
#dfmap.Country = np.where(dfmap.Country == 'Columbia', 'Colombia', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'England', 'uk', dfmap.Country)
#dfmap.Country = np.where(dfmap.Country == 'Nth America', 'USA', dfmap.Country)
dfmap.Country = np.where(dfmap.Country == 'S Africa', 'South Africa', dfmap.Country)

data = dict(type = 'choropleth',
            locations = dfmap.Country,
            locationmode = 'country names',
            colorscale= 'Portland',
       #     color=dfmap.Tier,
            z=dfmap.Tier,
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

df = df.sort_values(by='Rating', ascending=False)
df = df.reset_index(drop=True) 
df.index = df.index+1
df = df[df.Position >= 1]

dfmap.Country = np.where(dfmap.Country ==  'uk', 'England',dfmap.Country)

sorted_unique_country = sorted(dfmap.Country.unique()) 
DEFAULT = sorted_unique_country.index(DEFAULT_CTRY)
selected_country = st.sidebar.radio('Country', sorted_unique_country, index = DEFAULT)

df = df[df.Country == selected_country].sort_values(by='Tier', ascending=True)
unique_league = df.League.unique()
st.header(selected_country)
selected_league = st.selectbox('League', unique_league)

df = df[df.League == selected_league]
df = df.sort_values(by='Position', ascending=True)
df.ExpPts = df.ExpPts.map('{:.1f}'.format)
st.table(df[['Team', 'GP', 'Pts', 'Diff', 'ExpPts', 'MaxPts', 'TitleProb']].style.format({"TitleProb": lambda x: '' if pd.isnull(x) else "{:.0%}".format(x)}))


st.write()
st.write(f"[Team ratings](https://worldteamratings.herokuapp.com#).")
st.write()
st.write(f"[Big games this coming week](https://sixpointers.herokuapp.com#).")
st.write()         
st.write(f"[https://elosports.wordpress.com/about/](https://elosports.wordpress.com/about/#).")

#st.sidebar  