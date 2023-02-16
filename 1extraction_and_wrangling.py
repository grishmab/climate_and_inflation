"""
Author: Grishma Bhattarai

Code Function: 
    I. Downloads and merges all necessary data required for the final dataframe.
            Data: 
                1. Datasets on Inflation (proxy: CPI and 
                GDP Deflator using the WORLD BANK API.
                2. Manually downloaded dataset on Climate Change 
                (proxy: global temperature change per year per country from 
                 the FAO website.
                3. World Country-Level Shapefile using GEOPANDAS.
                
    II. Cleans the merged dataset to produce and save a final dataframe.
    
    III. Downloads and saves another set of TWITTER data (tweets) to analyze 
    word distribution and network around the hashtag 'inflation'.
"""


import os
import pandas as pd
import geopandas
from pandas_datareader import wb #world bank api
import pycountry # country names and iso codes
from twython import Twython # tweets data
import json

# change this according to your directory
base_path = r'/Users/happyfeet/Documents/GitHub/final-project-finalproject_climate_inflation'
df_fao_path = os.path.join(base_path, 'raw data/faostat.csv')

##-- data generation ---------------------------------------------------------- 

def iso_generator():
    """
    Generates a list of ISO_3 codes for all countries using the pycountry package,
    then removes codes not supported by the World Bank API. 
    Input: None.
    Output: A list of ISO_3 codes for countries supported by the World Bank API. 
    """
    world_iso = []
    country = []
    for i in list(pycountry.countries):
        code = i.alpha_3
        world_iso.append(code)
        country.append(i)
    # remove list of countries not supported by the World Bank API 
    # (eg. Anguilla, Åland Islands etc.)
    unsupported_iso = {'ABW','AIA','ALA','AND','ASM','ATA','ATF','BES','BLM',
                       'BLZ','BMU','BVT','CCK','COK','CUW','CXR','CYM','ERI',
                       'ESH','FRO','FLK','GGY','GIB','GLP','GRL','GUF','GUM',
                       'HKG','HMD','IMN','IOT','JEY','LIE','MAC','MAF','MCO',
                       'MHL','MNP','MSR','MTQ','MYT','NCL','NFK','NIU','PCN',
                       'NRU','PRI','PSE','PYF','REU','SGS','SHN','SJM','SPM',
                       'SMR','TCA','TKL','TUV','TWN','UMI','UZB','VAT','VGB',
                       'VIR','WLF', 'ARG', 'CUB', 'TKM', 'SOM'}
    final_iso = [ele for ele in world_iso if ele not in unsupported_iso]
    return final_iso


world_iso = iso_generator() # generate iso codes for countries

def final_data_generator(world_iso, variables, labels, start_date, end_date):
    """
    Uses Pandas data reader for the World Bank, manually downloaded dataset 
    from FAO and the Geopandas World features to produce a merged dataset or 
    chosen indicators for all countries specified for a specific time frame. 
    Inputs:
        world_iso (list):A list of 2/3 digit ISO codes for countries.                
        variables (list):A list of World Bank Indicator codes 
                        (eg. ['FP.CPI.TOTL.ZG']).
        labels (list):A list of variable names for the WB Indicator codes selected 
                        (eg. ['inflation']).
        start_date (int):A start date for the data (eg. 2000).
        start_date (int):A end date for the data (eg. 2010).
    Output: Final dataframe with all the necessary data merged 
    (geometry data, FAO data and indicators data from APIs).
    """
    indicators = wb.download(indicator=variables, country=world_iso, 
                             start=start_date, end=end_date)
    indicators = indicators.reset_index(drop=False)
    indicators.columns = ['country', 'year'] + labels
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    # merge geopandas dataframe to WB API dataframe
    world_total = pd.merge(world, indicators, how='inner', left_on='name', 
                           right_on='country', sort=True)
    world_total['year'] = world_total['year'].astype(int)
    world_total = world_total.drop(['pop_est', 'gdp_md_est', 'country'], axis=1)
    # load manually downloaded FAO dataframe
    df_fao = pd.read_csv(df_fao_path)
    df_fao = df_fao.drop(['Domain Code', 'Domain', 'Area Code (M49)', 'Element Code',
                          'Element', 'Months Code', 'Months', 'Year Code', 'Unit', 
                          'Flag', 'Flag Description'], axis=1)
    df_fao = df_fao.rename(columns={'Value': 'TempChange'})
    # merge FAO df to the previously merged df to create a final df
    world_final = pd.merge(world_total, df_fao, how='inner', left_on=['name','year'], 
                           right_on=['Area','Year'], sort=True)
    # drop unnecessary or repetitive columns
    world_final = world_final.drop(['Area', 'Year'], axis=1)
    return world_final

# specify the WB indicator codes and their labels for download
variable = ['FP.CPI.TOTL', 'NY.GDP.DEFL.ZS.AD']
label = ['CPI', 'GDPDeflator']

# produce the final merged df for cleaning
df = final_data_generator(world_iso, variable, label, 2001, 2020)

##-- data cleaning ------------------------------------------------------------ 

# remove scientific notation and round float variables to 3 digits
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df.info()

df.shape

len(df.name.unique())
# we have data for 127 unique countries
# now we look at the data distribution of our indicators to carry on necessary 
# data wrangline/cleaning

df.describe()

# we see some missing values for the indicators
# we also see that the distribution is not normal with presence of significant 
# outliers for all indicators
# hence, we will replace missing values by the median and not the mean 
# for each indicator

# group by country and replace missing values by median value within a country
# for all indicators
df['CPI'] = df.groupby('name')['CPI'].transform(lambda x: x.fillna(x.median()))
df['GDPDeflator'] = df.groupby('name')['GDPDeflator'].transform(lambda x: x.fillna(x.median()))
df['TempChange'] = df.groupby('name')['TempChange'].transform(lambda x: x.fillna(x.median()))

df.isna().sum() # no missing values anymore

# change year from int to object type
df['year'] = df['year'].astype(str)

# export the final df into 'clean data' directory
df_final_path = os.path.join(base_path, 'clean data/df_final.csv')
df.to_csv(df_final_path, index=False, header=True)


##-- TWITTER data generation --------------------------------------------------

def tweet_dissect(key, secret, hashtag):
    """
    Generates 3 objects:  
    1. all hashtags (a list to store the found hashtags, may have repeats)
    2. tweet hashtags (a list of lists, one for each tweet of the hashtags in that tweet)
    3. hashtag counts (a dictionary mapping hashtags to an occurrence count).
    Input: 
        key (string): a key string to access Twitter remotely.
        secret (string): a secret string to access Twitter remotely.
    Output: 3 objects for all hashtags, tweet hashtags and hashtag counts.
    """
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    # execute a twitter search
    # result_type can be 'popular', 'recent' or 'mixed'
    # the max count is 100
    result = twitter.search(q= hashtag, result_type='recent', count=100, lang='en')
    # a list to store the found hashtags, may have repeats
    all_hashtags = []
    # a list of lists, one for each tweet of the hashtags in that tweet
    tweet_hashtags = []
    # a dictionary mapping hashtags to an occurrence count
    hashtag_counts = {}
    # loop over twets
    for tweet in result['statuses']:
        # a list comprhension to pull out a list of hashtags from the tweet
        hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
        # add the hashtag list to our list of hashtag lists
        tweet_hashtags += [hashtags]
        # append the hashtags to our list of the hashtags
        all_hashtags += hashtags
        # increment the appropriate counts for all of the hashtags
        for tag in hashtags:
            if tag in hashtag_counts:
                hashtag_counts[tag] += 1
            else:
                hashtag_counts[tag] = 1
    return all_hashtags, tweet_hashtags, hashtag_counts

# log in using Twitter credentials
APP_KEY = 'xniDYFLSZ1kBv56l4cy84PjLC'
APP_SECRET = 'bAHyEKjs4SciA2WLBGbTnsPXqXgHaAamSK9juJuUG59peX3i9f'
hashtag = '#inflation'

all_hashtags, tweet_hashtags, hashtag_counts = tweet_dissect(APP_KEY, 
                                                             APP_SECRET, hashtag)

# save the 3 objects in as text files or jsons
all_hashtags_path = os.path.join(base_path, 'clean data/all_hashtags.txt')
tweet_hashtags_path = os.path.join(base_path, 'clean data/tweet_hashtags.txt')
hashtag_counts_path = os.path.join(base_path, 'clean data/hashtag_counts.txt')

with open(all_hashtags_path, 'w') as f:
    for hashtag in all_hashtags:
        f.write(f"{hashtag},")
        
with open(tweet_hashtags_path, 'w') as f2:
    f2.write(json.dumps(tweet_hashtags))
        
with open(hashtag_counts_path, 'w') as f3:
    f3.write(json.dumps(hashtag_counts))
    
f.close()
f2.close()
f3.close()


