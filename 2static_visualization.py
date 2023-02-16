"""
Author: Grishma Bhattarai

Code Function: 
    Creates static timeseries (2000-2020) trend plot for any chosen indicator 
    for any chosen list of countries. 
    
    We specifically create 2 using the flexible funCtion:
        1. Time series line graph of Temperature Change for Afghanistan, Nepal, China
        Bangladesh and India (2001-2020).
        2. Time series line graph of CPI for Finland, France and Germany 
        (2001-2020).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# change this according to your directory
base_path = r'/Users/happyfeet/Documents/GitHub/final-project-finalproject_climate_inflation'
df_final_path = os.path.join(base_path, 'clean data/df_final.csv')

df_final = pd.read_csv(df_final_path)
df_final['year'] = df_final['year'].astype(str)



##--time series plot generation------------------------------------------------

def indicator_trends(variable, countries ,label, title, image_path):
    """
    Plots the chosen variable/indicator by date (2001-2020) for a specific 
    country for trend observation.
    Inputs:
        variable (string) : variable for y-axis
                            (eg. CPI, GDPDeflator, TempChange)
        countries (list): list of countries whose trends the 
                            user wantes to observe
        label (string): y-axis label 
        title (string): plot title
        image_path (string): path including file name for saving the plot
    Output: time-series plot
    """
    sns.set_style('whitegrid')
    plt.rcParams.update({'font.size': 13})
    fig, ax = plt.subplots(figsize=(18,10))
    sns.lineplot(data=df_final[df_final['name'].isin(countries)], x='year',
                 y=variable, hue='name')
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.set_ylabel(label)
    ax.legend(loc='best')
    fig.savefig(image_path)
    plt.show()

static_plot1_path = os.path.join(base_path, 'figures/static_plot1.png')
static_plot2_path = os.path.join(base_path, 'figures/static_plot2.png')

#------------------------------------------------------------------------------

# call the function to display and sabe the plots
indicator_trends('TempChange', ['Afghanistan', 'Nepal', 'China', 'Bangladesh', 'India'],
                 'Temperature Change from Previous Year in Degree Celcius', 
                 'Trends of Temperature Change from 2001-2020', static_plot1_path)

indicator_trends('CPI', ['Finland', 'France', 'Germany'],
                 'CPI (2010=100)', 
                 'Consumer Price Index (CPI) from 2001-2020', static_plot2_path)
