import pandas as pd
import datetime
import numpy as np


print("Reading sentiment data")

sentiment_data_itg = pd.read_excel("Twitter Data with Sentiment.xlsx")
sentiment_data_itg["Date"] = pd.to_datetime(sentiment_data_itg["Date"], format= "%m/%d/%Y")

relevant_data = sentiment_data_itg[["User", "Date", "Sentiment"]]



print("Done")


tweet_with_fav = {}
fav_data = pd.read_excel("Data from Twitter NV Favorites.xlsx")
for index, row in fav_data.iterrows():
    tweet_with_fav[row["User"] + row["Text"]] = row["favorites"]

favorites = []
for index, row in sentiment_data_itg.iterrows():
    if (row["User"] + row["Text Spanish"]) in tweet_with_fav:
        favorites.append(tweet_with_fav[row["User"] + row["Text Spanish"]])
    else:
        favorites.append(None)

relevant_data["Favs"] = favorites


sentiment_data_itg = pd.DataFrame(sentiment_data_itg[sentiment_data_itg.columns.values[9:]]).apply(pd.to_numeric)

relevant_data["Program"] = sentiment_data_itg.idxmax(axis = 1)
relevant_data["Week"] = relevant_data["Date"].dt.week


relevant_data.to_csv("sentiment_TWT_data.csv")