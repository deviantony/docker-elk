#!/usr/bin/env python3 

import os
import pytz
import numpy
import pandas
import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import cm
from pandas.plotting import register_matplotlib_converters

import spam
import plot
import utilities


register_matplotlib_converters()
def load_data(workingdir, pickle_file='users.pkl', filter_spam=True):

    # load the activity data
    path = os.path.join(workingdir, pickle_file)
    df = pandas.read_pickle(path)

    types = {'users.pkl': {'from': 'usr_id',
                           'to': 'user_id'},
             'resources.pkl': {'from': 'resource_id',
                               'to': 'resources'},
             'activity.pkl': {'from': 'user_id',
                              'to': 'user_id'}}

    # filter spam users
    typ = os.path.basename(pickle_file)
    if filter_spam:
        df = spam.filter_dataframe(df,
                                   workingdir,
                                   use_cache=True,
                                   input_col=types[typ]['from'],
                                   spam_col=types[typ]['to'])

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


#        # fill NA values.  This happens when a user never logs in
#        df.usr_last_login_date = df.usr_last_login_date.fillna(0, downcast=False)

#        # replace NaN to clean xls output
#        df = df.fillna('', downcast=False)

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


def total(input_directory='.',
          start_time=datetime(2000, 1, 1),
          end_time=datetime.today(),
          step=1,
          label='total users',
          color='k',
          linestyle='-',
          **kwargs):

    print('--> calculating total users')

    # load the data based on working directory
    df = load_data(input_directory)

    # group and cumsum
    df = df.sort_index()
    grp = '%dd' % step
    ds = df.groupby(pandas.Grouper(freq=grp)).count().usr_id.cumsum()

    ds = utilities.subset_by_date(ds, start_time, end_time)

    # create plot object
    x = ds.index
    y = ds.values.tolist()
    return plot.PlotObject(x, y,
                           label=label,
                           color=color,
                           linestyle=linestyle)


def active(input_directory='',
           start_time=datetime(2000, 1, 1),
           end_time=datetime.today(),
           active_range=30,
           step=1,
           label='Active Users',
           color='b',
           linestyle='-',
           **kwargs):
    """
    Calculates the number of active users for any given time frame.
    An active user is a user that has performed a HydroShare action 
    (as defined in activity.pkl) within the specified active range.
    """

    print('--> calculating active users')

    # load the data based on working directory
    df = load_data(input_directory, 'activity.pkl')
    df = utilities.subset_by_date(df, start_time, end_time)
    df = df.sort_index()

    dfu = load_data(input_directory, 'users.pkl')
    dfu = utilities.subset_by_date(dfu, start_time, end_time)

    x, y = [], []

    # set the start date as the earliest available date plus the
    # active date range
    t = df.date.min() + timedelta(days=active_range)
    while t < end_time:

        min_active_date = t - timedelta(days=active_range)

        # isolate users that performed an action
        subdf = df[(df.date <= t) &
                   (df.date > min_active_date)]
        total_active_users = subdf.user_id.nunique()

        # save the results
        x.append(t)
        y.append(total_active_users)

        t += timedelta(days=step)

    # create plot object
    plot_obj = plot.PlotObject(x, y, label=label,
                               color=color, linestyle=linestyle)

    return plot_obj


def new(input_directory='.',
        start_time=datetime(2000, 1, 1),
        end_time=datetime.today(),
        active_range=30,
        step=1,
        label='New Users',
        color='g',
        linestyle='-',
        **kwargs):

    # load the data based on working directory
    df = load_data(input_directory)
    df = utilities.subset_by_date(df, start_time, end_time)

    print('--> calculating new users')
    x = []
    y = []

    t = df['usr_created_date'].min()
    while t < end_time:

        earliest_date = t - timedelta(days=active_range)

        subdfn = df[(df.usr_created_date <= t) &
                    (df.usr_created_date > earliest_date)]
        new = subdfn.usr_id.nunique()

        y.append(new)
        x.append(t)

        t += timedelta(days=step)

    # create plot object
    return plot.PlotObject(x,
                           y,
                           label=label,
                           color=color,
                           linestyle=linestyle)


def returning(input_directory='.',
              start_time=datetime(2000, 1, 1),
              end_time=datetime.today(),
              active_range=30,
              step=10,
              color='r',
              label='Returning Users',
              linestyle='-',
              **kwargs):

    # load the data based on working directory
    df = load_data(input_directory, 'users.pkl')
    df = utilities.subset_by_date(df, start_time, end_time)
    dfa = load_data(input_directory, 'activity.pkl')
    dfa = utilities.subset_by_date(dfa, start_time, end_time)

    print('--> calculating returning users')
    x = []
    y = []

    # set the start date as the earliest available date plus the
    # active date range
    t = dfa.date.min() + timedelta(days=active_range)
#    n = []
#    a = []
    while t < end_time:
        earliest_date = t - timedelta(days=active_range)

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
    return plot.PlotObject(x,
                           y,
                           label=label,
                           color=color,
                           linestyle=linestyle)


def usertype(input_directory='.',
             start_time=datetime(2000, 1, 1),
             end_time=datetime.today(),
             aggregation='1D',
             linestyle='-',
             usertypes=[],
             **kwargs):

    # load the data based on working directory
    df = load_data(input_directory, 'users.pkl')
    df = utilities.subset_by_date(df, start_time, end_time)

    # define HS user types
    ut_vocab = ['Unspecified',
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
                'Other']

    # clean the data
    df.loc[~df.usr_type.isin(ut_vocab), 'usr_type'] = 'Other'

    # loop through each of the user types
    plots = []

    # plot only the provided user types
    if len(usertypes) == 0:
        # select all unique user types
        usertypes = df.usr_type.unique()

    colors = iter(cm.jet(numpy.linspace(0, 1, len(usertypes))))
    for utype in usertypes:

        # group by user type
        du = df.loc[df.usr_type == utype]

        # remove null values
        du = du.dropna()

        # group by date frequency
        ds = du.groupby(pandas.Grouper(freq=aggregation)).count().usr_type.cumsum()
        x = ds.index
        y = ds.values
        c = next(colors)

        # create plot object
        plots.append(plot.PlotObject(x, y, label=utype, color=c, linestyle='-'))

    return plots
