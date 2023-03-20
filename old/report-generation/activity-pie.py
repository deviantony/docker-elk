#!/usr/bin/env python3

import os
import pytz
import pandas
import argparse
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


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


def downloads_by_type(working_dir, st, et, drop_cols,
                      figtitle,
                      filename='hydroshare-downloads-by-types.png'):

    # load the data based on working directory
    df = load_data(working_dir)
    df = df.sort_index()
    df = df[df.action == 'download']
    df = subset_by_date(df, st, et)
    df = df[~df.user_type.isnull()]

    df = df.filter(items=['user_type'])
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
        df[u] = np.where(df['user_type'] == u, 1, 0)
    df['Other'] = np.where(~df['user_type'].isin(user_types), 1, 0)

    # remove 'usr_type' b/c it's no longer needed
    df = df.drop('user_type', axis=1)

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

    # remove where percentage is 0.00
    df = df[df.score > 0]
    df = df.sort_values(by='percent', ascending=False)

    labels = list(df.index)
    values = list(df.percent)

    # hard coded: move undergrad away from com/professional b/c they overlap
    idx = len(labels) - 1
    labels.insert(2, labels.pop(idx))
    values.insert(2, values.pop(idx))

    ax.pie(values, labels=labels)
#    pi = df.percent.plot.pie(ax=ax, explode=explode, labeldistance=1.1, startangle=10)

#    bbox_props = dict(boxstyle="square,pad=0.5", fc="w", ec="k", lw=0)
#    kw = dict(arrowprops=dict(arrowstyle="-"),
#              bbox=bbox_props, zorder=0, va="center")
#    texts = [t for t in pi.texts]
#
#    import pdb; pdb.set_trace()
#    total_patches = len(pi.patches)
#    pop_idx = 0
#    for i in range(0, total_patches):
#        p = pi.patches[i]
#        text = pi.texts.pop(pop_idx)
##        if text.get_text() == '':
##            continue
#        pop_idx += 1
#
#        ang = (p.theta2 - p.theta1)/2. + p.theta1
#        y = np.sin(np.deg2rad(ang))
#        x = np.cos(np.deg2rad(ang))
#        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
#        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
#        kw["arrowprops"].update({"connectionstyle": connectionstyle})
#
#        ax.annotate(text.get_text(), xy=(x, y),
#                    xytext=(1.35*np.sign(x), 1.4*y),
#                    horizontalalignment=horizontalalignment, **kw)

    plt.xlabel('')
    plt.ylabel('')

    # save the figure and the data
    print('--> saving figure as %s' % filename)
    outpath = os.path.join(working_dir, filename)
    plt.savefig(outpath, bbox_inches="tight")


def downloads_by_specified(working_dir, st, et, figtitle,
                           filename='downloads-known-vs-unknown.png'):

    # load the data based on working directory
    df = load_data(working_dir)
    df = df.sort_index()
    df = df[df.action == 'download']
    df = subset_by_date(df, st, et)

    # user type is not specified for "anonymous" users
    total_downloads = len(df)
    unknown_user_downloads = len(df[df.user_type.isnull()])
    known_user_downloads = total_downloads - unknown_user_downloads

    # count number of users for each type
    df = pandas.DataFrame({'type': ['Unknown', 'HydroShare Users'],
                           'score': [unknown_user_downloads,
                                     known_user_downloads]
                           })
    df = df.set_index('type')
    df['percent'] = round(df['score']/df['score'].sum()*100, 2)
    df = df.rename({'Unknown': 'Unknown (%2.2f%%)' %
                                 (df.loc['Unknown'].percent)})
    df = df.rename({'HydroShare Users': 'HydroShare Users (%2.2f%%)' %
                                     (df.loc['HydroShare Users'].percent)})

    # make pie chart
    print('--> making pie chart...')
    fig = plt.figure(figsize=(10, 10))
    plt.title(figtitle)

    def make_autopct(values, scores):
        def my_autopct(pct):
            idx = np.argmin(abs(values - pct))
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=scores[idx])
        return my_autopct

    labels = ['Unknown', 'HydroShare Users']
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
                        default='HydroShare User Type Distribution %s'
                        % datetime.now().strftime('%m-%d-%Y'))
    parser.add_argument('--filename',
                        help='output figure name',
                        default='hydroshare-downloads.png')
    parser.add_argument('--st',
                        help='start time MM-DD-YYYY (UTC)',
                        default='01-01-2000')
    parser.add_argument('--et',
                        help='start time MM-DD-YYYY (UTC)',
                        default=datetime.now().strftime('%m-%d-%Y'))
    parser.add_argument('--exclude',
                        help='comma separated list of user types to exclude',
                        type=str, default=',')
    parser.add_argument('-k',
                        help='plot pie chart of downloads for known users',
                        action='store_true')
    parser.add_argument('-u',
                        help='plot pie chart of downloads: known and unknown',
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

    # set timezone to UTC
    st = pytz.utc.localize(st)
    et = pytz.utc.localize(et)

    # check that dat exist
    if not os.path.exists(os.path.join(args.working_dir, 'users.pkl')):
        print('\n\tcould not find \'users.pkl\', skipping.'
              '\n\trun \'collect_hs_data\' to retrieve these missing data')
    else:
        if args.k:
            downloads_by_type(args.working_dir, st, et,
                              excludes,
                              args.figure_title,
                              args.filename)
        if args.u:
            downloads_by_specified(args.working_dir, st, et,
                                   args.figure_title,
                                   args.filename)
