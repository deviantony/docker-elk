#!/usr/bin/env python3 

import os
import pytz
import pandas
import argparse
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

import plot
import users
import utilities


user_types = ['Unspecified',
              'Post-Doctoral Fellow',
              'Commercial/Professional',
              'University Faculty',
              'Government Official',
              'University Graduate Student',
              'Professional',
              'University Professional or Research Staff',
              'Local Government',
              'University Undergraduate Student',
              'School Student Kindergarten to 12th Grade',
              'School Teacher Kindergarten to 12th Grade',
              'Other'
              ]


def all(input_directory='.',
        start_time=datetime(2000, 1, 1),
        end_time=datetime(2030, 1, 1),
        exclude=[],
        **kwargs):

    print('--> building user types pie-chart')

    # load the data based on working directory
    df = users.load_data(input_directory)
    df = utilities.subset_by_date(df, start_time, end_time)
    df = df.filter(items=['usr_type'])

    # count number of users for each type
    for u in user_types:
        df[u] = np.where(df['usr_type'] == u, 1, 0)
    df['Other'] = np.where(~df['usr_type'].isin(user_types), 1, 0)

    # remove 'usr_type' b/c it's no longer needed
    df = df.drop('usr_type', axis=1)

    # remove specified columns so they won't be plotted
    for drp in exclude:
        try:
            print('--> not reporting %s: %s users'
                  % (drp, df[drp].sum()))
            df.drop(drp, inplace=True, axis=1)
        except Exception as e:
            print(f'Error dropping from users pie df: {e}')

    # calculate total and percentages for each user type
    ds = df.sum()
    df = pandas.DataFrame({'type': ds.index, 'score': ds.values})
    df = df.set_index('type')
    df['percent'] = round(df['score']/df['score'].sum()*100, 2)

    print('--> total number of users reporting: %d' % df.score.sum())

    for u in user_types:
        if u not in exclude:
            pct = df.loc[u].percent
            df = df.rename({u: '%s (%2.2f%%)' % (u, pct)})

    return plot.PlotObject(None,
                           df.percent,
                           dataframe=df,
                           label='percent')


