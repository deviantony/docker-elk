#!/usr/bin/env python3



"""
Utility functions
"""

import pandas


def save_data_to_csv(data_dict, index='date'):
    for k, v in data_dict.items():
        dfs = []
        for d in v:
            # convert series to frame if necessary
            if type(d) == pandas.Series:
                d = pandas.DataFrame(d)

#            # set the index
#            d.set_index('date', inplace=True)
            if d.empty:
                continue

            dfs.append(d)

        try:
            # combine dataframes
            df_concat = pandas.concat(dfs, axis=1)

            df_concat.to_csv(k)

            print(f'--> data saved to: {k}')
        except ValueError as e:
            print(f'Warning: looks like there is some data missing! {e}')
            print(f'Attempted to save this dict to csv: {data_dict}')


def subset_by_date(dat, st, et, date_column='date'):

    if type(dat) == pandas.DataFrame:

        # select dates between start/end range
        mask = (dat[date_column] >= st) & (dat[date_column] <= et)
        dat = dat.loc[mask]
        return dat

    elif type(dat) == pandas.Series:

        # select dates between start/end range
        mask = (dat.index >= st) & (dat.index <= et)
        return dat.loc[mask]

