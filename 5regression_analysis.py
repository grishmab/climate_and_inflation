"""
Author: Grishma Bhattarai

Code Function: 
    Runs multiple regression models:
        1. Simple OLS of Inflation (CPI) on Climate Change (TempChange)
        2. Simple OLS of Inflation (GDPDeflator) on Climate Change (TempChange)
        3. Fixed Effects Regression of Inflation (CPI) on Climate Change (TempChange)
        4. Fixed Effects Regression of Inflation (GDPDeflator) on Climate 
                                                            Change (TempChange)
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# change this according to your directory
base_path = r'/Users/happyfeet/Documents/GitHub/final-project-finalproject_climate_inflation'
df_final_path = os.path.join(base_path, 'clean data/df_final.csv')

df_final = pd.read_csv(df_final_path)

df_final.info()

def regression_model(dependent, independent, image_path):
    '''
    Models the specified variables (OLS) and saves the output as image in the 
    specified image_path.
    '''
    model = sm.OLS(dependent, independent).fit()
    fig, ax = plt.subplots(figsize=(8,5))
    ax.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, 
            fontproperties = 'monospace') # monospace to deal w/ line-shifts
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(image_path)
    plt.show()
    
#-- Regression 1: Simple OLS CPI~TempChange -----------------------------------

# model
regression1_path = os.path.join(base_path, 'figures/regression1.png')
regression_model(df_final.CPI, df_final.TempChange, regression1_path)

#------------------------------------------------------------------------------

#-- Regression 2: Simple OLS GDPDeflator~TempChange ---------------------------

# model
regression2_path = os.path.join(base_path, 'figures/regression2.png')
regression_model(df_final.GDPDeflator, df_final.TempChange, regression2_path)

#------------------------------------------------------------------------------

#-- Regression 3: Fixed Effects CPI~TempChange --------------------------------

# copy final df as df_demean to calculate demeaned variables
df_demean = df_final.copy()

# calculate the country mean for consumer price index
df_demean['mean_cpi_bycountry'] = df_demean.groupby('name').CPI.transform(np.mean)

# calculate the country mean for precipitation
df_demean['mean_tempchange_bycountry'] = df_demean.groupby('name').TempChange.transform(np.mean)

# demean, subtract each row by the entity-mean
df_demean['TempChange'] = df_demean['TempChange'] - df_demean['mean_tempchange_bycountry']
df_demean['CPI'] = df_demean['CPI'] - df_demean['mean_cpi_bycountry']

# model
regression3_path = os.path.join(base_path, 'figures/regression3.png')
regression_model(df_demean.CPI, df_demean.TempChange, regression3_path)

#------------------------------------------------------------------------------

#-- Regression 4: Fixed Effects GDPDeflator~TempChange ------------------------

# calculate the country mean for gdp deflator
df_demean['mean_gdpdeflator_bycountry'] = df_demean.groupby('name').GDPDeflator.transform(np.mean)

# demean, subtract each row by the entity-mean
df_demean['GDPDeflator'] = df_demean['GDPDeflator'] - df_demean['mean_gdpdeflator_bycountry']

# model 
regression4_path = os.path.join(base_path, 'figures/regression4.png')
regression_model(df_demean.GDPDeflator, df_demean.TempChange, regression4_path)

#------------------------------------------------------------------------------





