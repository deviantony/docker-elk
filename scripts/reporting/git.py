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
    def __init__(self, x, y, label='', style='b-'):
        self.x = x
        self.y = y
        self.label = label
        self.style = style


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


def get_data(username, password,
             url="https://api.github.com/repos/hydroshare/hydroshare/issues",
             outpath='hydroshare_git_issues.csv'):

    dat = []
    idx = []

    AUTH = (username, password)

    r = requests.get('%s?state=all&per_page=50&page=%d' % (url, 1), auth=AUTH)
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
    

def all_issues(working_dir):
    
    print('--> computing all issues...', flush=True, end='')
    df = load_data(working_dir)

    # select unique issue numbers to remove duplicates caused by
    # issues having multiple labels
    df_unique = df.drop_duplicates('number')

    # group by date
    df_dt = df_unique.groupby(pandas.Grouper(key='created_dt', freq='W')) \
                     .count().cumsum()

    xdata = df_dt.index
    ydata = df_dt.number.values
    
    plot = PlotObject(x=xdata, y=ydata, label='all issues', style='k-')

    print('%d total' % ydata[-1])
    return plot

def closed_issues(working_dir):
    
    print('--> computing all closed...', flush=True, end='')
    
    df = load_data(working_dir)

    # select unique issue numbers to remove duplicates caused by
    # issues having multiple labels
    df_unique = df.drop_duplicates('number')

    # group by date
    df_dt = df_unique.groupby(pandas.Grouper(key='created_dt', freq='W')) \
                     .count().cumsum()

    xdata = df_dt.index
    ydata = df_dt.closed.values

    plot = PlotObject(x=xdata, y=ydata, label='closed issues', style='b-')

    print('%d total' % ydata[-1])
    return plot


def open_issues(working_dir):

    print('--> computing all open...', flush=True, end='')

    df = load_data(working_dir)

    # select unique issue numbers to remove duplicates caused by
    # issues having multiple labels
    df_unique = df.drop_duplicates('number')

    # group by date
    df_dt = df_unique.groupby(pandas.Grouper(key='created_dt', freq='W')) \
                     .count().cumsum()

    xdata = df_dt.index
    ydata = df_dt.open.values

    plot = PlotObject(x=xdata, y=ydata, label='open issues', style='r-')

    print('%d total' % ydata[-1])
    return plot


def open_bugs(working_dir):

    df = load_data(working_dir)

    # plot a summary of open issues
    df_open = df[df.state == 'open']

    # group open bugs by date
    df_open_bug = df_open[df_open.label == 'bug']
    df_open_bug_list = list(df_open_bug.number.values)
    df_open_bug = df_open_bug.groupby(pandas.Grouper(key='created_dt',
                                                     freq='W')) \
                             .count().cumsum()
    xdata = df_open_bug.index
    ydata = df_open_bug.number.values

    plot = PlotObject(x=xdata, y=ydata, label='open - bugs', style='r-')
    return plot

def open_enhancements(working_dir):
    
    df = load_data(working_dir)

    # plot a summary of open issues
    df_open = df[df.state == 'open']

    # group open enhancements by date
    df_open_enh = df_open[df_open.label == 'enhancement']
    df_open_enh_list = list(df_open_enh.number.values)
    df_open_enh = df_open_enh.groupby(pandas.Grouper(key='created_dt',
                                                     freq='W')) \
                             .count().cumsum()

    xdata = df_open_enh.index
    ydata = df_open_enh.number.values
    
    plot = PlotObject(x=xdata, y=ydata, label='open - enhancements', style='b-')
    return plot

def open_other(working_dir):

    df = load_data(working_dir)
    
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
                                                     freq='W')) \
                             .count().cumsum()

    xdata = df_open_non.index
    ydata = df_open_non.number.values

    plot = PlotObject(x=xdata, y=ydata, label='open - other', style='k-')
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--working-dir',
                        help='path to working directory',
                        required=True)
    parser.add_argument('--git-url',
                         help='url for github project',
                         default="https://api.github.com/repos/hydroshare/hydroshare/issues")
    parser.add_argument('--filename',
                        help='filename for the output figure',
                        default='git-issues.png')
    parser.add_argument('--figure_title',
                        help='title for output figure',
                        default='Summary of Git Issues')
    parser.add_argument('--collect',
                        help='force collection of data',
                        action='store_true')
    parser.add_argument('-a',
                        help='plot all issues',
                        action='store_true')
    parser.add_argument('-o',
                        help='plot open issues',
                        action='store_true')
    parser.add_argument('-c',
                        help='plot closed issues',
                        action='store_true')
    parser.add_argument('-b',
                        help='plot open bug tickets',
                        action='store_true')
    parser.add_argument('-e',
                        help='plot open enhancement tickets',
                        action='store_true')
    parser.add_argument('-n',
                        help='plot open non-bug, non-enhancement issues',
                        action='store_true')
    args = parser.parse_args()


    csv = os.path.join(args.working_dir, 'git_issues.csv')
    url = args.git_url

    # collect github data
    if not os.path.exists(csv) or args.collect:
        username = input('Please enter your Github username: ')
        password = getpass.getpass('Password: ')
        get_data(username, password, url, csv)
    else:
        print('--> reusing %s' % csv)

    plots = []
    if args.a:
        plots.append(all_issues(args.working_dir))
    if args.o:
        plots.append(open_issues(args.working_dir))
    if args.c:
        plots.append(closed_issues(args.working_dir))
    if args.b:
        plots.append(open_bugs(args.working_dir))
    if args.e:
        plots.append(open_enhancements(args.working_dir))
    if args.n:
        plots.append(open_other(args.working_dir))

    if len(plots) > 0:
        plot(plots, os.path.join(args.working_dir, args.filename),
             title=args.figure_title,
             ylabel='Number of Issues',
             xlabel='Date Created')
    

