import pandas as pd
import datetime
import numpy as np


user_data = pd.read_excel("Influencers_Total_Instagram_new.xlsx")

print(len(user_data["User Name"]))
program_with_user = set([i.strip().lower() for i in user_data["Program"]])

program_hashtags = pd.read_excel("Programs IDs.xlsx")
programs = set()
hashtag_to_program = {}
for index, row in program_hashtags.iterrows():
    hashtags = [i.strip().lower() for i in row["Hashtag"].split(",") + row["HashColumn"].split(",")]
    for i in hashtags:
        if i not in hashtag_to_program:
            hashtag_to_program[i] = (row["Programa"].strip().lower())
    programs.add(row["Programa"].strip().lower())

print(programs)
programs = (programs.intersection(program_with_user))
print(programs)

twitter_users = set()

twitter_file = pd.read_csv("sentiment_TWT_data.csv")
twitter_data = dict()
for index, row in twitter_file.iterrows():
    program_name = hashtag_to_program.get(row["Program"].strip().lower(), "").strip().lower()
    if program_name not in programs:
        program_name = "Other Programs".strip().lower()
    user_name = row["User"].strip().lower()
    week_num = row["Week"]
    sentiment = row["Sentiment"]
    likes = row["Favs"]
    twitter_users.add(user_name)
    if user_name not in twitter_data:
        twitter_data[user_name] = dict()
    if program_name not in twitter_data[user_name]:
        twitter_data[user_name][program_name] = {"Positive" : 0, "Negative": 0, "Neutral": 0, "Favs": 0}
    if type(sentiment) == str:
        twitter_data[user_name][program_name][sentiment] += 1
    if not np.isnan(likes):
        twitter_data[user_name][program_name]["Favs"] += likes

instagram_users = set()
instagram_file = pd.read_csv("sentiment_ITG_data.csv")
instagram_data = dict()
for index, row in instagram_file.iterrows():
    program_name = hashtag_to_program.get(row["Program"].strip().lower(), "").strip().lower()
    if program_name not in programs:
        program_name = "Other Programs".strip().lower()
    if type(row["User Name"]) != str:
        continue
    user_name = row["User Name"].strip().lower()
    week_num = row["Week"]
    sentiment = row["Sentiment_main"] if type(row["Sentiment_main"]) == str else row["Sentiment"]
    likes = row["Like Count"]
    instagram_users.add(user_name)
    if user_name not in instagram_data:
        instagram_data[user_name] = dict()
    if program_name not in instagram_data[user_name]:
        instagram_data[user_name][program_name] = {"Positive" : 0, "Negative": 0, "Neutral": 0, "Likes": 0}
    if type(sentiment) == str:
        instagram_data[user_name][program_name][sentiment] += 1
    if not np.isnan(likes):
        instagram_data[user_name][program_name]["Likes"] += likes


data = {}
data["Twi_Pos"], data["Twi_Neg"], data["Twi_Neu"], data["Favorites"] = [],[],[], []
data["Ins_Pos"], data["Ins_Neg"], data["Ins_Neu"], data["Likes"] = [],[],[], []
data["Account"] = []

for index, row in user_data.iterrows():
    user_name = row["User Name"].strip().lower()
    program_name = row["Program"].strip().lower()
    #data["User"].append(user_name)
    #data["Program"].append(program_name)

    if user_name in twitter_data and program_name in twitter_data[user_name]:
        data["Twi_Pos"].append(twitter_data[user_name][program_name]["Positive"])
        data["Twi_Neg"].append(twitter_data[user_name][program_name]["Negative"])
        data["Twi_Neu"].append(twitter_data[user_name][program_name]["Neutral"])
        data["Favorites"].append(twitter_data[user_name][program_name]["Favs"])
    else:
        data["Twi_Pos"].append(None)
        data["Twi_Neg"].append(None)
        data["Twi_Neu"].append(None)
        data["Favorites"].append(None)


    if user_name in instagram_data and program_name in instagram_data[user_name]:
        data["Ins_Pos"].append(instagram_data[user_name][program_name]["Positive"])
        data["Ins_Neg"].append(instagram_data[user_name][program_name]["Negative"])
        data["Ins_Neu"].append(instagram_data[user_name][program_name]["Neutral"])
        data["Likes"].append(instagram_data[user_name][program_name]["Likes"])
    else:
        data["Ins_Pos"].append(None)
        data["Ins_Neg"].append(None)
        data["Ins_Neu"].append(None)
        data["Likes"].append(None)


    if user_name not in twitter_users and user_name in instagram_users:
        account = "Instagram"
    elif user_name not in instagram_users and user_name in twitter_users:
        account = "Twitter"
    elif user_name in instagram_users and user_name in twitter_users:
        account = "Both"
    else:
        account = "None"

    data["Account"].append(account)

data_df = pd.DataFrame.from_dict(data)
final = pd.concat([user_data, data_df], axis = 1, sort = False)

final.to_csv("User_Follower_new_instagram.csv")
