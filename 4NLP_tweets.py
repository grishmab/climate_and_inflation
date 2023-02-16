"""
Author: Grishma Bhattarai

Code Function: 
    NLP Visualizations-- Creates a wordcloud, hashtag frequency plot and 
    hashtag network plots for a chosen hashtag (here, '#inflation). 
"""

import os
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
import networkx as nx # text network visualization
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS # wordcloud visualization
import json

# change this according to your directory
base_path = r'/Users/happyfeet/Documents/GitHub/final-project-finalproject_climate_inflation'
all_hashtags_path = os.path.join(base_path, 'clean data/all_hashtags.txt')
tweet_hashtags_path = os.path.join(base_path, 'clean data/tweet_hashtags.txt')
hashtag_counts_path = os.path.join(base_path, 'clean data/hashtag_counts.txt')


# read text files/jsons as objects (list, list of lists, dictionary)

# object 1: all_hashtags-- a list to store the found hashtags for a word,
                        # may have repeats
all_hashtags_file = open(all_hashtags_path, "r")
all_hashtags_data = all_hashtags_file.read()
all_hashtags = all_hashtags_data.split(",")
all_hashtags_file.close()

# object 2: tweet_hashtags-- a list of lists, one for each tweet of the hashtags 
                            # in that tweet
tweet_hashtags_file = open(tweet_hashtags_path, "r")
tweet_hashtags_data = tweet_hashtags_file.read()
tweet_hashtags = json.loads(tweet_hashtags_data)
tweet_hashtags_file.close()

# object 3: hashtag_counts-- a dictionary mapping hashtags to an occurrence count
hashtag_counts_file = open(hashtag_counts_path, "r")
hashtag_counts_data = hashtag_counts_file.read()
hashtag_counts = json.loads(hashtag_counts_data)
hashtag_counts_file.close()

#------------------------------------------------------------------------------

# create a word cloud from the list of hash tags
# note: this twitter data generates on real time so your output may be 
# different than when I executed it
fig, ax = plt.subplots(figsize=(14,12))
cloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=1200, 
                  height=1000).generate(' '.join(list(all_hashtags)))                                                                                                    
ax.imshow(cloud)
ax.axis('off')
nlp_plot1_path = os.path.join(base_path, 'figures/nlp_plot1.png')
fig.savefig(nlp_plot1_path)
plt.show()

#------------------------------------------------------------------------------

# a bar chart of the hashtags and their frequency of use 
        # (threshold = 3 or more occurences):
hashtag_counts_series = pd.Series(hashtag_counts)
maxoccurence = hashtag_counts_series[hashtag_counts_series>3]

fig, ax = plt.subplots(figsize=(10,9))
maxoccurence.plot.bar(colormap='summer')
ax.set_ylabel("Frequency")
ax.set_xlabel("Hashtags")
ax.set_title("Most Occuring Hashtags")
nlp_plot2_path = os.path.join(base_path, 'figures/nlp_plot2.png')
fig.savefig(nlp_plot2_path)
plt.show()

#------------------------------------------------------------------------------

# next, make a dataframe out of the list of lists that has the hashtags in each tweet
# use a preprocessor called a Transaction Encoder to create a binary 2d array
# in the binary 2d array, rows are tweets and columns are a hashtags with 1's 
# if that hashtag occurred in that tweet and 0 if not
te = TransactionEncoder()
occurrences = te.fit(tweet_hashtags).transform(tweet_hashtags).astype("uint8")

# turn that 2d array into a dataframe with the column names
occurrences_df = pd.DataFrame(occurrences, columns=te.columns_)

# from that 2d array of hashtag occurrences, create a co-occurrence matrix
# rows and columns are a particular hashtag and the value is how many times
# those hashtags co-occurred (note that the diagonals simply contain the 
# number of times that hashtag occurred)
co_occurrences = occurrences.T.dot(occurrences)

# turn that co-occurrence matrix into a dataframe with labels
co_occurrences_df = pd.DataFrame(co_occurrences, index=te.columns_, 
                                 columns=te.columns_)
labels = { k:te.columns_[k] for k in range(len(te.columns_)) }

# finally, plot a network graph of the hashtags with lines connecting hashtags 
# that co-occur:
fig, ax = plt.subplots(figsize=(18,25))
g1 = nx.Graph(co_occurrences)
nx.draw_kamada_kawai(g1, labels=labels, with_labels=True, 
                     node_color='lightgreen', font_size=20)
nlp_plot3_path = os.path.join(base_path, 'figures/nlp_plot3.png')
fig.savefig(nlp_plot3_path)

# since the plot is a little cluttered, we flatten out the previous graph into a 
# more circu;ar network of hashtags
fig, ax = plt.subplots(figsize=(18,25))
g2 = nx.Graph(co_occurrences)
nx.draw_circular(g2, labels=labels, with_labels=True, 
                 node_color='lightgreen', font_size=20)
nlp_plot4_path = os.path.join(base_path, 'figures/nlp_plot4.png')
fig.savefig(nlp_plot4_path)
