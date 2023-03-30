import pandas as pd

df = pd.read_csv('dominion_voting/output/attempt.csv', low_memory=False)
df = df.drop_duplicates()

def get_amount_of_time(df, start, end, month):
    list_of_df = []
    while start <= end:
        print(start)
        temp = df.loc[df['Date'].str.contains('{}/{}/'.format(month, start), case=False, na=False)]
        list_of_df.append(temp)
        start = start + 1
    final = pd.concat(list_of_df, ignore_index=True)
    return final

week = get_amount_of_time(df, 1, 30, 11)


def create_edge_list(df):
    final = df.loc[df['Engagement Type'].str.contains('RETWEET|QUOTE', case=False, na=False)]
    final = final[['Author', 'Thread Author', 'Engagement Type', 'Thread Created Date']]

    freq_table_frequency2 = final.groupby(['Author', 'Thread Author']).size().reset_index(name="frequency")
    freq_table_frequency2 = freq_table_frequency2.sort_values(by="frequency", ascending=False, ignore_index=True)
    freq_table_frequency2['Type'] = 'Directed'
    freq_table_frequency2.rename(
        columns={"Thread Author": 'Source', "Author": 'Target', "frequency": 'Weight', "Type": 'Type'}, inplace=True)
    freq_table_frequency2.to_csv('dominion_voting/week_edge_list/edgelist_{}_to_{}.csv'.format(df['Date'][0].replace("/", "_"), df['Date'][len(df) - 1].replace("/", "_")), index = False)
    
create_edge_list(week)
