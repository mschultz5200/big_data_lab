import time
from datetime import datetime
import regex as re
import pandas as pd
from moralis import evm_api
import json
import string

def clean_time(time):
    split_time = re.split(r"T", time)
    date = split_time[0]
    time = re.split(r".000Z", split_time[1])
    d_t = date + " " + time[0]
    return d_t

# Function to convert string to datetime
def convert(date_time):
    cleaned_time = clean_time(date_time)
    format = '%Y-%m-%d %H:%M:%S'  # The format
    datetime_str = datetime.strptime(cleaned_time, format)
    return datetime_str

def get_elapsed_time(df):
    time_elapsed = []
    day = []
    hour = []
    for index, row in df.iterrows():
        if index == 0: 
            time_elapsed.append(0)
            day.append(convert(row['block_timestamp']).day)
            hour.append(convert(row['block_timestamp']).hour)
        else:
            temp = convert(df.iloc[index]['block_timestamp']) - convert(df.iloc[index - 1]['block_timestamp'])
            final = int(temp.total_seconds())
            time_elapsed.append(final)
            day.append(convert(row['block_timestamp']).day)
            hour.append(convert(row['block_timestamp']).hour)
    return time_elapsed, day, hour
 

def td_itf(combined_table):
    combined_table['frequency'] = combined_table['frequency'].div(sum(combined_table['frequency']))
    combined_table['value'] = combined_table['value'].div(sum(combined_table['value']))
    
    combined_table['weight'] = [(row['value'] + (1/row['frequency'])) / 10 for index, row in combined_table.iterrows()]
    combined_table = combined_table.loc[combined_table['weight'] > 1.0]
    print(combined_table)


def start_weights(df):
    freq_table_frequency = df.groupby(['from_address', 'to_address']).size().reset_index(name="frequency")
    freq_table_value = df.groupby(['from_address', 'to_address']).sum().reset_index()
    combined_table = pd.merge(freq_table_frequency, freq_table_value)
   

def create_data_frame(results, address):

    results['value'] = results['value'].div(10 ** 18)

    new_df = results[['to_address', 'from_address', 'value', 'gas', 'block_timestamp']]

    new_df = new_df.loc[::-1].reset_index()

    time_between, hour, day = get_elapsed_time(new_df)
    new_df['time_b/w_trans'] = time_between
    new_df['day'] = day
    new_df['hour'] = hour

    type_of_trans = []
    for index, row in new_df.iterrows():
        if row['to_address'] == address.lower():
            type_of_trans.append(0)
        else:
            type_of_trans.append(1)
    
    new_df['type_of_trans'] = type_of_trans
    return new_df


def call_api(api_key, address, cursor):
    if cursor == '':
        params = {
            "address": address, 
            "chain": "eth",
        }
    else: 
        params = {
            "address": address, 
            "chain": "eth",
            'cursor': cursor,
        }

    result = evm_api.transaction.get_wallet_transactions(
        api_key=api_key,
        params=params,
    )
    final_json = json.dumps(result['result'], indent=4, sort_keys=True)

    temp_df = pd.read_json(final_json)
    previous_cursor = result['cursor']

    return temp_df, previous_cursor


def get_transaction_history(api_key, address):
    list_of_histories = []
    previous_cursor = ""
    nextCursor = True
    index = 0
    
    while nextCursor:
        print(index)
        if previous_cursor == "":
           
           temp, previous_cursor = call_api(api_key, address, previous_cursor)
           list_of_histories.append(temp)

           if previous_cursor == None:
               nextCursor = False
        else:
            temp, previous_cursor = call_api(api_key, address, previous_cursor)
            list_of_histories.append(temp)

            if previous_cursor == None:
                nextCursor = False
        
        index = index + 1

    df = create_data_frame(pd.concat(list_of_histories, ignore_index=True), address)
    df.to_csv('identity_review/csv_output/single_wallet_history/history_{}.csv'.format(address))
    

def main():
    api_key = '5M47SltcWwM6LG4DjNisTcSdNs175YsOUePfgmVKqYSAOFxPRaPaD2VRF4H4V4SH'
    address = '0x6162759eDAd730152F0dF8115c698a42E666157F'
    get_transaction_history(api_key, address)



if __name__ == "__main__":
    main()


# number of transaction 
# temporal random graph models, 
# looking at the number of out degrees
# looking at the inference first