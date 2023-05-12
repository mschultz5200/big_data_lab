import pandas as pd
from NEAT_get_transaction import get_transaction_history

df = pd.read_csv('identity_review/csv_output/single_wallet_history/history_0x098b716b8aaf21512996dc57eb0615e2383e2f96.csv')

df = df.loc[df['malicious'] == 1].reset_index()

wallets = df['to_address'].to_list()
wallets = list(dict.fromkeys(wallets))
print(wallets[23])

waiting = []
list_of_dfs = []
index = 0



for i in range(len(wallets)):
    print(wallets[i])
    print(len(wallets))
    temp = get_transaction_history('5M47SltcWwM6LG4DjNisTcSdNs175YsOUePfgmVKqYSAOFxPRaPaD2VRF4H4V4SH', wallets[i])
    list_of_dfs.append(temp)
    new_wallets = list(dict.fromkeys(temp['to_address'].to_list()))
    waiting.append(new_wallets)
    wallets.pop(i)

    if i == len(wallets) - 1:
        flatten_list = lambda irregular_list:[element for item in irregular_list for element in flatten_list(item)] if type(irregular_list) is list else [irregular_list]
        waiting = flatten_list(waiting)
        wallets = waiting
        index = index + 1
        print(index)
    
    if index == 5:
        print("done")
        break



final = pd.concat(list_of_dfs, ignore_index=True)
final.to_csv('identity_review/csv_output/network_spread.csv', index=None)
    



