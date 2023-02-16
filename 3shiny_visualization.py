"""
Author: Grishma Bhattarai

Code Function: 
    Creates shiny application for 2 dynamic visualizations.
    
"""

from shiny import App, render, ui
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas 
import os

# change this according to your directory
base_path = r'/Users/happyfeet/Documents/GitHub/final-project-finalproject_climate_inflation'
df_final_path = os.path.join(base_path, 'clean data/df_final.csv')

df_final = pd.read_csv(df_final_path)
#df_final['year'] = df_final['year'].astype(str)
# geometry-type changes into string--type when being imported from a saved df
# therefore, change the GEOPANDAS column from object to geometry-type first
df_final['geometry'] = geopandas.GeoSeries.from_wkt(df_final['geometry'])
df_final = geopandas.GeoDataFrame(df_final, geometry='geometry')






# user interface design
app_ui = ui.page_fluid(
    ui.row(ui.column(12, ui.h2('Is Climate Chnage a Driver of Inflation?'), 
                     ui.hr(),
                     align='center')),
    ui.row(ui.column(10, ui.h5(ui.em('Final Project Dynamic Visualizations')),
                     offset=1,
                     align='center')),
    ui.row(ui.column(4, ui.input_radio_buttons('variable', 
                                               'Indicators', 
                                               choices=['CPI',
                                                       'GDPDeflator',
                                                       'TempChange']),
                     offset=1,
                     align='center'),
           ui.column(4, ui.input_slider('slider1', 'GeoPlot Year', value=2010,
                                               min=2001, max=2020, sep=''),
                     offset=2,
                     align='center')),
    ui.row(ui.column(12, ui.output_plot('geoplot'),
                     align='center')),
    ui.row(ui.column(4, ui.input_select('variable2', 
                                               'Relationship', 
                                               choices=['CPI vs. Temperature Change',
                                                        'GDP Deflator vs. Temperature Change']),
                     offset=1,
                     align='center'),
           ui.column(4, ui.input_slider('slider2', 'ScatterPlot Year', value=2012,
                                               min=2001, max=2020, sep=''),
                     offset=2,
                     align='center')),
    ui.row(ui.column(12, ui.output_plot('scatterplot'),
                     align='center'))
)

#------------------------------------------------------------------------------

# server design
def server(input, output, session):
     
        
    @output
    @render.plot
    def geoplot():
        # issues with returning a geoplot object through multiple functions, hence, data
        # extraction and plotting are both in once function
        df_final = pd.read_csv(df_final_path)
        #df_final['year'] = df_final['year'].astype(str)
        
        # geometry-type changes into string--type when being imported from a saved df
        # therefore, change the GEOPANDAS column from object to geometry-type first
        df_final['geometry'] = geopandas.GeoSeries.from_wkt(df_final['geometry'])
        df_final = geopandas.GeoDataFrame(df_final, geometry='geometry')            
        if input.variable() == 'CPI': #color change for inflation and co2 emissions
            color = 'YlOrRd'
        elif input.variable() == 'GDPDeflator':
            color = 'PuBuGn'
        else:
           color = 'YlGnBu'
        fig, ax = plt.subplots(figsize=(16,16))
        # locatable axes for the geoplot
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.1)
        df_subset = df_final[df_final['year'] == input.slider1()]
        ax = df_subset.plot(ax=ax, column=input.variable(), legend=True,
                            cax=cax, cmap=color)
        ax.axis('off')
        # dynamic plot title based on input indicator and year
        ax.set_title(f"Global GeoPlot of {input.variable()} for Year {input.slider1()}") 
        return ax
    
    
    @output
    @render.plot
    def scatterplot():
        df_final = pd.read_csv(df_final_path)
        df_subset = df_final[df_final['year'] == input.slider2()]
        fig, ax = plt.subplots(figsize=(10,8))
        if input.variable2() == 'CPI vs. Temperature Change': 
            sns.scatterplot(data=df_subset, x='CPI', y='TempChange', 
                            hue='continent')
            ax.set_xlabel('CPI (2010=100)')
            ax.set_ylabel('TempChange (Degree Celcius)')
        else:
           sns.scatterplot(data=df_subset, x='GDPDeflator', y='TempChange', 
                           hue='continent')
           ax.set_xlabel('GDP Deflator (2010=100)')
           ax.set_ylabel('TempChange (Degree Celcius)')
        # dynamic plot title based on input indicator and year
        ax.set_title(f"Scatterplot of {input.variable2()} for Year {input.slider2()}")
        return ax
    
#------------------------------------------------------------------------------    

# final app object 
app = App(app_ui, server)
