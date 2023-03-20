#!/usr/bin/env python3

import os
import pickle
import signal
import datetime
import argparse
import pandas as pd
import hs_restclient as hsapi
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()


def check_pub(q, out_q):
    while True:
        resid = q.get()
        if resid is None:
            return

        with Timeout(10):
            scimeta = hs.getScienceMetadata(resid)
            funding = scimeta['funding_agencies']

            # add more metadata
            extra = dict(res_title=scimeta['title'],
                         res_id=resid)

            print('.', end='', flush=True)
            if len(funding) > 0:
                print('|', end='')
                for fund in funding:
                    d = {**fund, **extra}
                    out_q.put(d)


def split_date_range(n):
    begin = datetime.date(2015, 5, 1)
    end = datetime.datetime.now().date()
    intervals = n

    date_list = []
    delta = (end - begin)/intervals
    st = begin
    for i in range(1, intervals + 1):
        et = begin+i*delta
        date_list.append([st, et])
        st = et

    return date_list


def collect_resource_ids(hs):
    dat = []
    resources = hs.resources(published=True)
    for resource in resources:
        meta = hs.getScienceMetadata(resource['resource_id'])
        dates = {}
        for dt in meta['dates']:
            dates[dt['type']] = dt['start_date']
        if 'published' not in dates:
            print(f'\nERROR: {resource["resource_id"]} doesn\'t contain '
                  'published date')
            continue

        data = dict(resource_id=resource['resource_id'],
                    owner_id=meta['creators'][0]['description'],
                    created_dt=dates['created'],
                    last_modified_dt=dates['modified'],
                    published_dt=dates['published'])
        dat.append(data)

    df = pd.DataFrame(dat)

    # convert columns to datetime objects
    df['created_dt'] = pd.to_datetime(df['created_dt'])
    df['last_modified_dt'] = pd.to_datetime(df['last_modified_dt'])
    df['Date Published'] = pd.to_datetime(df['published_dt'])
    df['resource_count'] = 1

    return df


def plot_line(df, filename, title='',
              agg='1M', width=.5, annotate=False,
              **kwargs):

    # create figure of these data
    fig, ax = plt.subplots(figsize=(12, 9))

    df['Published Resource Count'] = df.resource_count
    df = df.groupby(pd.Grouper(key="Date Published", freq=agg))
    df = df.sum().fillna(0)

    ax.bar(df.index, df['Published Resource Count'], width=width)

    if annotate:
        for p in ax.patches:
            ax.annotate("%.2f" % p.get_height(),
                        (p.get_x() + p.get_width() / 2.,
                         p.get_height()),
                        ha='center',
                        va='center',
                        xytext=(0, 10),
                        textcoords='offset points')

    # set plot attributes
    for k, v in kwargs.items():
        try:
            getattr(ax, 'set_'+k)(v)
        except AttributeError:
            pass

    # add a legend
    plt.legend()

    # add monthly minor ticks
    plt.subplots_adjust(bottom=0.25)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    fig.suptitle(title)
    ax.set_ylabel('Published Resource Count')

    # save the figure and the data
    print('--> saving figure as %s' % filename)
    plt.savefig(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='doi statistics')
    parser.add_argument('--working-dir',
                        help='path to working directory',
                        required=True)
    parser.add_argument('--agg',
                        help='timestep aggregation for summarizing data, '
                             'e.g. 1D, 3M, etc',
                        default='1M')
    parser.add_argument('--filename',
                        help='filename for the output figure',
                        default='hs-published.png')
    parser.add_argument('--title',
                        help='figure title',
                        default='HydroShare Published Resources')
    parser.add_argument('--bar-width',
                        help='width of bars in the plot',
                        type=float,
                        default=.5)
    parser.add_argument('--annotate',
                        help='turn on bar plot annotations',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    # define the names of the pkl files that will be created
    published = os.path.join(args.working_dir,
                             'published_resources.pkl')
    resources_list = os.path.join(args.working_dir,
                                  'published_resources_list.pkl')

    # collect data for HydroShare
    print('--> collecting published resource metadata ... ',
          flush=True, end='')
    pub_pkl_exists = os.path.exists(published)
    if not (pub_pkl_exists):
        # connect to HS
        hs = hsapi.HydroShare()

        # collect metadata for published resources
        resources = collect_resource_ids(hs)
        with open(published, 'wb') as f:
            pickle.dump(resources, f)
        print('done')
    else:
        print('skipping')

    print('--> loading data')
    df = pd.read_pickle(published)

    # plot published by date
    print('--> making plot')
    outpath = os.path.join(args.working_dir, args.filename)
    plot_line(df,
              outpath,
              title=args.title,
              agg=args.agg,
              width=args.bar_width,
              annotate=args.annotate)

    print('SUCCESS')


