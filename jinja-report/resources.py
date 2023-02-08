#!/usr/bin/env python3 

import os
import csv
import pytz
import pandas
import argparse
import numpy as np
from tabulate import tabulate
from datetime import datetime, timedelta
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import plot
import utilities


def load_data(workingdir):

    # load the activity data
    path = os.path.join(workingdir, 'resources.pkl')
    df = pandas.read_pickle(path)

    # convert dates
    df['date'] = pandas.to_datetime(df.res_date_created).dt.normalize()
    df.res_date_created = pandas.to_datetime(df.res_date_created).dt.normalize()

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
        mask = (dat.date >= st) & (dat.date < et)
        dat = dat.loc[mask]
        return dat

    elif type(dat) == pandas.Series:

        # select dates between start/end range
        mask = (dat.index >= st) & (dat.index < et)
        return dat.loc[mask]


def total(input_directory='.',
          start_time=datetime(2000, 1, 1),
          end_time=datetime(2030, 1, 1),
          aggregation='1D',
          label='total resource size',
          color='b',
          linestyle='-',
          **kwargs):

    print('--> calculating total resources size')

    # load the data based on working directory
    print('    .. loading dataset')
    df = load_data(input_directory)
    df = subset_by_date(df, start_time, end_time)

    print('    .. filling missing values')
    df.fillna(0)

    print('    .. computing resource size (GB)')
    df.res_size = df.res_size / 1000000000

    print('    .. sorting data')
    df = df.sort_index()

    print('    .. determining cumulative sum')
    df = df.groupby(pandas.Grouper(freq=aggregation)).sum().cumsum()['res_size']

    plot_obj = plot.PlotObject(x=df.index,
                               y=df.values,
                               label=label,
                               color=color,
                               linestyle=linestyle)
    return plot_obj


def count(input_directory='.',
          start_time=datetime(2000, 1, 1),
          end_time=datetime(2030, 1, 1),
          aggregation='1D',
          label='total number of resources',
          color='b',
          linestyle='-',
          **kwargs):


    if 'status' not in kwargs.keys():
        raise Exception('Missing Status Argument. Can not create figure')

    terms = ['private', 'public', 'published', 'discoverable']
    if kwargs['status'] not in terms:
        raise Exception(f'{kwargs["status"]} not an known term. Please choose from one of the following: {terms}')

    print(f'--> calculating total {kwargs["status"]} resources')

    # load the data based on working directory
    print('    .. loading dataset')
    df = load_data(input_directory)
    df = subset_by_date(df, start_time, end_time)

    print('    .. filling missing values')
    df.fillna(0)

    print('    .. sorting data')
    df = df.sort_index()

    # filter only public
    print(f'    .. isolating resource status is {kwargs["status"]}')
    df = df[df.res_pub_status == kwargs['status']]

    print('    .. determining cumulative sum')
    df = df.groupby(pandas.Grouper(freq=aggregation)).count().cumsum()['res_size']

    plot_obj = plot.PlotObject(x=df.index,
                               y=df.values,
                               label=label,
                               color=color,
                               linestyle=linestyle)
    return plot_obj


def count_public(**kwargs):
    kwargs['status'] = 'public'
    return count(**kwargs)


def count_published(**kwargs):
    kwargs['status'] = 'published'
    return count(**kwargs)


def count_private(**kwargs):
    kwargs['status'] = 'private'
    return count(**kwargs)


def count_discoverable(**kwargs):
    kwargs['status'] = 'discoverable'
    return count(**kwargs)


#def total_resources_by_type(working_dir, st, et, agg='1D'):
#
#    print('--> calculating total resource size by type')
#
#
#    # load the data based on working directory
#    df = load_data(working_dir)
#    df = subset_by_date(df, st, et)
#    df.fillna(0)
#    df.res_size = df.res_size / 1000000000
#
#    # loop through each resource type and isolate resource size
#    # in its own data frame
#    resource_types = list(df.res_type.unique())
#    dfs = []
#    for rtype in resource_types:
#        dat = df[df.res_type == rtype]
#        dat = dat.filter(['res_size'], axis=1)
#        dat = dat.rename(columns={'res_size': rtype})
#        dfs.append(dat)
#
#    # join all the data frames together along a common index
#    df = pandas.concat(dfs, sort=False)
#
#    # fill N/A and calculate cumulative resource sizes
#    df = df.fillna(0)
#    df = df.sort_index()
#
#    # group by aggregation
#    return df.groupby(pandas.Grouper(freq=agg)).sum().cumsum()
#
#
#def total_resources_by_status(working_dir, st, et, agg='1D'):
#
#    print('--> calculating total resource size by status')
#
#
#    # load the data based on working directory
#    df = load_data(working_dir)
#    df = subset_by_date(df, st, et)
#
#    df = df[['res_pub_status']]
#    df = df.rename(columns={'res_pub_status':'status'})
#    for t in df.status.unique():
#        df.loc[df.status == t, t] = 1
#    df = df.drop(['status'], axis=1)
#    df = df.fillna(0)
#
#    df = df.groupby(pandas.Grouper(freq=agg)).sum().cumsum()
#
#    return df
#
#
#def plot_line(df, filename, **kwargs):
#
#    # create figure of these data
#    print('--> making figure...')
#    fig, ax = plt.subplots(figsize=(12, 9))
#    plt.xticks(rotation=45)
#    plt.subplots_adjust(bottom=0.25)
#
#    if 'columns' in kwargs.keys():
#        for label in kwargs['columns']:
#            df[label].plot(ax=ax, label=label)
#            
#            # annotate the last point
#            ax.text(df.index[-1] + timedelta(days=5), # x-loc
#                    df[label].iloc[-1], # y-loc
#                    f'{int(df[label].iloc[-1])}', # text value
#                    bbox=dict(boxstyle='square,pad=0.5',
#                              fc='none', # foreground color
#                              ec='none', # edge color
#                            ))
#    else:
#        df.plot(ax=ax)
#        # annotate the last point
#        ax.text(df.index[-1] + timedelta(days=5), # x-loc
#                df.iloc[-1], # y-loc
#                f'{int(df.iloc[-1])}', # text value
#                bbox=dict(boxstyle='square,pad=0.5',
#                          fc='none', # foreground color
#                          ec='none', # edge color
#                          ))
#
#    ax.grid()
#
#    # set plot attributes
#    for k, v in kwargs.items():
#        try:
#            getattr(ax, 'set_'+k)(v)
#        except AttributeError:
#            pass
#
#    # add a legend
#    if 'legend' in kwargs:
#        if kwargs['legend']:
#            plt.legend()
#
#    # save the figure and the data
#    print('--> saving figure as %s' % filename)
#    plt.savefig(filename)
#
#
#def plot_stacked(df, filename, **kwargs):
#
#    # create figure of these data
#    print('--> making figure...')
#    fig, ax = plt.subplots(figsize=(12, 9))
#    plt.xticks(rotation=45)
#    plt.subplots_adjust(bottom=0.25)
#
#    df.plot.area(ax=ax, linewidth=0, colormap="nipy_spectral")
#
#    # set plot attributes
#    for k, v in kwargs.items():
#        try:
#            getattr(ax, 'set_'+k)(v)
#        except AttributeError:
#            pass
#
#    # add a legend
#    if 'legend' in kwargs:
#        if kwargs['legend']:
#            plt.legend()
#
#    # save the figure and the data
#    print('--> saving figure as %s' % filename)
#    plt.savefig(filename)
#
#
#def validate_inputs(working_dir, st, et):
#
#    ######### check date formats #########
#    try:
#        st = datetime.strptime(st, '%m-%d-%Y')
#    except ValueError:
#        st = datetime.strptime('01-01-2000', '%m-%d-%Y')
#        print('\tincorrect start date format, using default start date: 01-01-2000')
#    try:
#        et = datetime.strptime(et, '%m-%d-%Y')
#    except ValueError:
#        et = datetime.now()
#        print('\tincorrect end date format, using default start date: %s' % et.strftime('%m-%d-%Y'))
#
#
#    ######### check that dat exist #########
#    if not os.path.exists(os.path.join(working_dir, 'activity.pkl')):
#        print('\n\tcould not find \'activity.pkl\', skipping.'
#              '\n\trun \'collect_hs_data\' to retrieve these missing data')
#
#    return st, et
#
#if __name__ == "__main__":
#
#    parser = argparse.ArgumentParser(description='general user statistics')
#    parser.add_argument('--working-dir',
#                        help='path to directory containing elasticsearch data',
#                        required=True)
#    parser.add_argument('--out-xlsx',
#                        help='path to output xlsx file',
#                        default='stats.xlsx')
#    parser.add_argument('--aggregation',
#                        help='aggregation to use, e.g. 1W',
#                        default='1W')
#    parser.add_argument('--active-range',
#                        help='number of days that qualify a user as active',
#                        default=90)
#    parser.add_argument('--figure-title',
#                        help='title for the output figure',
#                        default='HydroShare Resource Size (GB) %s' \
#                        % datetime.now().strftime('%m-%d-%Y') )
#    parser.add_argument('--st',
#                        help='start time MM-DD-YYYY',
#                        default='01-01-2000')
#    parser.add_argument('--et',
#                        help='start time MM-DD-YYYY',
#                        default=datetime.now().strftime('%m-%d-%Y'))
#    parser.add_argument('-t',
#                        help='plot total resources (cumulative)',
#                        action='store_true')
#    parser.add_argument('-u',
#                        help='plot total resource size (cumulative) by type',
#                        action='store_true')
#    parser.add_argument('-s',
#                        help='plot total resources by status',
#                        action='store_true')
#    parser.add_argument('--filename',
#                        default='hydroshare_res.png',
#                        help='name of the output file')
#
#    args = parser.parse_args()
#
#    ######### check date formats #########
#    st, et = validate_inputs(args.working_dir, args.st, args.et)
#
#    # set timezone to UTC
#    st = pytz.utc.localize(st)
#    et = pytz.utc.localize(et)
#
#    plots = []
#    if args.t:
#        df = (total_resources(args.working_dir,
#                              st,
#                              et,
#                              agg=args.aggregation))
#        plot_line(df,
#                  os.path.join(args.working_dir, args.filename),
#                  title=args.figure_title,
#                  ylabel='Disk Size (GB)',
#                  xlabel='Date Created')
#    if args.u:
#        df = (total_resources_by_type(args.working_dir,
#                                      st,
#                                      et,
#                                      agg=args.aggregation))
#        plot_stacked(df, os.path.join(args.working_dir, args.filename),
#                     title=args.figure_title,
#                     ylabel='Disk Size (GB)',
#                     xlabel='Date Created',
#                     legend=True)
#    if args.s:
#        df = total_resources_by_status(args.working_dir,
#                                       st,
#                                       et,
#                                       agg=args.aggregation)
#        plot_line(df,
#                  os.path.join(args.working_dir, args.filename),
#                  title='HydroShare Resource Count by Status',
#                  ylabel='Resource Count',
#                  xlabel='Date Created',
#                  legend=True,
#                  columns=['published',
#                           'discoverable',
#                           'public',
#                           'private'])
#
#
#
##    if args.t:
##        res = total_users(args.working_dir, st, et,
##                          step)
##        plots.append(res)
##    if args.a:
##        res = active_users(args.working_dir, st, et,
##                           activedays, step)
##        plots.append(res)
##    if args.n:
##        res = new_users(args.working_dir, st, et,
##                        activedays, step)
##        plots.append(res)
##    if args.r:
##        res = returning_users(args.working_dir, st, et,
##                              activedays, step)
##        plots.append(res)
##
##
##    print('Script Complete')
##
##
##
#
#
#
#
#
