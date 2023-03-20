from datetime import datetime
import regex as re
import string
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
 
def clean_time(time):
    split_time = re.split(r"T", time)
    date = split_time[0]
    time = re.split(r".000Z", split_time[1])
    d_t = date + " " + time[0]
    # d_t = d_t.translate(str.maketrans('', '', string.punctuation))
    return d_t

# Function to convert string to datetime
def convert(date_time):
    cleaned_time = clean_time(date_time)
    # format = '%Y-%m-%d %H:%M:%S'  # The format
    # datetime_str = datetime.strptime(cleaned_time, format)
    # final = int(datetime_str.strftime("%Y%m%d%H%M%S"))
    return cleaned_time
 
 
# Driver code
df = pd.read_csv('identity_review/history.csv')

# this line will gather all the accounts that current address is sending money to
# df = df.loc[df['from_address'].str.contains('0x098B716B8Aaf21512996dC57EB0615e2383E2f96'.lower())]

x = []

for index, row in df.iterrows():
    x.append(convert(row['block_timestamp']))
    print(row['block_timestamp'])

df['block_timestamp'] = x



# for index, row in df.iterrows():
#     temp = []
#     temp.append(row['value'])
#     d_t = convert(row['block_timestamp'])
#     temp.append(d_t)
#     x.append(temp)

# clf = LocalOutlierFactor(n_neighbors=7, algorithm='auto', metric="cityblock", novelty=True, contamination=0.5).fit(x)

# df['LOC'] = clf.predict(x)

df.to_csv('identity_review/cleaned_time_history.csv')



# next need to figure out how to turn date time into an apporiate integer

# still deciding if this would be a good

# it basically just says if there if value > 0 it is an outlier

# another step I can take is looking at the median value of the data and finding outliers that way
# need to look at literature going forward to get a better understand, and so that i'm not blindly pushing forward

#random graph model based on some varaibles