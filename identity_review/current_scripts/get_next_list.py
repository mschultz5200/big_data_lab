import pandas as pd
from NEAT_get_transaction import get_transaction_history
import pickle
import os
import sklearn

df = pd.read_csv('identity_review/csv_output/single_wallet_history/history_0x098b716b8aaf21512996dc57eb0615e2383e2f96.csv')

df = df.loc[df['malicious'] == 1].reset_index()
df = df.iloc[5:,3:].reset_index()

wallets = df['to_address'].to_list()
wallets = list(dict.fromkeys(wallets))

for wallet in wallets:
    temp = get_transaction_history('5M47SltcWwM6LG4DjNisTcSdNs175YsOUePfgmVKqYSAOFxPRaPaD2VRF4H4V4SH', wallet)
