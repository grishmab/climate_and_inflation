# Data and Programming for Public Policy II - Python Programming
# PPHA 30538

## Author: Grishma Bhattarai

### Final Project: Reproducible Research
### Research Question: Is Climate Change a Key Driver of Inflation"
### Autumn 2022
### Name of the Project Repository: datasci-harris/final-project-finalproject_climate_inflation

----------------------
<img src="https://www.occupy.com/sites/default/files/styles/slide_narrow/public/field/image/planet_money.jpg?itok=m0Weuayi" width="700" height="350">

**FILE ORGANIZATION:**
- *Writeup.pdf*: Final writeup of the project.
- **raw data**:  A directory containing any raw data that was manually downloaded.
  - *faostat.csv*: CSV file containing per year temperature change data from 2001 to 2020 for all countries (source: Food and Agriculture Organization Database).
- **clean data**: A directory containing the final dataset created after merging different necessary datasets and cleaning them.
  - *df_final.csv*
- **figures**: A directory containing all final figures.
  - *static_plot1.png*: Time series line graph of Temperature Change for Afghanistan, Nepal, China, Bangladesh and India (2001-2020).
  - *static_plot2.png*: Time series line graph of CPI for Finland, France and Germany (2001-2020).
  - *shiny_plot1.png*
  - *shiny_plot2.png*
  - *shiny_webpage.png*
  - *nlp_plot1.png*: A WordCloud of all hashtags associated with a specific hashtag (here, ‘#inflation’). 
  - *nlp_plot2.png*: A bar chart of the hashtags and their frequency of use (threshold = 3 or more occurrence).
  - *nlp_plot3.png*: A network graph of the hashtags associated with ‘#inflation’ with lines connecting hashtags that co-occur.
  - *nlp_plot4.png*: A CIRCULAR network graph of the hashtags associated with ‘#inflation’ with lines connecting hashtags that co-occur (flattened out version of *nlp_plot3.png* for convenience). 
  - *regression1.png*
  - *regression2.png*
  - *regression3.png*
  - *regression4.png*
- *1extraction_and_wrangling.py*
  - Extracts, merges, and cleans all necessary data:
    - Datasets on Inflation (proxy: Consumer Price Index and GDP Deflator) using the WORLD BANK API.
    - Manually downloaded dataset on Climate Change (proxy: temperature change per year from the FAO website (faostat.csv).
    - World Country-Level Shapefile using GEOPANDAS.
    - TWITTER data (tweets) to analyze word distribution and network around the hashtag ‘inflation’.
- *2static_visualization.py* 
  - Creates static time-series (2000-2020) trend plot for any chosen indicator for any chosen list of countries. 
- *3shiny_visualization.py*
  - Creates 2 dynamic, interactive plots and projects them in a Shiny application web page.
- *4NLP_tweets.py*
  - Creates a WordCloud, hashtag frequency bar plot and hashtag network plots for a chosen hashtag (here, ‘#inflation’).
- *5regression_analysis.py*
  - Runs multiple regression models:
    - Simple OLS of Inflation (CPI) on Climate Change (TempChange)
    - Simple OLS of Inflation (GDPDeflator) on Climate Change (TempChange)
    - Fixed Effects Regression of Inflation (CPI) on Climate Change (TempChange)
    - Fixed Effects Regression of Inflation (GDPDeflator) on Climate Change (TempChange)
----------------------

**RELEVANCE:** 

Currently, climate change isn’t viewed as a major contributing factor for high prices, but as severe weather events increase in frequency and devastate industries that contribute to the world economy, experts warn it increasingly will be if temperatures keep rising. Severe weather events, like hurricanes, wildfires and droughts, devastate entire communities while costing billions to rebuild. It also affects industry, from energy to transportation and agriculture, leading to a significant rise in food costs for millions. A lot of literature focuses on the microeconomic implications of climate change. However, with this project, I aim to look at the macroeconomic implications of climate change (re: inflation). Specifically, ‘Is Climate Change a Key Driver of Inflation?’ is the research question I am focusing on. 

**PROJECT SUMMARY:** 

In order to attempt to answer this substantial question, I decided to use temperature change from previous year to current year for each year from 2001 to 2020 as a proxy for climate change. Likewise, I decided to use both Consumer Price Index (CPI) and GDP deflator from 2001 to 2020 as proxies for inflation. I used WorldBank API to download the CPI and GDP deflator data while I manually downloaded the temperature change data from the FAO database. I then proceeded to merge these indicators along with shapefile data on world geography because I needed this specific geometry for one of my visualizations. During the cleaning, one of the major issues I faced removing the ISO codes of countries that were not supported by the WorldBank API from the ISO list I had curated. Due to this, I ended up having only 124 countries in my final dataset. Another significant issue I faced was dealing with missing values. Because I was going to be conducting fixed-effects regression analysis in the later part of my project, I needed to find a way to impute those missing values. For this, I explored the data distribution of each indicator, and realized that there were significant outliers. Thus, I decided to replace the missing values by the median of those indicators for each specific country. After meticulous exploration of each variable and proper cleaning and imputation, I finally prepared a clean dataset. With this dataset, I created 2 detailed static plots using matplotlib/seaborn and 2 detailed dynamic plots projected in a Shiny application. 

One of the main focuses of my final project however, was the Natural Language Processing (NLP) portion. For this part of the final project, I decided to go beyond the scope of what was taught this quarter to try to analyze tweet hashtags around the word ‘#inflation’. For this, I executed a Twitter search using application key and application secret Twitter credentials. After conducting the search, I stored a list of found hashtags from tweets containing our main hashtag ‘#inflation’. I also stored a list of list, one for each tweet of the hashtags in that tweet. Finally, I created a dictionary mapping hashtags to an occurrence count. With these 3 different data objects, I then proceeded to create meticulous visualizations. I created a WordCloud to try to understand other hashtags associated with ‘#inflation. I also created a bar plot of most occurring hashtags to see which hashtags were linked the most when people tweeted about inflation. Finally, I used a preprocessor called a Transaction Encoder to create array of tweet-hashtags occurrences and co-occurrences, to finally visualize them as text networks. This network plot displayed all the hashtags associated with ‘#inflation’ with lines connecting hashtags that co-occurred. My main reason for investigating these hashtags/tweets through visualization was to understand if the public also associated inflation with climate change. We know that sometimes academia seems to be a bit disconnected from the real life. Therefore, I wanted to check if the growing literature on climate change’s impact on prices aligned with public views. From the visualizations, it was very clear that a lot of public discourse around inflation as seen through the tweets, was political and did not really focus on climate change or global warming—an interesting digression from what growing peer-reviewed literature is suggesting. Insights aside, purely looking at the code too, the extracted NLP data is extremely dynamic in the sense that the tweets are scoured and the hashtags are extracted in real time every time the code is executed. Therefore, outputs may be different every time the code is executed based on real time. Moreover, the data extraction process takes the hashtag we want to explore as an argument. Therefore, in that sense, the data extraction of the tweets (1extraction_and_wrangling.py) and all the visualizations that follow (nlp_tweets.py) are both scalable and portable-- the user can use the same files to explore any other hashtag than the one I chose for the objective of this project ('#inflation'). 

Finally, for the regression analysis, I decided to implement four models: simple OLS of CPI on temperature change, simple OLS of GDP deflator on temperature change, fixed-effects regression of CPI on temperature change, and, fixed-effects regression of GDP deflator on temperature change. I implemented the two simple OLS simply to understand baseline numbers for the problem. From these two OLS regressions, it was clear that CPI was a better proxy for inflation which produced statistically significant results when compared to the GDP deflator. I then chose to exploit the fact that we had managed to create panel data to perform a fixed-effects regression to avoid issues of omitted variable bias. Therefore, the fixed-effects regression models were used to estimate the effect of intrinsic characteristics of countries within our panel data set. The result of arguably one of the better regression models shoed that the coefficient of temperature change is positive and statistically significant. We can interpret it as an increase in change in temperature per year by a degree Celsius will lead to a 26.55 units increase in Consumer Price Index, which is huge! However, this might be due to other omitted variables that vary over time that introduce the bias. Nonetheless, with all 4 regressions, we do see that global rise in temperature runs simultaneous to global increase in prices—the causality of this relationship however, is definitely questionable. Note that the specifications of all four regressions are purposefully parsimonious i.e. I purposefully decided to not use any controls to avoid bias associated with “bad controls” (or over-controlling). This is because many of the determinants of growth, typically included in standard growth regressions (for example, institutional quality, educational achievement, policies, and so forth), may themselves be shaped by weather shocks and are thus not part of the baseline estimation (Faccia et al., 2021). Of course, to the extent that these are time-invariant and country-specific, they are incorporated in the country fixed effects. 
No research is perfect and the same is the case for this project. Our dataset has annual frequency, however, according the insights of Colacito et al. (2019), it is difficult to assess the impact of temperature anomalies using annual data. For example, extreme summer and winter temperatures could average out throughout the year. Moreover, hot summers and mild winters may have opposite effects on economic activity. The latter could also hold for prices. Therefore, a future avenue for this project could be to look at quarterly data rather than annual data. Other possible avenues would be to try to collect data points on all nations, and spend more time to produce more representative/exhaustive regression models. However, since this was a coding-heavy project, I shifted my focus specifically on writing codes that are functional, portable and scalable. 

----------------------
**REFERENCE:**  

1. Riccardo Colacito, Bridget Hoffmann, and Toan Phan. Temperature and growth: a panel analysis of the United
States. Journal of Money, Credit and Banking, 51(2-3):313–368, 2019.

2. Faccia, D, M Parker and L Stracca (2021), “Feeling the heat:  extreme temperatures and price stability”, ECB
Working Paper, forthcoming.



