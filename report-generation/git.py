#!/usr/bin/env python3

import os
import sys
import pandas
import getpass
import requests
import argparse
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


class PlotObject(object):
    def __init__(self, x, y, label='', style='b-', type='line'):
        self.x = x
        self.y = y
        self.label = label
        self.style = style
        self.type = type


class Issue(object):
    def __init__(self, issue_dict):
        self.number = issue_dict['number']
        self.state = issue_dict['state']
        self.url = issue_dict['url']
        self.labels = issue_dict['labels']

        self.title = issue_dict['title']
        self.title = self.title.replace('\r', '') \
                               .replace('\n', '') \
                               .replace(',', ' ')

        self.created_dt = issue_dict['created_at']
        if self.created_dt is not None:
            self.created_dt = datetime.strptime(self.created_dt,
                                          '%Y-%m-%dT%H:%M:%SZ')

        self.closed_dt = issue_dict['closed_at']
        if self.closed_dt is not None:
            self.closed_dt = datetime.strptime(self.closed_dt,
                                         '%Y-%m-%dT%H:%M:%SZ')

    def __issue_to_dict(self, i=None):
        if i is None:
            l = ''
        else:
            l = self.labels[i]['name']

        return dict(number=self.number,
                    created_dt=self.created_dt,
                    closed_dt=self.closed_dt,
                    state=self.state,
                    title=self.title,
                    url=self.url,
                    label=l)

    def get(self):
        data = []
        if len(self.labels) > 0:
            for i in range(0, len(self.labels)):
                data.append(self.__issue_to_dict(i))
        else:
            data.append(self.__issue_to_dict())
        return data


def subset_by_date(dat, st, et, key='date'):

    if type(dat) == pandas.DataFrame:

        # select dates between start/end range
        mask = (dat[key] >= st) & (dat[key] < et)
        dat = dat.loc[mask]
        return dat

    elif type(dat) == pandas.Series:

        # select dates between start/end range
        mask = (dat.index >= st) & (dat.index < et)
        return dat.loc[mask]


def validate_inputs(working_dir, st, et):

    # check date formats
    try:
        st = datetime.strptime(st, '%m-%d-%Y')
    except ValueError:
        st = datetime.strptime('01-01-2000', '%m-%d-%Y')
        print('\tincorrect start date format, using default start date: '
              '01-01-2000')
    try:
        et = datetime.strptime(et, '%m-%d-%Y')
    except ValueError:
        et = datetime.now()
        print('\tincorrect end date format, using default start date: %s'
              % et.strftime('%m-%d-%Y'))

#    # check that dat exist 
#    if not os.path.exists(os.path.join(working_dir, 'users.pkl')):
#        print('\n\tcould not find \'users.pkl\', skipping.'
#              '\n\trun \'collect_hs_data\' to retrieve these missing data')

    return st, et


def get_data(username, password,
             url="https://api.github.com/repos/hydroshare/hydroshare/issues",
             outpath='hydroshare_git_issues.csv'):


    dat = []
    idx = []

    AUTH = (username, password)

    r = requests.get('%s?state=all&per_page=500&page=%d' % (url, 1), auth=AUTH)
    jdat = r.json()
    for d in jdat:
        dat.append(Issue(d))

    # loop through github issue pages and save issue json
    if 'link' in r.headers:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
        print('--> collecting data.', end='', flush=True)
        while 'last' in pages and 'next' in pages:
            pg = pages['next'].split('=')[-1]
            r = requests.get(pages['next'], auth=AUTH)
            jdat = r.json()

            # save the issue
            for d in jdat:
                dat.append(Issue(d))
            print('.', end='', flush=True)

            # exit when the last page is reached
            if pages['next'] == pages['last']:
                break

            pages = dict(
                [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])

        print('done')

    # save to csv
    print('--> writing issues to csv...', end='', flush=True)
    with open(outpath, 'w') as f:
        f.write('#\n# Generated on %s\n' % datetime.now())
        f.write('# Notes: each issue is listed below once for each git label'
                ' that it has. This makes analysis with pandas easier\n#\n')
        headers = list(dat[0].get()[0].keys())
        f.write('%s\n' % ','.join(headers))
        for item in dat:
            for label in item.get():
                txt_list = [str(label[h]) for h in headers]
                f.write('%s\n' % ','.join(txt_list))
    print('done')


def load_data(working_dir):
    csv = os.path.join(working_dir, 'git_issues.csv')
    if not os.path.exists(csv):
        print('--> !Error: could not find git_issues.csv in %s' %
                path)
        sys.exit(0)

    # load the csv file into a pandas dataframe
    df = pandas.read_csv(csv, sep=',', comment='#')
    
    df['created_dt'] = pandas.to_datetime(df.created_dt, errors='coerce') \
                             .dt.normalize()
    df['closed_dt'] = pandas.to_datetime(df.closed_dt, errors='coerce') \
                            .dt.normalize()

    # summarize all issues by label

    #import pdb; pdb.set_trace()

    d = df.groupby('label').count().number.to_frame()
    d.columns = ['all_issues']

    # summarize all open issues
    d1 = df[df.state == 'open'].groupby('label').count().number.to_frame()
    d1.columns = ['open_issues']

    #d = d.merge(d1, on='label')
    d = d.merge(d1, left_index=True, right_index=True)

#    tbl = tabulate(d.sort_values('all_issues', ascending=False),
#                   headers='keys', tablefmt='psql')
#    print(tbl)

    # indicate issues as either 'open' or 'closed'
    df.loc[df.state == 'open', 'open'] = 1
    df.loc[df.state == 'closed', 'closed'] = 1

    return df
    

def filter_by_label(df, label_str):
    """
    label1 label2 -label3
    """
    
    if label_str == 'None' or label_str is None or len(label_str) == 0:
        return '', df

    all_labels = df.label.unique()

    logical_and = []
    logical_not = []
    # split apart the label components
    labels = label_str.split(' ')
    for label in labels:
        if label not in all_labels and label[1:] not in all_labels:
            print(f'Label not found: {label}, skipping')
            sys.exit(1)
        if label[0] == '~':
            logical_not.append(label[1:])
        else:
            logical_and.append(label)

    # filter the data
    series_label = ''
    if len(logical_and) > 0:
        df = df[df.label.isin(logical_and)]
        series_label += '+'.join(logical_and)
    if len(logical_not) > 0:
        df = df[~df.label.isin(logical_not)]
        series_label += '* -' + '-'.join(logical_not)

    return series_label, df


def all_issues(working_dir, st, et, ptype='line', agg='W', label=None, style='k-'):
    
    print('--> computing all issues...', flush=True, end='')
    df = load_data(working_dir)
    df = subset_by_date(df, st, et, key='created_dt')

    # select unique issue numbers to remove duplicates caused by
    # issues having multiple labels
    df_unique = df.drop_duplicates('number')

    # filter by label
    flabel, df_unique = filter_by_label(df, label)

    # group by date
    df_dt = df_unique.groupby(pandas.Grouper(key='created_dt', freq=agg)) \
                     .count().cumsum()

    xdata = df_dt.index
    ydata = df_dt.number.values
    
    #slabel = f'open+closed issues: {label}' if label is not None else 'open+closed issues'
    slabel = f'open+closed issues: {flabel}'
    plot = PlotObject(x=xdata, y=ydata,
                      label=slabel,
                      style=style,
                      type=ptype)

    print('%d total' % ydata[-1])
    return plot


def closed_issues(working_dir, st, et, ptype='line', agg='W', cum=False, label=None, style='b-'):
    """
    count of issues that have been closed based on closed_dt,
    summarized by Agg
    """

    print('--> computing all closed...', flush=True, end='')

    df = load_data(working_dir)
    df = subset_by_date(df, st, et, key='closed_dt')

    # select unique issue numbers to remove duplicates caused by
    # issues having multiple labels
    df_unique = df.drop_duplicates('number')
    
    # filter by label
    flabel, df_unique = filter_by_label(df, label)

#    # drop all values that do not have a closed_dt
#    df_closed = df_unique.closed_dt.dropna()

    # group by date closed
    df_dt = df_unique.groupby(pandas.Grouper(key='closed_dt', freq=agg)) \
                     .count()
    if cum:
        df_dt = df_dt.cumsum()

    xdata = df_dt.index
    ydata = df_dt.closed.values

#    slabel = f'closed issues: {label}' if label is not None else 'all closed issues'
    slabel = f'closed issues: {flabel}'
    plot = PlotObject(x=xdata, y=ydata,
                      label=slabel,
                      style=style,
                      type=ptype)

    print('%d total' % ydata[-1])
    return plot


def open_issues(working_dir, st, et, ptype='line', agg='W', cum=False, label=None, style='r-'):

    print('--> computing all open...', flush=True, end='')

    df = load_data(working_dir)
    df = subset_by_date(df, st, et, key='created_dt')

    # select unique issue numbers to remove duplicates caused by
    # issues having multiple labels
    df_unique = df.drop_duplicates('number')

    # filter by label
    flabel, df_unique = filter_by_label(df, label)

    # group by date
    df_dt = df_unique.groupby(pandas.Grouper(key='created_dt', freq=agg)) \
                     .count()
    if cum:
        df_dt = df_dt.cumsum()

    xdata = df_dt.index
    ydata = df_dt.open.values

    slabel = f'open issues: {flabel}'
    plot = PlotObject(x=xdata, y=ydata,
                      label=slabel,
                      style=style,
                      type=ptype)

    print('%d total' % ydata[-1])
    return plot


def open_bugs(working_dir, st, et, ptype='line', agg='W'):

    df = load_data(working_dir)
    df = subset_by_date(df, st, et, key='created_dt')

    # plot a summary of open issues
    df_open = df[df.state == 'open']

    # group open bugs by date
    df_open_bug = df_open[df_open.label == 'bug']
    df_open_bug_list = list(df_open_bug.number.values)
    df_open_bug = df_open_bug.groupby(pandas.Grouper(key='created_dt',
                                                     freq=agg)) \
                             .count().cumsum()
    xdata = df_open_bug.index
    ydata = df_open_bug.number.values

    plot = PlotObject(x=xdata, y=ydata,
                      label='open - bugs', style='r-',
                      type=ptype)
    return plot


def open_enhancements(working_dir, st, et, ptype='line', agg='W'):

    df = load_data(working_dir)
    df = subset_by_date(df, st, et, key='created_dt')

    # plot a summary of open issues
    df_open = df[df.state == 'open']

    # group open enhancements by date
    df_open_enh = df_open[df_open.label == 'enhancement']
    df_open_enh_list = list(df_open_enh.number.values)
    df_open_enh = df_open_enh.groupby(pandas.Grouper(key='created_dt',
                                                     freq=agg)) \
                             .count().cumsum()

    xdata = df_open_enh.index
    ydata = df_open_enh.number.values

    plot = PlotObject(x=xdata, y=ydata,
                      label='open - enhancements', style='b-',
                      type=ptype)
    return plot


def open_other(working_dir, st, et, ptype='line', agg='W'):

    df = load_data(working_dir)
    df = subset_by_date(df, st, et, key='created_dt')

    # plot a summary of open issues
    df_open = df[df.state == 'open']

    # group all open issues that are not bugs or enhancements by date
    df_open_non = df_open[~df_open.label.isin(['bug', 'enhancement'])]
    df_open_non = df_open_non.drop_duplicates('number')

    df_open_bug = df_open[df_open.label == 'bug']
    df_open_bug_list = list(df_open_bug.number.values)
    df_open_enh = df_open[df_open.label == 'enhancement']
    df_open_enh_list = list(df_open_enh.number.values)

    # remove all issue numbers that exist in enhancements and bugs lists
    bug_enh_tickets = list(df_open_bug_list) + list(df_open_enh_list)
    df_open_non = df_open_non[~df_open_non.isin(bug_enh_tickets)]

    df_open_non = df_open_non.groupby(pandas.Grouper(key='created_dt',
                                                     freq=agg)) \
                             .count().cumsum()

    xdata = df_open_non.index
    ydata = df_open_non.number.values

    plot = PlotObject(x=xdata, y=ydata,
                      label='open - other', style='k-',
                      type=ptype)
    return plot


def plot(plotObjs_ax1, filename, plotObjs_ax2=[],
         ptype='line', annotate=False, grid=True, **kwargs):
    """
    Creates a figure give plot objects
    plotObjs: list of plot object instances
    filename: output name for figure *.png
    **kwargs: matplotlib plt args, e.g. xlabel, ylabel, title, etc
    """

    # create figure of these data
    print('--> making figure...')
    fig, ax = plt.subplots(figsize=(12, 9))
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.25)

    # set plot attributes
    for k, v in kwargs.items():
        getattr(ax, 'set_'+k)(v)

    if ptype == 'bar':
        data = {}
        for p in plotObjs_ax1:
            data[p.label] = p.y
        data['date'] = plotObjs_ax1[0].x

        df = pandas.DataFrame(data)
        df.set_index('date', inplace=True)
        df.index = pandas.to_datetime(df.index)
        df.plot.bar(ax=ax)

        fig.autofmt_xdate()
        new_label = []
        for i in ax.get_xticklabels():
            date = datetime.strptime(i.get_text(), '%Y-%m-%d %H:%M:%S')
            new_label.append(date.strftime("%m-%Y"))
        ax.set_xticklabels(new_label)
        if annotate:
            for p in ax.patches:
                ax.annotate("%.2f" % p.get_height(),
                            (p.get_x() + p.get_width() / 2.,
                             p.get_height()),
                            ha='center',
                            va='center',
                            xytext=(0, 10),
                            textcoords='offset points')

    elif ptype == 'line':
        for pobj in plotObjs_ax1:
            ax.plot(pobj.x, pobj.y, pobj.style, label=pobj.label)
        
            # annotate the last point
            if annotate:
                ax.text(pobj.x[-1] + timedelta(days=5), # x-loc
                        pobj.y[-1], # y-loc
                        int(round(pobj.y[-1], 0)), # text value
                        bbox=dict(boxstyle='square,pad=0.5',
                                  fc='none', # foreground color
                                  ec='none', # edge color
                                  ))

        # add monthly minor ticks
        months = mdates.MonthLocator()
        ax.xaxis.set_minor_locator(months)
#        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b %d'))


    # add a legend
    plt.legend()

    # turn on the grid
    if grid:
        ax.grid()

    # save the figure and the data
    print('--> saving figure as %s' % filename)
    plt.savefig(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--working-dir',
                        help='path to working directory',
                        required=True)
    parser.add_argument('--git-url',
                        help='url for github project',
                        default="https://api.github.com/repos/hydroshare/hydroshare/issues")
    parser.add_argument('--username',
                        help='GitHub username')
    parser.add_argument('--password',
                        help='GitHub password')
    parser.add_argument('--filename',
                        help='filename for the output figure',
                        default='git-issues.png')
    parser.add_argument('--get-labels',
                        help='print all issue labels that are present in the data',
                        action='store_true')
    parser.add_argument('--figure-title',
                        help='title for output figure',
                        default='Summary of Git Issues')
    parser.add_argument('--collect',
                        help='force collection of data',
                        action='store_true')
    parser.add_argument('--plot-type',
                        help='type of plot; line or bar',
                        default='line')
    parser.add_argument('--agg',
                        help='data aggregation i.e. 1D, 1W, 3M, etc.',
                        default='1M')
    parser.add_argument('--st',
                        help='reporting start date MM-DD-YYYY',
                        default='01-01-2000')
    parser.add_argument('--et',
                        help='reporting end date MM-DD-YYYY',
                        default=datetime.now().strftime('%m-%d-%Y'))
    parser.add_argument('-a',
                        help='plot all issues by the date they were created',
                        action='store_true')
    parser.add_argument('-o',
                        help='plot all issues with status=open by the date in which they were created',
                        action='store_true')
    parser.add_argument('-c',
                        help='plot all issues with status=closed by the date in which they were closed',
                        action='store_true')
    parser.add_argument('-b',
                        help='plot all issues with status=open and type=bug by the date they were created',
                        action='store_true')
    parser.add_argument('--label', nargs='+',
            help='filter issues by label: "bug Modeling -enhancement" "* -bug"',
                        default=[None])
    parser.add_argument('-e',
                        help='plot open enhancement tickets',
                        action='store_true')
    parser.add_argument('-n',
                        help='plot open non-bug, non-enhancement issues',
                        action='store_true')
    parser.add_argument('--cumulative',
                        help='plot cumulative values',
                        action='store_true',
                        default=False)
    parser.add_argument('--annotate',
                        help='annotate the plot data',
                        action='store_true',
                        default=False)
    parser.add_argument('--grid',
                        help='add a grid to the plot',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    st, et = validate_inputs(args.working_dir, args.st, args.et)
    csv = os.path.join(args.working_dir, 'git_issues.csv')
    url = args.git_url

    # collect github data

    if not os.path.exists(csv) or args.collect:
        if not (args.username or args.password):
            username = input('Please enter your Github username: ')
            password = getpass.getpass('Password: ')
        else:
            username = args.username
            password = args.password
        get_data(username, password, url, csv)
    else:
        print('--> reusing %s' % csv)

    plots = []
   
#    import pdb; pdb.set_trace()

    # loop through labels
    for label in args.label:
        if args.a:
            # all issues
            plots.append(all_issues(args.working_dir,
                                    st, et,
                                    args.plot_type,
                                    args.agg, label))
        if args.o:
            # all open issues
            plots.append(open_issues(args.working_dir,
                                     st, et,
                                     args.plot_type,
                                     args.agg,
                                     cum=args.cumulative,
                                     label=label))
        if args.c:
            # all closed issues
            plots.append(closed_issues(args.working_dir,
                                       st, et,
                                       args.plot_type,
                                       args.agg,
                                       cum=args.cumulative,
                                       label=label))
        if args.b:
            # all open bugs
            plots.append(open_bugs(args.working_dir,
                                   st, et,
                                   args.plot_type,
                                   args.agg))
        if args.e:
            # all open enhancements
            plots.append(open_enhancements(args.working_dir,
                                           st, et,
                                           args.plot_type,
                                           args.agg))
        if args.n:
            # all non-bug non-enhancements
            plots.append(open_other(args.working_dir,
                                    st, et,
                                    args.plot_type,
                                    args.agg))
    if args.get_labels:
        df = load_data(args.working_dir)
        for label in df.label.unique():
            print(label)

    if len(plots) > 0:
        types = []
        for p in plots:
            types.append(p.type)
        t = list(set(types))

        if len(t) > 1:
            print('Cannot mix multiple plot types!')
            sys.exit(1)

        if t[0] == 'line':
            plot(plots, os.path.join(args.working_dir, args.filename),
                 title=args.figure_title,
                 ylabel='Number of Issues',
                 xlabel='Date Created',
                 annotate=args.annotate,
                 grid=args.grid,
                 ptype='line')
        elif t[0] == 'bar':
            annotate = False
#            if len(plots) == 1:
#                annotate = True
            plot(plots, os.path.join(args.working_dir, args.filename),
                 title=args.figure_title,
                 ylabel='Number of Issues',
                 xlabel='Date Created',
                 ptype='bar',
                 annotate=args.annotate)
        else:
            print('Unsupported plot type: %s' % t[0])
            sys.exit(1)
