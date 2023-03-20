import pandas as pd
import os


def get_csvs(path):
    list_df = []
    list_files = os.listdir(path)

    path_list = [path + item for item in list_files if item != '.DS_Store']
    path_list.sort()
    for item in path_list:
        print(item)
        temp_df = pd.read_csv(item, low_memory=False)
        temp_df.dropna(how='all')
        list_df.append(temp_df)
    final = pd.concat(list_df, ignore_index=True)
    return final


def combine_df_network(path):
    df = get_csvs(path)

    final = df.loc[df['Engagement Type'].str.contains('RETWEET|QUOTE', case=False, na=False)]
    final = final[['Author', 'Thread Author', 'Engagement Type', 'Thread Created Date']]
    # final = final.loc[final['Thread Created Date'].str.contains('-11-|-10-| ', case=False, na=False)]
    final = final.drop_duplicates()
    
    freq_table_frequency1 = final.groupby(['Author', 'Thread Author', 'Engagement Type']).size().reset_index(name="frequency")
    freq_table_frequency1 = freq_table_frequency1.iloc[0:60000]
    freq_table_frequency1 = freq_table_frequency1.sort_values(by="frequency", ascending=False, ignore_index=True)
    freq_table_frequency1.to_csv('dominion_voting/output/attr_network.csv')

    freq_table_frequency2 = final.groupby(['Author', 'Thread Author']).size().reset_index(name="frequency")
    freq_table_frequency2 = freq_table_frequency2.sort_values(by="frequency", ascending=False, ignore_index=True)
    freq_table_frequency2 = freq_table_frequency2.iloc[0:60000]
    freq_table_frequency2['Type'] = "Directed"
    freq_table_frequency2.rename(
        columns={"Thread Author": "Source",
                "Author": "Target",
                 "frequency": "Weight",
                 "Type": "Type"},
                 inplace=True)
    
    freq_table_frequency2 = freq_table_frequency2[["Source", "Target", "Weight", "Type"]]

    freq_table_frequency2.to_csv('dominion_voting/output/dominion_gephi_network.csv')




path = 'dominion_voting/data/'

df = combine_df_network(path)