# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# In this notebook we use the new Sunburst plot by [plotly](http://plot.ly/) to illustrate how the World population is splitted among regions and countries. The data set illustrated here originates from the [World Bank](https://data.worldbank.org).

# +
import numpy as np
import pandas as pd
import urllib
import mock
import plotly.offline as offline
import plotly.graph_objs as go

# Head and tail of data frames
pd.set_option('display.max_rows', 6)

# Patch plotly.py to use the latest plotly.js
url = 'https://cdn.plot.ly/plotly-latest.min.js'

def plotly_latest():
    return urllib.request.urlopen(url).read().decode('utf-8')

with mock.patch('plotly.offline.offline.get_plotlyjs', plotly_latest):
    offline.init_notebook_mode()
# -

# Country and associated regions
import world_bank_data as wb
countries = wb.get_countries()
countries

# Population dataset, by the World Bank (most recent value)
population = wb.get_series('SP.POP.TOTL', mrv=1)
population

# Same data set, indexed with the country code
population = wb.get_series('SP.POP.TOTL', labels=False, mrv=1)
population.index = population.index.droplevel('series').droplevel('year')
population

# Aggregate region, country and population
df = countries[['region', 'name']].rename(columns={'name':'country'}).loc[countries.region!='Aggregates']
df['population'] = population
df

# +
# The sunburst plot requires weights (values), labels, and parent (region, or World)
# We build the corresponding table here
columns = ['parents', 'labels', 'values']

level1 = df.copy()
level1.columns = columns
level1['text'] = level1['values'].apply(lambda pop:'{:,.0f}'.format(pop))

level2 = df.groupby('region').population.sum().reset_index()[['region', 'region', 'population']]
level2.columns = columns
level2['parents'] = 'World'
# move value to text for this level
level2['text'] = level2['values'].apply(lambda pop:'{:,.0f}'.format(pop))
level2['values'] = 0

all_levels = pd.concat([level1, level2], axis=0).reset_index(drop=True)
all_levels
# -

# And now we can plot the World Population
offline.iplot(dict(
    data = [dict(type='sunburst', **all_levels, hoverinfo='text')],
    layout = dict(title='World Population (World Bank, 2017)<br>Click on a region to zoom',
                  width=800, height=800)),
              validate=False)
