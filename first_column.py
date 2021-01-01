import pandas as pd
import datetime
import numpy as np

time_data = pd.read_excel("TVRxTimeBand.xlsx")
time_data["Date"] = pd.to_datetime(time_data['Date'], format="%d.%m.%Y")
dates_in_db = set(time_data["Date"])
columns = time_data.columns.values
start_ind = 4
date_objects = [i.split(" - ") for i in columns[4:]]
format = "%H:%M:%S"
date_objects = [(datetime.datetime.strptime(i[0], format), datetime.datetime.strptime(i[1], format)) for i in date_objects]


main_data = pd.read_excel("Programs_FV.xlsx")
main_data["Date"] = pd.to_datetime(main_data["Date"], format = "%Y-%m-%d %H:%M:%S")
main_data['time'] = pd.to_datetime(main_data['Start time'].astype(str)) + pd.to_timedelta("00:15:00")


data = {"Program": [], "TVR_TimeBand":[], "Total_ITG_Interactions": [], "Total_Twi_Interations": [],
        "Influencers_Twitter_user":[], "Influencers_Twitter_post":[], "Influencers_Twitter_interaction":[],"Influencers_Twitter_followers":[],
        "Influencers_Instagram_user":[], "Influencers_Instagram_post":[], "Influencers_Instagram_interaction":[], "Influencers_Instagram_followers":[]}


interaction_data = pd.read_excel("Interactions_Total.xlsx")
program_interactions = {}
for index, row in interaction_data.iterrows():
    if (row["Program"].strip().lower()) not in program_interactions:
        program_interactions[row["Program"].strip().lower()] = {0: None, 1: None}
    program_interactions[row["Program"].strip().lower()][row["SMI"]] = row["Interactions"]



influencers_data_twt = pd.read_excel("Influencers_Total_new.xlsx")
program_twt_influence = {}
for index,row in influencers_data_twt.iterrows():
    if (row["Program"].strip().lower()) not in program_twt_influence:
        program_twt_influence[row["Program"].strip().lower()] = {"User": 0, "Interactions": 0, "Posts":0, "Followers": 0}
    program_twt_influence[row["Program"].strip().lower()]["User"] += 1
    program_twt_influence[row["Program"].strip().lower()]["Interactions"] += row["Interactions"]
    program_twt_influence[row["Program"].strip().lower()]["Posts"] += row["Posts"]
    program_twt_influence[row["Program"].strip().lower()]["Followers"] += row["Followers"]


influencers_data_itg = pd.read_excel("Influencers_Total_Instagram_new.xlsx")
program_itg_influence = {}
for index,row in influencers_data_itg.iterrows():
    if (row["Program"].strip().lower()) not in program_itg_influence:
        program_itg_influence[row["Program"].strip().lower()] = {"User": 0, "Interactions": 0, "Posts":0, "Followers": 0}
    program_itg_influence[row["Program"].strip().lower()]["User"] += 1
    program_itg_influence[row["Program"].strip().lower()]["Interactions"] += row["Interactions"]
    program_itg_influence[row["Program"].strip().lower()]["Posts"] += row["Posts"]
    if not np.isnan(row["Followers"]):
        program_itg_influence[row["Program"].strip().lower()]["Followers"] += row["Followers"]

promotions_data = pd.read_excel("Promotions.xlsx")
promotions_per_program = {}
for index, row in promotions_data.iterrows():
    if (row["Program"].strip().lower()) not in promotions_per_program:
        promotions_per_program[row["Program"].strip().lower()] = dict()
    promotions_per_program[row["Program"].strip().lower()][row["Week"]] = [row["Insertions"], row["GRP abs."], row["Reach"], row["OTS"]]

data["Insertions"], data["GRP abs."], data["Reach"], data["OTS"] = [],[],[],[]

program_hashtags = pd.read_excel("Programs IDs.xlsx")
hashtag_to_program = {}
for index, row in program_hashtags.iterrows():
    hashtags = [i.strip().lower() for i in row["Hashtag"].split(",") + row["HashColumn"].split(",")]
    for i in hashtags:
        if i not in hashtag_to_program:
            hashtag_to_program[i] = (row["Programa"].strip().lower())

print(hashtag_to_program)
sentiment_count_ITG = {}
senitment_data_itg = pd.read_csv("sentiment_ITG_data.csv")
for index, row in senitment_data_itg.iterrows():
    program_name = hashtag_to_program.get(row["Program"].strip().lower(), '').strip().lower()
    week_num = row["Week"]
    sentiment = row["Sentiment_main"] if type(row["Sentiment_main"]) == str else row["Sentiment"]
    likes = row["Like Count"]
    if program_name not in sentiment_count_ITG:
        sentiment_count_ITG[program_name] = dict()

    if week_num not in sentiment_count_ITG[program_name]:
        sentiment_count_ITG[program_name][week_num] = {"Positive" : 0, "Negative": 0, "Neutral": 0, "Likes": 0}
    if type(sentiment) == str:
        sentiment_count_ITG[program_name][week_num][sentiment] += 1
    if not np.isnan(likes):
        sentiment_count_ITG[program_name][week_num]["Likes"] += likes

data["Ins_Pos"], data["Ins_Neg"], data["Ins_Neu"], data["Likes"] = [],[],[], []

sentiment_count_TWT = {}
senitment_data_twt = pd.read_csv("sentiment_TWT_data.csv")
for index, row in senitment_data_twt.iterrows():
    program_name = hashtag_to_program.get(row["Program"].strip().lower(), '').strip().lower()
    week_num = row["Week"]
    sentiment = row["Sentiment"]
    likes = row["Favs"]
    if program_name not in sentiment_count_TWT:
        sentiment_count_TWT[program_name] = dict()
    if week_num not in sentiment_count_TWT[program_name]:
        sentiment_count_TWT[program_name][week_num] = {"Positive" : 0, "Negative": 0, "Neutral": 0, "Favs": 0}
    if type(sentiment) == str:
        sentiment_count_TWT[program_name][week_num][sentiment] += 1
    if not np.isnan(likes):
        sentiment_count_TWT[program_name][week_num]["Favs"] += likes

data["Twi_Pos"], data["Twi_Neg"], data["Twi_Neu"], data["Favorites"] = [],[],[], []
data["Tot_Pos"] = []
data["Tot_Neg"] = []
data["Tot_Neu"] = []

for index, row in main_data.iterrows():
    iter_num = 0
    selected_column = start_ind
    for start, end in date_objects:
        if row["time"].time() >= start.time() and row["time"].time() < end.time():
            selected_column += iter_num
            iter_num += 1

    data["TVR_TimeBand"].append(time_data[time_data["Date"] == row["Date"]][columns[selected_column]].values[0])

    if (row["Program"].strip().lower() in program_interactions):
        data["Total_Twi_Interations"].append(program_interactions[row["Program"].strip().lower()][0])
        data["Total_ITG_Interactions"].append(program_interactions[row["Program"].strip().lower()][1])

    data["Program"].append(row["Program"])


    if (row["Program"].strip().lower() in program_twt_influence):
        data["Influencers_Twitter_user"].append((program_twt_influence[row["Program"].strip().lower()]["User"]))
        data["Influencers_Twitter_post"].append((program_twt_influence[row["Program"].strip().lower()]["Posts"]))
        data["Influencers_Twitter_interaction"].append((program_twt_influence[row["Program"].strip().lower()]["Interactions"]))
        data["Influencers_Twitter_followers"].append(round(
            (program_twt_influence[row["Program"].strip().lower()]["Followers"])))
    else:
        data["Influencers_Twitter_user"].append(None)
        data["Influencers_Twitter_post"].append(None)
        data["Influencers_Twitter_interaction"].append(None)
        data["Influencers_Twitter_followers"].append(None)
        
    if (row["Program"].strip().lower() in program_itg_influence):
        data["Influencers_Instagram_user"].append((program_itg_influence[row["Program"].strip().lower()]["User"]))
        data["Influencers_Instagram_post"].append((program_itg_influence[row["Program"].strip().lower()]["Posts"]))
        data["Influencers_Instagram_interaction"].append((program_itg_influence[row["Program"].strip().lower()]["Interactions"]))
        data["Influencers_Instagram_followers"].append(round(
            (program_itg_influence[row["Program"].strip().lower()]["Followers"])))
    else:
        data["Influencers_Instagram_user"].append(None)
        data["Influencers_Instagram_post"].append(None)
        data["Influencers_Instagram_interaction"].append(None)
        data["Influencers_Instagram_followers"].append(None)

    if (row["Program"].strip().lower() in promotions_per_program and row["Week"] in promotions_per_program[row["Program"].strip().lower()]):
        data["Insertions"].append(promotions_per_program[row["Program"].strip().lower()][row["Week"]][0])
        data["GRP abs."].append(promotions_per_program[row["Program"].strip().lower()][row["Week"]][1])
        data["Reach"].append(promotions_per_program[row["Program"].strip().lower()][row["Week"]][2])
        data["OTS"].append(promotions_per_program[row["Program"].strip().lower()][row["Week"]][3])

    else:
        data["Insertions"].append(None)
        data["GRP abs."].append(None)
        data["Reach"].append(None)
        data["OTS"].append(None)

    total_positive = None
    total_negative = None
    total_neutral = None

    if row["Program"].strip().lower() in sentiment_count_ITG and row["Week"] in sentiment_count_ITG[row["Program"].strip().lower()]:
        program_week_data = sentiment_count_ITG[row["Program"].strip().lower()][row["Week"]]
        data["Ins_Pos"].append(program_week_data["Positive"])
        data["Ins_Neg"].append(program_week_data["Negative"])
        data["Ins_Neu"].append(program_week_data["Neutral"])
        data["Likes"].append(program_week_data["Likes"])
        total_positive = program_week_data["Positive"]
        total_negative = program_week_data["Negative"]
        total_neutral = program_week_data["Neutral"]
    else:
        data["Ins_Pos"].append(None)
        data["Ins_Neg"].append(None)
        data["Ins_Neu"].append(None)
        data["Likes"].append(None)

    if row["Program"].strip().lower() in sentiment_count_TWT and row["Week"] in sentiment_count_TWT[row["Program"].strip().lower()]:
        program_week_data = sentiment_count_TWT[row["Program"].strip().lower()][row["Week"]]
        data["Twi_Pos"].append(program_week_data["Positive"])
        data["Twi_Neg"].append(program_week_data["Negative"])
        data["Twi_Neu"].append(program_week_data["Neutral"])
        data["Favorites"].append(program_week_data["Favs"])
        if total_positive is None:
            total_positive = program_week_data["Positive"]
        else:
            total_positive += program_week_data["Positive"]

        if total_negative is None:
            total_negative = program_week_data["Negative"]
        else:
            total_negative += program_week_data["Negative"]

        if total_neutral is None:
            total_neutral = program_week_data["Neutral"]
        else:
            total_neutral += program_week_data["Neutral"]
    else:
        data["Twi_Pos"].append(None)
        data["Twi_Neg"].append(None)
        data["Twi_Neu"].append(None)
        data["Favorites"].append(None)

    data["Tot_Pos"].append(total_positive)
    data["Tot_Neg"].append(total_negative)
    data["Tot_Neu"].append(total_neutral)


#print(set(data["Program"]))


data_df = pd.DataFrame.from_dict(data)
final = pd.concat([main_data, data_df], axis = 1, sort = False)
final.to_csv("final_with_follower.csv")
