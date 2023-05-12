import pandas as pd
from NEAT_get_transaction import get_transaction_history
import pickle
import os
import numpy as np
import sklearn


def _get_avg_trans_per_day(df):
    months = [*set(df['month'])]
    days = [*set(df['day'])]
    day_by_day = [len(df.loc[df['block_timestamp'].str.contains(r'(?:(?:(-?(0){}|-{}))-(?:(-?(0){}|-{})))'.format(month, month, day, day), case=False, na=False)]) for month in months for day in days]
    day_by_day = [val for val in day_by_day if val > 0]
    return sum(day_by_day) / len(day_by_day)

temp = get_transaction_history('0cbQY37AJB0TsoX86tgDuH3ewDiKGmfRgDtpFOTJ1fRtKP3OeC5UWfrniT1yW9dq', '0xa3e59061cc89be9cabcd5af44d8033905dddcb0e')

print(_get_avg_trans_per_day(temp))




