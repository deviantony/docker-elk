#!/usr/bin/env python3

import os
import pandas
import numpy as np
from datetime import datetime, timedelta


def subset_by_date(dat, st, et, col='date'):

    if type(dat) == pandas.DataFrame:

        # select dates between start/end range
        mask = (dat[col] >= st) & (dat[col] < et)
        dat = dat.loc[mask]
        return dat

    elif type(dat) == pandas.Series:

        # select dates between start/end range
        mask = (dat[col] >= st) & (dat[col] < et)
        return dat.loc[mask]


def all_resolved_issues(df, st, et, dirname):

    # plot a summary of open issues
    df_closed = df[df.state == 'closed']

    # select unique issue numbers to remove duplicates caused by
    # issues having multiple labels
    df_unique = df_closed.drop_duplicates('number')

    df_resolved = subset_by_date(df_unique, st, et, 'closed_dt')

    keys = ['closed_dt', 'number', 'title', 'url']

    # save to csv
    outpath = os.path.join(dirname, 'all_resolved_issues.csv')
    with open(outpath, 'a') as f:
        f.write('# List of all closed issues for the Hydroshare project\n')
        f.write('# Period start date:  %s\n' % st)
        f.write('# Period end date : %s\n' % et)
        f.write('# Generated on %s\n\n' % datetime.now())
        df_resolved[keys].sort_values('closed_dt', ascending=False).to_csv(f)


def resolved_bugs(df, st, et, dirname):

    # plot a summary of open issues
    df_bugs = df[(df.state == 'closed') & (df.label == 'bug')]

    df_bugs = subset_by_date(df_bugs, st, et, 'closed_dt')

    keys = ['closed_dt', 'number', 'title', 'url']

    # save to csv
    outpath = os.path.join(dirname, 'resolved_bugs.csv')
    with open(outpath, 'a') as f:
        f.write('# List of all closed bugs for the Hydroshare project\n')
        f.write('# Period start date:  %s\n' % st)
        f.write('# Period end date : %s\n' % et)
        f.write('# Generated on %s\n\n' % datetime.now())
        df_bugs[keys].sort_values('closed_dt', ascending=False).to_csv(f)


def resolved_features(df, st, et, dirname):

    # plot a summary of open issues
    df_feature = df[(df.state == 'closed') & (df.label == 'enhancement')]

    df_feature = subset_by_date(df_feature, st, et, 'closed_dt')

    keys = ['closed_dt', 'number', 'title', 'url']

    # save to csv
    outpath = os.path.join(dirname, 'resolved_features.csv')
    with open(outpath, 'a') as f:
        f.write('# List of all closed features for the Hydroshare project\n')
        f.write('# Period start date:  %s\n' % st)
        f.write('# Period end date : %s\n' % et)
        f.write('# Generated on %s\n\n' % datetime.now())
        df_feature[keys].sort_values('closed_dt', ascending=False).to_csv(f)

