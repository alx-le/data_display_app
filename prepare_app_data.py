# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 10:19:26 2021

@author: a-lerf
"""

import pandas as pd
import numpy as np

#load csv files from WorldBank
df_mob = pd.read_csv('data/mob_data.csv')
df_gdp = pd.read_csv('data/gdp_data.csv')

df_mob = df_mob.drop(['Series Name','Series Code'],axis = 1)
df_gdp = df_gdp.drop(['Series Name','Series Code'],axis = 1)

df_mob = df_mob.set_index(['Country Code']).sort_index()
mob_index = df_mob.index
df_gdp = df_gdp.set_index(['Country Code']).sort_index()
gdp_index = df_gdp.index

#compare index and drop index not included in obesity dataset
df_gdp = df_gdp.drop(gdp_index.difference(mob_index))

df_mob = df_mob.reset_index()
df_gdp = df_gdp.reset_index()

df_mob = df_mob.set_index(['Country Code', 'Country Name'])
df_gdp = df_gdp.set_index(['Country Code', 'Country Name'])

def get_year_data(df1,df2,year):
    '''
    method to extract data for a certain year from both datasets
    returns combined DataFrame with obesity and log GDP data for all countries
    for selected year
    '''
    
    year = str(year)
    year_str = year + ' [YR' + year + ']'
    
    df_prep_1 = df1[year_str]
    df_prep_2 = df2[year_str]
    
    df_prep_1 = pd.to_numeric(df_prep_1, errors='coerce')
    df_prep_2 = pd.to_numeric(df_prep_2, errors='coerce')
    
    #new series names
    series_name = ['obesity rate ' + df_prep_1.name[:4], df_prep_1.name[:4] + 'gdp']
    
    #new empty DataFrame to fill with selected year data
    df_out = pd.DataFrame({})
    
    df_out[series_name[0]] = df_prep_1.sort_index()
    df_out[series_name[1]] = df_prep_2.sort_index()
    
    df_out.replace(to_replace = '..', value = np.nan)
    
    #get log of GDP data
    df_out['log gdp ' + year] = np.log(df_out[year + 'gdp'])
    
    #drop GDP data
    df_out = df_out.drop([year + 'gdp'], axis = 1)
    
    return df_out.dropna()


def get_year_country_data(df1, df2):
    '''
    method to create final DataFrame for all years from 1975 to 2016 for app use
    '''
    df_out = pd.DataFrame({})
    
    for yr in range(1975,2017):
        df = get_year_data(df1,df2,yr)
        for col in df.columns:
            df_out[col] = df[col]

    return df_out.dropna()

df_save = get_year_country_data(df_mob,df_gdp)

df_save.to_csv('data/app_data.csv')
