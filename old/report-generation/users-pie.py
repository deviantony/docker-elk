#!/usr/bin/env python3 

import os
import pytz
import pandas
import argparse
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


def load_data(workingdir):

    # load the activity data
    path = os.path.join(workingdir, 'users.pkl')
    df = pandas.read_pickle(path)

    # convert dates
    df['date'] = pandas.to_datetime(df.usr_created_date).dt.normalize()

    df.usr_created_date = pandas.to_datetime(df.usr_created_date).dt.normalize()
    df.usr_last_login_date = pandas.to_datetime(df.usr_last_login_date).dt.normalize()
    df.report_date = pandas.to_datetime(df.report_date).dt.normalize()

#    # fill NA values.  This happens when a user never logs in
#    df.usr_last_login_date = df.usr_last_login_date.fillna(0)
#
#    # replace NaN to clean xls output
#    df = df.fillna('')

    # add another date column and make it the index
    df['Date'] = df['date']

    # change the index to timestamp
    df.set_index(['Date'], inplace=True)

    return df


def subset_by_date(dat, st, et):

    if type(dat) == pandas.DataFrame:

        # select dates between start/end range
        mask = (dat.date >= st) & (dat.date <= et)
        dat = dat.loc[mask]
        return dat

    elif type(dat) == pandas.Series:

        # select dates between start/end range
        mask = (dat.index >= st) & (dat.index <= et)
        return dat.loc[mask]


def user_types_pie_chart(working_dir, st, et, drop_cols,
                         figtitle, 
                         filename='hydroshare-user-types.png'):

    print('--> building user types pie-chart')

    # load the data based on working directory
    df = load_data(working_dir)
    df = subset_by_date(df, st, et)
    df = df.filter(items=['usr_type'])
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

    # count number of users for each type
    for u in user_types:
        df[u] = np.where(df['usr_type'] == u, 1, 0)
    df['Other'] = np.where(~df['usr_type'].isin(user_types), 1, 0)

    # remove 'usr_type' b/c it's no longer needed
    df = df.drop('usr_type', axis=1)

    # remove specified columns so they won't be plotted
    unreported_users = 0
    for drp in drop_cols:
        try:
            print('--> not reporting %s: %s users'
                  % (drp, df[drp].sum()))
            df.drop(drp, inplace=True, axis=1)
        except:
            pass

    # calculate total and percentages for each user type
    ds = df.sum()
    df = pandas.DataFrame({'type': ds.index, 'score': ds.values})
    df = df.set_index('type')
    df['percent'] = round(df['score']/df['score'].sum()*100, 2)

    print('--> total number of users reporting: %d' % df.score.sum())

    for u in user_types:
        if u not in drop_cols:
            pct = df.loc[u].percent
            df = df.rename({u: '%s (%2.2f%%)' % (u, pct)})

    # make pie chart
    print('--> making user types pie chart...')
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.title(figtitle)

    df.percent.plot.pie(ax=ax, labeldistance=1.1)

    plt.xlabel('')
    plt.ylabel('')
    plt.tight_layout()

    # save the figure and the data
    print('--> saving figure as %s' % filename)
    outpath = os.path.join(working_dir, filename)
    plt.savefig(outpath, bbox_inches="tight")


def user_type_specified(working_dir, st, et, figtitle,
                        filename='hydroshare-user-type-completed.png'):

    print('--> building user types pie-chart')

    # load the data based on working directory
    df = load_data(working_dir)
    df = subset_by_date(df, st, et)
    df = df.filter(items=['usr_type'])
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

    # count number of users for each type
    df['Specified'] = np.where(df['usr_type'].isin(user_types), 1, 0)
    df['Not Specified'] = np.where(~df['usr_type'].isin(user_types), 1, 0)

    df = pandas.DataFrame({'type': ['Specified', 'Not Specified'],
                           'score': [df['Specified'].sum(),
                                     df['Not Specified'].sum()]
                           })
    df = df.set_index('type')
    df['percent'] = round(df['score']/df['score'].sum()*100, 2)
    df = df.rename({'Specified': 'Specified (%2.2f%%)' %
                                 (df.loc['Specified'].percent)})
    df = df.rename({'Not Specified': 'Not Specified (%2.2f%%)' %
                                     (df.loc['Not Specified'].percent)})

    # make pie chart
    print('--> making user types pie chart...')
    fig = plt.figure(figsize=(10, 10))
    plt.title(figtitle)

    def make_autopct(values, scores):
        def my_autopct(pct):
            idx = np.argmin(abs(values - pct))
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=scores[idx])
        return my_autopct

    labels = ['Specified', 'Not Specified']
    fracs = df.percent.values
    scores = df.score.values
    plt.pie(fracs, labels=labels, autopct=make_autopct(fracs, scores))

    plt.xlabel('')
    plt.ylabel('')

    # save the figure and the data
    print('--> saving figure as %s' % filename)
    outpath = os.path.join(working_dir, filename)
    plt.savefig(outpath, bbox_inches="tight")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='user type statistics')
    parser.add_argument('--working-dir',
                        help='path to directory containing elasticsearch data',
                        required=True)
    parser.add_argument('--figure-title',
                        help='title for the output figure',
                        default='HydroShare User Type Distribution %s' \
                        % datetime.now().strftime('%m-%d-%Y') )
    parser.add_argument('--filename',
                        help='output figure name',
                        default='hydroshare-user-types.png')
    parser.add_argument('--st',
                        help='start time MM-DD-YYYY, (UTC)',
                        default='01-01-2000')
    parser.add_argument('--et',
                        help='start time MM-DD-YYYY, (UTC)',
                        default=datetime.now().strftime('%m-%d-%Y'))
    parser.add_argument('--exclude',
                        help='comma separated list of user types to exclude',
                        type=str, default=',')
    parser.add_argument('-p',
                        help='plot pie chart of user types',
                        action='store_true')
    parser.add_argument('-c',
                        help='plot pie chart of user types complete vs not completed',
                        action='store_true')
    args = parser.parse_args()

    excludes = [item for item in args.exclude.split(',')]

    ######### check date formats #########
    st_str = args.st
    et_str = args.et
    try:
        st = datetime.strptime(st_str, '%m-%d-%Y')
    except ValueError:
        st = datetime.strptime('01-01-2000', '%m-%d-%Y')
        print('\tincorrect start date format, using default start date: 01-01-2000')
    try:
        et = datetime.strptime(et_str, '%m-%d-%Y')
    except ValueError:
        et = datetime.now()
        print('\tincorrect end date format, using default start date: %s' % et.strftime('%m-%d-%Y'))

    # set timezone for start and end dates
    st = pytz.utc.localize(st)
    et = pytz.utc.localize(et)

    # check that dat exist
    if not os.path.exists(os.path.join(args.working_dir, 'users.pkl')):
        print('\n\tcould not find \'users.pkl\', skipping.'
              '\n\trun \'collect_hs_data\' to retrieve these missing data')
    else:
        if args.p:
            user_types_pie_chart(args.working_dir, st, et,
                                 excludes,
                                 args.figure_title,
                                 args.filename)
        if args.c:
            user_type_specified(args.working_dir, st, et,
                                args.figure_title,
                                args.filename)
