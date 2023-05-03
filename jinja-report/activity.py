#!/usr/bin/env python3

import os
import pandas
import argparse
import numpy as np
from tabulate import tabulate
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import plot
import utilities


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


def quarterly_activity_table(input_directory='.',
                             start_time=datetime(2000, 1, 1),
                             end_time=datetime(2030, 1, 1),
                             step=1,
                             label='total users',
                             color='k',
                             linestyle='-',
                             aggregation='Q',
                             **kwargs):
    print('--> calculating activity table')

    # load the data based on working directory
    df = load_data(input_directory, 'activity.pkl')

    # drop all but elasticsearch indices that match www-activity-####.##
    # df = df.loc[df['es-index'].str.match('^www-activity-\d{4}.\d{2}$')]

    df = df.filter(['action'], axis=1)

    # create columns for each action
    for act in df.action.unique():
        df[act] = np.where(df.action == act, 1, 0)

    # remove the action column since its been divided into
    # individual columns
    df.drop('action', axis=1, inplace=True)
    # df = df.loc[:, df.columns.notnull()]

    df = df.groupby(pandas.Grouper(freq=aggregation)).sum()

    # drop unnecessary columns
    df = df.filter(['Date', 'begin_session', 'login', 'delete',
                    'create', 'download', 'app_launch'], axis=1)

    # rename columns
    df = df.rename(columns={'begin_session': 'Begin\nSession',
                            'login': 'Login',
                            'delete': 'Delete\nResource',
                            'create': 'Create\nResource',
                            'download': 'Download\nResource',
                            'app_launch': 'App\nLaunch'
                            })

    # modify the index to string type - for table printing
    df.index = [item.strftime('%m-%d-%Y') for item in df.index]

    # reverse the rows so that the table will be created in descending
    # chronological order
    df = df[::-1]

    return plot.PlotObject(None, None,
                           dataframe=df)


#def total_app_actions(working_dir, st, et, agg):
#
#    print('--> calculating all actions')
#
#    # load the data based on working directory
#    df = load_data(working_dir)
#
#    # group and cumsum
#    df = df.sort_index()
#    df = df[df.action == 'app_launch']
#    ds = df.groupby(pandas.Grouper(freq=agg)).action \
#                                             .count() \
#                                             .cumsum()
#
#    print(ds.max())
#    ds = subset_by_date(ds, st, et)
#
#    # create plot object
#    x = ds.index
#    y = ds.values.tolist()
#    plot = PlotObject(x, y, label='All App Launches', style='k-')
#
#    return plot
#
#
#def jupyter_actions(working_dir, st, et, agg):
#
#    print('--> calculating jupyter actions')
#
#    # load the data based on working directory
#    df = load_data(working_dir)
#
#    # group and cumsum
#    df = df.sort_index()
#    jhnames = ['JupyterHub NCSA', 'JupyterHub']
#    df = df[df.action == 'app_launch']
#    df = df[df.name.isin(jhnames)]
#    ds = df.groupby(pandas.Grouper(freq=agg)).action \
#                                             .count()
#    print('-- --> Average of %3.2f JupterHub launches per %s' % (ds.mean(), agg))
#    ds = ds.cumsum()
#    print(ds.max())
#
#    ds = subset_by_date(ds, st, et)
#
#    # create plot object
#    x = ds.index
#    y = ds.values.tolist()
#    plot = PlotObject(x, y, label='JupyterHub App Launches', style='g-')
#
#    return plot
#
#
#def download_actions(working_dir, st, et, agg):
#    
#    # load the data based on working directory
#    df = load_data(working_dir)
#    
#    df = df.sort_index()
#    df = df[df.action == 'app_launch']
#    appdf = pandas.DataFrame.from_dict({'date':df.date})
#
#
#def all_app_actions(working_dir, st, et, agg):
#
#    print('--> calculating all actions')
#
#    # load the data based on working directory
#    df = load_data(working_dir)
#
#    # group and cumsum
#    df = df.sort_index()
#    df = df[df.action == 'app_launch']
#    appdf = pandas.DataFrame.from_dict({'date':df.date})
#    for act in df.name.unique():
#        appdf[act] = np.where(df.name == act, 1, 0)
#    appdf = appdf.resample('D').sum().fillna(0)
#    appcols = [c for c in appdf.columns if c != 'date']
#    ds = appdf[appcols].groupby(pandas.Grouper(freq=agg)).sum()
#    ds = ds.cumsum()
#
#    ds['date'] = ds.index
#    ds = subset_by_date(ds, st, et)
#
#    # create plot objects
#    plots = []
#    cmap = plt.get_cmap('viridis')
#    colors = cmap(np.linspace(0, 1, len(ds.columns)))
#    i = 0
#    for col in ds.columns:
#        if col.lower() == 'date':
#            continue
#        x = ds[col].index
#        y = ds[col].values.tolist()
#        plot = PlotObject(x, y, label=col, style='-', color=colors[i])
#        plots.append(plot)
#        i += 1
#
#    return plots
#
#
#def plot(plotObjs_ax1, filename, plotObjs_ax2=[], **kwargs):
#    """
#    Creates a figure give plot objects
#    plotObjs: list of plot object instances
#    filename: output name for figure *.png
#    **kwargs: matplotlib plt args, e.g. xlabel, ylabel, title, etc
#    """
#
#    # create figure of these data
#    print('--> making figure...')
#    fig, ax = plt.subplots(figsize=(12, 9))
#    plt.xticks(rotation=45)
#    plt.subplots_adjust(bottom=0.25)
#
#    # set plot attributes
#    for k, v in kwargs.items():
#        getattr(ax, 'set_'+k)(v)
#
#    for pobj in plotObjs_ax1:
#        ax.plot(pobj.x, pobj.y, pobj.style, label=pobj.label)
#
#    if len(plotObjs_ax2) > 0:
#        ax2 = ax.twinx()
#        for pobj in plotObjs_ax2:
#            ax2.plot(pobj.x, pobj.y, pobj.style, label=pobj.label)
#
#    # add a legend
#    plt.legend()
#
#    # add monthly minor ticks
#    months = mdates.MonthLocator()
#    ax.xaxis.set_minor_locator(months)
#
#    # save the figure and the data
#    print('--> saving figure as %s' % filename)
#    plt.savefig(filename)
#
#
#if __name__ == "__main__":
#
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--working-dir',
#                        help='path to directory containing elasticsearch data',
#                        required=True)
#    parser.add_argument('--agg',
#                        help='aggregation, i.e http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases.',
#                        default='Q')
#    parser.add_argument('--figure-title',
#                        help='title for the output figure',
#                        default='HydroShare App Launches %s'
#                        % datetime.now().strftime('%m-%d-%Y'))
#    parser.add_argument('--filename',
#                        help='filename for the output figure',
#                        default='hydroshare-apps.png')
#    parser.add_argument('--st',
#                        help='start time MM-DD-YYYY',
#                        default='01-01-2000')
#    parser.add_argument('--et',
#                        help='start time MM-DD-YYYY',
#                        default=datetime.now().strftime('%m-%d-%Y'))
#    parser.add_argument('-t',
#                        help='create activity table',
#                        action='store_true')
#    parser.add_argument('-a',
#                        help='plot total app launches',
#                        action='store_true')
#    parser.add_argument('-j',
#                        help='plot all JupyterHub launches',
#                        action='store_true')
#    parser.add_argument('-A',
#                        help='plot total launches for every known app.',
#                        action='store_true')
#    parser.add_argument('-tabulate',
#                        help='dump output into a table',
#                        action='store_true')
#
#    args = parser.parse_args()
#
#    # check date formats 
#    st_str = args.st
#    et_str = args.et
#    try:
#        st = datetime.strptime(st_str, '%m-%d-%Y')
#    except ValueError:
#        st = datetime.strptime('01-01-2000', '%m-%d-%Y')
#        print('\tincorrect start date format, using default start '
#              'date: 01-01-2000')
#    try:
#        et = datetime.strptime(et_str, '%m-%d-%Y')
#    except ValueError:
#        et = datetime.now()
#        print('\tincorrect end date format, using default start date: %s'
#              % et.strftime('%m-%d-%Y'))
#
#    # check that dat exist
#    if not os.path.exists(os.path.join(args.working_dir, 'activity.pkl')):
#        print('\n\tcould not find \'activity.pkl\', skipping.'
#              '\n\trun \'collect_hs_data\' to retrieve these missing data')
#    else:
#        # cast input strings to integers
#        agg = args.agg
#        plots = []
#
#        if args.t:
#            res = activity_table(args.working_dir, agg)
#            create_activity_table_figure(res,
#                                         os.path.join(args.working_dir,
#                                                      args.filename))
#        if args.a:
#            res = total_app_actions(args.working_dir, st, et, agg)
#            plots.append(res)
#        if args.j:
#            res = jupyter_actions(args.working_dir, st, et, agg)
#            plots.append(res)
#        if args.A:
#            res = all_app_actions(args.working_dir, st, et, agg)
#            plots.extend(res)
#        if not args.tabulate:
#            if len(plots) > 0:
#                plot(plots, os.path.join(args.working_dir, args.filename),
#                     title=args.figure_title,
#                     ylabel='Number of Launches',
#                     xlabel='Date')
#        else:
#            data = {'date': plots[0].x}
#            for plot in plots:
#                data[plot.label] = plot.y
#            df = pandas.DataFrame.from_dict(data)
#            df.to_excel(os.path.join(args.working_dir, 'activity_table.xlsx'))
