#!/usr/bin/env python3 

import os
import pandas
import argparse
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class PlotObject(object):
    def __init__(self, x, y, label='', style='b-'):
        self.x = x
        self.y = y
        self.label = label
        self.style = style


def load_data(workingdir, pickle_file='users.pkl'):

    # load the activity data
    path = os.path.join(workingdir, pickle_file)
    df = pandas.read_pickle(path)

    columns = df.columns

    # parse users
    if 'usr_created_date' in columns:

        # convert dates
        df['date'] = pandas.to_datetime(df.usr_created_date).dt.normalize()

        df.usr_created_date = pandas.to_datetime(df.usr_created_date) \
                                    .dt.normalize()
        df.usr_last_login_date = pandas.to_datetime(df.usr_last_login_date) \
                                       .dt.normalize()
        df.report_date = pandas.to_datetime(df.report_date) \
                               .dt.normalize()

        # fill NA values.  This happens when a user never logs in
        df.usr_last_login_date = df.usr_last_login_date.fillna(0)

        # replace NaN to clean xls output
        df = df.fillna('')

        # add another date column and make it the index
        df['Date'] = df['date']

        # change the index to timestamp
        df.set_index(['Date'], inplace=True)

    # parse activity
    elif 'session_timestamp' in columns:

        # convert dates
        df['date'] = pandas.to_datetime(df.session_timestamp) \
                           .dt.normalize()

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


def total_users(working_dir, st, et, step):

    print('--> calculating total users')

    # load the data based on working directory
    df = load_data(working_dir)

    # group and cumsum
    df = df.sort_index()
    grp = '%dd' % step
    ds = df.groupby(pandas.TimeGrouper(grp)).count().usr_id.cumsum()

    ds = subset_by_date(ds, st, et)

    # create plot object
    x = ds.index
    y = ds.values.tolist()
    plot = PlotObject(x, y, label='total users', style='k-')

    return plot


def active_users(working_dir, st, et, activerange, step):
    """
    Calculates the number of active users for any given time frame.
    An active user is a user that has performed a HydroShare action 
    (as defined in activity.pkl) within the specified active range.
    """

    print('--> calculating active users')

    # load the data based on working directory
    df = load_data(working_dir, 'activity.pkl')
    df = subset_by_date(df, st, et)
    df = df.sort_index()

    dfu = load_data(working_dir, 'users.pkl')
    dfu = subset_by_date(dfu, st, et)

    x, y = [], []

    # set the start date as the earliest available date plus the 
    # active date range
    t = df.date.min() + timedelta(days=activedays)
    while t < et:

        min_active_date = t - timedelta(days=activerange)

        # isolate users that performed an action
        subdf = df[(df.date <= t) &
                   (df.date > min_active_date)]
        total_active_users = subdf.user_id.nunique()

#        # isolate new users (this is necessary to more accurately determine
#        # the initial count of active users since activity does not span 
#        # the full record of user accounts
#        subdfu = dfu[(dfu.usr_created_date <= t) &
#                     (dfu.usr_created_date > min_active_date)]
#        unique_new_users = subdfu.usr_id.unique()
#
#        total_active_users = len(set(list(unique_new_users) +
#                                     list(unique_active_users)))
        
        # save the results
        x.append(t)
        y.append(total_active_users)

        t += timedelta(days=step)

    # create plot object
    plot = PlotObject(x, y, label='active users (%d days)' % activerange,
                      style='b-')

    return plot


def new_users(working_dir, st, et, activerange, step):

    # load the data based on working directory
    df = load_data(working_dir)
    df = subset_by_date(df, st, et)

    print('--> calculating new users')
    x = []
    y = []

    t = df['usr_created_date'].min()
    while t < et:
        
        earliest_date = t - timedelta(days=activerange)

#        # subset all users to those that exist up to the current time, t
#        subdf = df[df.usr_created_date <= t]
#
#        # The number of new users in activerange up to time dateJoined[i] (i.e. the range 1:i) are users who 
#        # created their account after dateJoine[i]-activerange
#        earliest_date = t - timedelta(days=activerange)
#        y.append(np.where((subdf.usr_created_date >= earliest_date) &
#                                            (subdf.usr_created_date <= t),
#                                            1, 0).sum())

        subdfn = df[(df.usr_created_date <= t) &
                    (df.usr_created_date > earliest_date)]
        new = subdfn.usr_id.nunique()
        
        y.append(new)
        x.append(t)

        t += timedelta(days=step)

    # create plot object
    plot = PlotObject(x, y, label='new users', style='g-')

    return plot


def returning_users(working_dir, st, et, activerange, step):

    # load the data based on working directory
    df = load_data(working_dir, 'users.pkl')
    df = subset_by_date(df, st, et)
    dfa = load_data(working_dir, 'activity.pkl')
    dfa = subset_by_date(dfa, st, et)

    print('--> calculating returning users')
    x = []
    y = []

    # set the start date as the earliest available date plus the 
    # active date range
    t = dfa.date.min() + timedelta(days=activedays)
    n, a = [],[]
    while t < et:
        earliest_date = t - timedelta(days=activerange)

        ## subset all users to those that exist up to the current time, t
        #subdf = df[df.usr_created_date <= t]

        subdfn = df[(df.usr_created_date <= t) &
                    (df.usr_created_date > earliest_date)]
        new = subdfn.usr_id.nunique()

        # calculate active users for this range
        subdfa = dfa[(dfa.date <= t) &
                     (dfa.date > earliest_date)]
        active = subdfa.user_id.nunique()

        # Users who were active, but obtained an account prior to the
        # active period are users who continue to return to and work
        # with HydroShare.
        y.append(active - new)
        x.append(t)

        t += timedelta(days=step)

    # create plot object
    plot = PlotObject(x, y, label='returning users', style='r-')
    return plot


def plot(plotObjs_ax1, filename, plotObjs_ax2=[], **kwargs):
    """
    Creates a figure give plot objects
    plotObjs: list of plot object instances
    filename: output name for figure *.png
    **kwargs: matplotlib plt args, e.g. xlabel, ylabel, title, etc
    """

    # create figure of these data
    print('--> making figure...')
    fig = plt.figure(figsize=(12, 9))
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.25)
    ax = plt.axes()

    # set plot attributes
    for k, v in kwargs.items():
        getattr(ax, 'set_'+k)(v)

    for pobj in plotObjs_ax1:
        ax.plot(pobj.x, pobj.y, pobj.style, label=pobj.label)

    if len(plotObjs_ax2) > 0:
        ax2 = ax.twinx()
        for pobj in plotObjs_ax2:
            ax2.plot(pobj.x, pobj.y, pobj.style, label=pobj.label)

    # add a legend
    plt.legend()

    # add monthly minor ticks
    months = mdates.MonthLocator()
    ax.xaxis.set_minor_locator(months)

    # save the figure and the data
    print('--> saving figure as %s' % filename)
    plt.savefig(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='general user statistics')
    parser.add_argument('--working-dir',
                        help='path to directory containing elasticsearch data',
                        required=True)
    parser.add_argument('--step',
                        help='timestep to use in aggregation in days',
                        default=10)
    parser.add_argument('--active-range',
                        help='number of days that qualify a user as active',
                        default=90)
    parser.add_argument('--figure-title',
                        help='title for the output figure',
                        default='HydroShare User Summary %s' \
                        % datetime.now().strftime('%m-%d-%Y') )
    parser.add_argument('--filename',
                        help='filename for the output figure',
                        default='hydroshare-users.png')
    parser.add_argument('--st',
                        help='start time MM-DD-YYYY',
                        default='01-01-2000')
    parser.add_argument('--et',
                        help='start time MM-DD-YYYY',
                        default=datetime.now().strftime('%m-%d-%Y'))
    parser.add_argument('-t',
                        help='plot total users line',
                        action='store_true')
    parser.add_argument('-a',
                        help='plot active users line',
                        action='store_true')
    parser.add_argument('-n',
                        help='plot new users line',
                        action='store_true')
    parser.add_argument('-r',
                        help='plot returning users line',
                        action='store_true')
    args = parser.parse_args()

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

    # check that dat exist
    if not os.path.exists(os.path.join(args.working_dir, 'activity.pkl')):
        print('\n\tcould not find \'activity.pkl\', skipping.'
              '\n\trun \'collect_hs_data\' to retrieve these missing data')
    else:
        # cast input strings to integers
        step = int(args.step)
        activedays = int(args.active_range)

        plots = []
        if args.t:
            res = total_users(args.working_dir, st, et,
                              step)
            plots.append(res)
        if args.a:
            res = active_users(args.working_dir, st, et,
                               activedays, step)
            plots.append(res)
        if args.n:
            res = new_users(args.working_dir, st, et,
                            activedays, step)
            plots.append(res)
        if args.r:
            res = returning_users(args.working_dir, st, et,
                                  activedays, step)
            plots.append(res)
        if len(plots) > 0:
            plot(plots, os.path.join(args.working_dir, args.filename),
                 title=args.figure_title,
                 ylabel='Number of Users',
                 xlabel='Date')
