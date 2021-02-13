# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:19:55 2021

@author: a-lerf
"""

import streamlit as st
import numpy as np
import pandas as pd


@st.cache(persist = True)
def load_data():
    '''
    load data from the prepared csv, see prepare_app_data.py
    returns a DataFrame
    '''
    data = pd.read_csv('data/app_data.csv', index_col = 0)
    
    return data.reset_index()

def plot_data(df, year, country):
    '''
    method to extract data for a specific country and years 
    and add new columns for selected country and years variables
    retuns a figure to plot in streamlit
    '''
    
    df_out = df.set_index(['Country Code'])
    
    #select column names for selected years
    column_names = ['obesity rate ' + year[0], 'log gdp ' + year[0],
                    'obesity rate ' + year[1], 'log gdp ' + year[1]]
    
    df_out = df_out[column_names]
    
    #create new columns for selected country and fill old columns with np.nan
    for c in df_out.columns:
        df_out[c + ' ' + country] = np.nan
        df_out[c + ' ' + country].loc[country] = df_out[c].loc[country]
        df_out[c].loc[country] = np.nan
        
    df_out = df_out.reset_index()    
    
    #plot all points for selected country and rest of the world
    ax = df_out.plot(kind = 'scatter', x = df_out.columns[3],
                      y = df_out.columns[4], color = 'b', label = 'World ' + year[0])
    df_out.plot(kind = 'scatter', x = df_out.columns[7], 
                y = df_out.columns[8], color = 'r', ax = ax, label = country + ' ' + year[0])
    df_out.plot(kind = 'scatter', x = df_out.columns[1], 
                y = df_out.columns[2], color = 'DarkBlue', ax = ax, label = 'World ' + year[1])
    df_out.plot(kind = 'scatter', x = df_out.columns[5], 
                y = df_out.columns[6], color = 'DarkOrange', ax = ax, label = country + ' ' + year[1])
    
    ax.set_xlabel("Obesity rates for male adults")
    ax.set_ylabel("log GDP")
    ax.legend(loc='center left',bbox_to_anchor=(1.0, 0.8));
    
    
    return ax.get_figure()

df = load_data()

#create lists for country names, country codes and years for 
#selection in the app 
country_list = [c for c in df['Country Name']]
tag_list = [t for t in df['Country Code']]
year_list = [yr[-4:] for yr in [y for y in df.columns[2:]]][::2]
country_dict = dict(zip(country_list,tag_list))

#create streamlit elements on main page
st.title('Male Obesity Rates vs Log GDP')

#sidebar for settings with selectboxes for years and country
st.sidebar.title('Settings')
left_column, right_column = st.sidebar.beta_columns(2)
year_one_selectbox = left_column.selectbox('Year one',(year_list))
year_two_selectbox = right_column.selectbox('Year two',(year_list[1:]))
country_selectbox = st.sidebar.selectbox('Please choose a country',(country_list))

#button press starts data preparation and plots figure if selected years
#are not the same
if st.sidebar.button('Show scatterplot'):
    if year_one_selectbox == year_two_selectbox:
        st.write('Please choose two different years!')
    else:
        st.write('Plot for ' + country_selectbox + ' in ' + year_one_selectbox  + 
                 ' and ' +  year_two_selectbox)
        df_plot = plot_data(df, [year_one_selectbox, year_two_selectbox], 
                                country_dict[country_selectbox])
    
        st.pyplot(df_plot)
    