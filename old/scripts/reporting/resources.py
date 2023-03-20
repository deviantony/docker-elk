#!/usr/bin/env python3 

import os
import csv
import pandas
import argparse
import numpy as np
from tabulate import tabulate
from datetime import datetime, timedelta
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class PlotObject(object):
    def __init__(self, x, y, label='', style='b-'):
        self.x = x
        self.y = y
        self.label = label
        self.style = style

    def get_dataframe(self):
        df = pandas.DataFrame(self.y, index=self.x, columns=[self.label])
        df.index = pandas.to_datetime(df.index)
        return df

def load_data(workingdir):

    # load the activity data
    path = os.path.join(workingdir, 'resources.pkl')
    df = pandas.read_pickle(path)

    # convert dates
    df['date'] = pandas.to_datetime(df.res_date_created).dt.normalize()
    df.res_date_created = pandas.to_datetime(df.res_date_created).dt.normalize()

    # replace NaN to clean xls output
    df = df.fillna('')

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


def total_resources_by_type(working_dir, st, et, agg='1D'):

    print('--> calculating total users')

    # load the data based on working directory
    df = load_data(working_dir)
    df = subset_by_date(df, st, et)
    df.fillna(0)
    df.res_size = df.res_size / 1000000000

    # loop through each resource type and isolate resource size
    # in its own data frame
    resource_types = list(df.res_type.unique())
    dfs = []
    for rtype in resource_types:
        dat = df[df.res_type == rtype]
        dat = dat.filter(['res_size'], axis=1)
        dat = dat.rename(columns={'res_size':rtype})
        dfs.append(dat)

    # join all the data frames together along a common index
    df = pandas.concat(dfs)

    # fill N/A and calculate cumulative resource sizes
    df = df.fillna(0)
    df = df.sort_index()
    df = df.cumsum()

    
#    import pdb; pdb.set_trace()
#        dat = dat.sort_index()
#        ds = dat.res_size.cumsum()
#        
#        # create plot object
#        x = ds.index
#        y = ds.values.tolist()
#        plots.append(PlotObject(x, y, label=rtype))

    return df



def plot_stacked(df, filename, **kwargs):

    # create figure of these data
    print('--> making figure...')
    fig = plt.figure(figsize=(12, 9))
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.25)
    ax = plt.axes()

    df.plot.area(ax=ax, linewidth=0, colormap="gist_ncar_r")

    # set plot attributes
    for k, v in kwargs.items():
        getattr(ax, 'set_'+k)(v)

    # add a legend
    plt.legend()

    # save the figure and the data
    print('--> saving figure as %s' % filename)
    plt.savefig(filename)

def validate_inputs(working_dir, st, et):

    ######### check date formats #########
    try:
        st = datetime.strptime(st, '%m-%d-%Y')
    except ValueError:
        st = datetime.strptime('01-01-2000', '%m-%d-%Y')
        print('\tincorrect start date format, using default start date: 01-01-2000')
    try:
        et = datetime.strptime(et, '%m-%d-%Y')
    except ValueError:
        et = datetime.now()
        print('\tincorrect end date format, using default start date: %s' % et.strftime('%m-%d-%Y'))


    ######### check that dat exist #########
    if not os.path.exists(os.path.join(working_dir, 'activity.pkl')):
        print('\n\tcould not find \'activity.pkl\', skipping.'
              '\n\trun \'collect_hs_data\' to retrieve these missing data')

    return st, et

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='general user statistics')
    parser.add_argument('--working-dir',
                        help='path to directory containing elasticsearch data',
                        required=True)
    parser.add_argument('--out-xlsx',
                        help='path to output xlsx file',
                        default='stats.xlsx')
    parser.add_argument('--step',
                        help='timestep to use in aggregation in days',
                        default=7)
    parser.add_argument('--active-range',
                        help='number of days that qualify a user as active',
                        default=90)
    parser.add_argument('--figure-title',
                        help='title for the output figure',
                        default='HydroShare Resource Size (GB) %s' \
                        % datetime.now().strftime('%m-%d-%Y') )
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
    st, et = validate_inputs(args.working_dir, args.st, args.et)


    plots = []
    if args.t:
        df = (total_resources_by_type(args.working_dir,
                                         st,
                                         et,
                                         agg='1W'))
        plot_stacked(df, os.path.join(args.working_dir, 'hydroshare_res.png'),
             title=args.figure_title,
             ylabel='Disk Size (GB)',
             xlabel='Date Resource Created')


#    if args.t:
#        res = total_users(args.working_dir, st, et,
#                          step)
#        plots.append(res)
#    if args.a:
#        res = active_users(args.working_dir, st, et,
#                           activedays, step)
#        plots.append(res)
#    if args.n:
#        res = new_users(args.working_dir, st, et,
#                        activedays, step)
#        plots.append(res)
#    if args.r:
#        res = returning_users(args.working_dir, st, et,
#                              activedays, step)
#        plots.append(res)
#
#
#    print('Script Complete')
#
#
#





