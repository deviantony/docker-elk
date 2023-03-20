#!/usr/bin/env python

"""
The purpose of this script is to provide a general method for summarizing
HydroShare user actions. The report generation tool has a number of specific
functions such as 'download_actions' and 'app_app_actions' that can be
generalized. This file aims to do that.
"""

import os
import pandas
import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class PlotObject(object):
    def __init__(self, x, y, label='', style='-', color=None):
        self.x = x
        self.y = y
        self.label = label
        self.style = style
        self.color = color

def load_data(workingdir, pickle_file='activity.pkl'):

    # load the activity data
    path = os.path.join(workingdir, pickle_file)
    df = pandas.read_pickle(path)

    # convert dates
    df['date'] = pandas.to_datetime(df.session_timestamp) \
                       .dt.normalize()

    # add another date column and make it the index
    df['Date'] = df['date']

    # change the index to timestamp
    df.set_index(['Date'], inplace=True)

    return df


