#!/usr/bin/env python3

import os
import pandas
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def all_issues(df, dirname):

    # select unique issue numbers to remove duplicates caused by
    # issues having multiple labels
    df_unique = df.drop_duplicates('number')

    # group by date
    df_dt = df_unique.groupby(pandas.Grouper(key='created_dt', freq='W')) \
                     .count().cumsum()

    # create a figure to summarize technical debt
    fig = plt.figure()
    ax = plt.gca()
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel('issue count')
    plt.xlabel('date')
    plt.title('HydroShare Issue Status')

    xdata = df_dt.index

    ydata = df_dt.number.values
    plt.plot(xdata, df_dt.number, color='k', linestyle='-', label='all')

    ydata = df_dt.closed.values
    plt.plot(xdata, ydata, color='b', linestyle='-', label='closed')

    ydata = df_dt.open.values
    plt.plot(xdata, df_dt.open, color='r', linestyle='-', label='open')
    plt.legend()
    plt.tight_layout()
    outpath = os.path.join(dirname, 'hs-issue-status.png')
    plt.savefig(outpath)


def open_issues(df, dirname):

    # plot a summary of open issues
    df_open = df[df.state == 'open']

    # group open bugs by date
    df_open_bug = df_open[df_open.label == 'bug']
    df_open_bug_list = list(df_open_bug.number.values)
    df_open_bug = df_open_bug.groupby(pandas.Grouper(key='created_dt',
                                                     freq='W')) \
                             .count().cumsum()

#    # group open enhancements by date
#    df_open_enh = df_open[df_open.label == 'enhancement']
#    df_open_enh_list = list(df_open_enh.number.values)
#    df_open_enh = df_open_enh.groupby(pandas.Grouper(key='created_dt',
#                                                     freq='W')) \
#                             .count().cumsum()

    # group all open issues that are not bugs or enhancements by date
    df_open_non = df_open[~df_open.label.isin(['bug', 'enhancement'])]
    df_open_non = df_open_non.drop_duplicates('number')

    # remove all issue numbers that exist in enhancements and bugs lists
    bug_enh_tickets = list(df_open_bug_list) #+ list(df_open_enh_list)
    df_open_non = df_open_non[~df_open_non.isin(bug_enh_tickets)]

    df_open_non = df_open_non.groupby(pandas.Grouper(key='created_dt',
                                                     freq='W')) \
                             .count().cumsum()

    print('Found %d non-bug, '
          'non-enhancement issues' % (len(df_open_non.number)))

    fig = plt.figure()
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel('issue count')
    plt.xlabel('date')
    plt.title('HydroShare Open Issues Summary')
    ax = plt.gca()

    xdata = df_open_non.index
    ydata = df_open_non.number.values
    plt.plot(xdata, ydata, color='k', linestyle='-', label='non-bug, '
                                                           'non-enhancement')

    xdata = df_open_bug.index
    ydata = df_open_bug.number.values
    plt.plot(xdata, ydata, color='r', linestyle='-', label='bugs')

#    xdata = df_open_enh.index
#    ydata = df_open_enh.number.values
#    plt.plot(xdata, ydata, color='b', linestyle='-', label='enhancements')

    plt.legend()
    plt.tight_layout()
    outpath = os.path.join(dirname, 'hs-open-issues-summary.png')
    plt.savefig(outpath)

