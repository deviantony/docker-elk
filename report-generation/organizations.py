#!/usr/bin/env python3

import os
import pytz
import pandas
import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class PlotObject(object):
    def __init__(self, x, y, label='', style='b-', type='line'):
        self.x = x
        self.y = y
        self.label = label
        self.style = style
        self.type = type

    def get_dataframe(self):
        df = pandas.DataFrame(self.y, index=self.x, columns=[self.label])
        df.index = pandas.to_datetime(df.index)
        return df


def load_data(workingdir):

    # load the data
    path = os.path.join(workingdir, 'users.pkl')
    df = pandas.read_pickle(path)

    # convert dates
    df['date'] = pandas.to_datetime(df.usr_created_date).dt.normalize()
    df.usr_created_date = pandas.to_datetime(df.usr_created_date) \
                                .dt.normalize()
    df.usr_last_login_date = pandas.to_datetime(df.usr_last_login_date) \
                                   .dt.normalize()
    df.report_date = pandas.to_datetime(df.report_date).dt.normalize()

#    # fill NA values.  This happens when a user never logs in
#    df.usr_last_login_date = df.usr_last_login_date.fillna(0)

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

    # check that dat exist 
    if not os.path.exists(os.path.join(working_dir, 'users.pkl')):
        print('\n\tcould not find \'users.pkl\', skipping.'
              '\n\trun \'collect_hs_data\' to retrieve these missing data')

    return st, et


def plot(plotObjs_ax1, filename, plotObjs_ax2=[], *args, **kwargs):
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

    df = pandas.concat([d.get_dataframe() for d in plotObjs_ax1],
                       axis=1).fillna(0)

    for pobj in plotObjs_ax1:
        ax.plot(pobj.x, pobj.y, pobj.style, label=pobj.label)

        # annotate the last point
        ax.text(pobj.x[-1] + timedelta(days=5), # x-loc
                pobj.y[-1], # y-loc
                pobj.y[-1], # text value
                bbox=dict(boxstyle='square,pad=0.5',
                          fc='none', # foreground color
                          ec='none', # edge color
                          ))

    ax.grid()
    ax.set_xlabel('Account Creation Date')

    # add a legend
    plt.legend()

    # add monthly minor ticks
    months = mdates.MonthLocator()
    ax.xaxis.set_minor_locator(months)

    # save the figure and the data
    print('--> saving figure as %s' % filename)
    plt.savefig(filename)


def distinct_organizations(workingdir, st, et, label='', agg='1M'):

    print('--> calculating distinct organizations')

    # load the data based on working directory and subset it if necessary
    df = load_data(workingdir)
    df = subset_by_date(df, st, et)

    # drop duplicates (except the first occurrence)
    df = df.drop_duplicates(subset='usr_organization', keep='first')

    # group and cumsum
    df = df.sort_index()
    grp = agg
    ds = df.groupby(pandas.Grouper(freq=grp)) \
           .usr_organization.nunique().cumsum()

    # create plot object
    x = ds.index
    y = ds.values.tolist()
    return PlotObject(x, y, label=label, style='k-')


def distinct_us_universities(workingdir, st, et, label='', agg='1M'):

    print('--> calculating distinct US universities')

    # load the data based on working directory and subset it if necessary
    df = load_data(workingdir)
    df = subset_by_date(df, st, et)

    # drop duplicates (except the first occurrence)
    df = df.drop_duplicates(subset='usr_organization', keep='first')

    # load university data
    uni = pandas.read_csv('dat/university-data.csv')
    uni_us = list(uni[uni.country == 'us'].university)

    # subset all organizations to just the approved list of US orgs
    df_us = df[df.usr_organization.isin(uni_us)]
 #   print(df_us.usr_organization.to_string())

    # group, cumulative sum, and create plot object
    grp = agg
    df_us = df_us.sort_index()
    ds_us = df_us.groupby(pandas.Grouper(freq=grp)) \
                 .usr_organization.nunique().cumsum()
    x = ds_us.index
    y = ds_us.values.tolist()

    return PlotObject(x, y, label=label, style='b-')


def distinct_international_universities(workingdir, st, et, label='', agg='1M'):

    print('--> calculating distinct international universities')

    # load the data based on working directory and subset it if necessary
    df = load_data(workingdir)
    df = subset_by_date(df, st, et)

    # drop duplicates (except the first occurrence)
    df = df.drop_duplicates(subset='usr_organization', keep='first')

    # load university data
    uni = pandas.read_csv('dat/university-data.csv')
    uni_int = list(uni[uni.country != 'us'].university)

    # subset all organizations to just the approved list of international orgs
    df_int = df[df.usr_organization.isin(uni_int)]
#    print(df_int.usr_organization.to_string())

    # group, cumulative sum, and create plot object
    grp = agg
    df_int = df_int.sort_index()
    ds_int = df_int.groupby(pandas.Grouper(freq=grp)) \
                   .usr_organization.nunique().cumsum()
    x = ds_int.index
    y = ds_int.values.tolist()

    return PlotObject(x, y, label=label, style='r-')


def distinct_cuahsi_members(workingdir, st, et, label='', agg='1M'):

    print('--> calculating CUAHSI members')

    # load the data based on working directory and subset it if necessary
    df = load_data(workingdir)
    df = subset_by_date(df, st, et)

    # drop duplicates (except the first occurrence)
    df = df.drop_duplicates(subset='usr_organization', keep='first')

    # load cuahsi member data
    mem = pandas.read_csv('dat/cuahsi-members.csv')
    mems = list(mem.name)

    # subset all organizations to just the approved list of CUAHSI orgs
    df_mem = df[df.usr_organization.isin(mems)]
#    print(df_mem.usr_organization.to_string())

    # group, cumulative sum, and create plot object
    grp = agg
    df_mem = df_mem.sort_index()
    ds_mem = df_mem.groupby(pandas.Grouper(freq=grp)) \
                   .usr_organization.nunique().cumsum()
    x = ds_mem.index
    y = ds_mem.values.tolist()

    return PlotObject(x, y, label=label, style='g-')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='hydroshare organization'
                                                 ' statistics')
    parser.add_argument('--working-dir',
                        help='path to directory containing elasticsearch data',
                        required=True)
    parser.add_argument('--st',
                        help='reporting start date MM-DD-YYYY (UTC)',
                        default='01-01-2000')
    parser.add_argument('--et',
                        help='reporting end date MM-DD-YYYY (UTC)',
                        default=datetime.now().strftime('%m-%d-%Y'))
    parser.add_argument('--title',
                        help='title for the output figure',
                        default='Unique HydroShare Organizations')
    parser.add_argument('--filename',
                        help='filename for the output figure',
                        default='organizations.png')
    parser.add_argument('--agg',
                        help='data aggregation i.e. http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases',
                        default='1M')
    parser.add_argument('-a',
                        help='plot all distinct organizations',
                        action='store_true')
    parser.add_argument('-u',
                        help='plot distinct US organizations',
                        action='store_true')
    parser.add_argument('-i',
                        help='plot distinct international organizations',
                        action='store_true')
    parser.add_argument('-c',
                        help='plot distinct cuahsi members',
                        action='store_true')
    args = parser.parse_args()

    st, et = validate_inputs(args.working_dir, args.st, args.et)

    # set timezone to UTC
    st = pytz.utc.localize(st)
    et = pytz.utc.localize(et)

    plots = []
    if args.a:
        plots.append(distinct_organizations(args.working_dir,
                                            st,
                                            et,
                                            'All Organizations',
                                            args.agg))
    if args.u:
        plots.append(distinct_us_universities(args.working_dir,
                                              st,
                                              et,
                                              'US Universities',
                                              args.agg))
    if args.c:
        plots.append(distinct_cuahsi_members(args.working_dir,
                                             st,
                                             et,
                                             'CUAHSI Member Institutions',
                                             args.agg))
    if args.i:
        plots.append(distinct_international_universities(args.working_dir,
                                                         st,
                                                         et,
                                                         'International'
                                                         ' Universities',
                                                         args.agg))

    if len(plots) > 0:
        plot(plots,
             os.path.join(args.working_dir, args.filename),
             title=args.title,
             ylabel='Number of Organizations',
             xlabel='Account Creation Date')



