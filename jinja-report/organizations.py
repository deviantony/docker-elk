#!/usr/bin/env python3

import os
import pandas
from datetime import datetime
from pandas.plotting import register_matplotlib_converters

import plot

register_matplotlib_converters()


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


#def total_table(input_directory='.',
#                start_time=datetime(2000, 1, 1),
#                end_time=datetime(2030, 1, 1),
#                num_records=50)
#    
#    print('--> calculating total distinct organizations - table')
#
#    # load the data based on working directory and subset it if necessary
#    df = load_data(input_directory)
#    df = subset_by_date(df, start_time, end_time)
#
#    # drop duplicates (except the first occurrence)
#    df = df.drop_duplicates(subset='usr_organization', keep='first')
#
#    # group and cumsum
#    df = df.sort_index()
#    ds = df.groupby(pandas.Grouper(freq=aggregation)) \
#           .usr_organization.nunique().cumsum()
#    
#    import pdb; pdb.set_trace()
#
#    # create plot object
#    x = ds.index
#    y = ds.values.tolist()


def total(input_directory='.',
          start_time=datetime(2000, 1, 1),
          end_time=datetime(2030, 1, 1),
          label='',
          aggregation='1M',
          linestyle='-',
          color='k',
          **kwargs):

    print('--> calculating total distinct organizations')

    # load the data based on working directory and subset it if necessary
    df = load_data(input_directory)
    df = subset_by_date(df, start_time, end_time)

    # drop duplicates (except the first occurrence)
    df = df.drop_duplicates(subset='usr_organization', keep='first')

    # group and cumsum
    df = df.sort_index()
    ds = df.groupby(pandas.Grouper(freq=aggregation)) \
           .usr_organization.nunique().cumsum()

    # create plot object
    x = ds.index
    y = ds.values.tolist()
    return plot.PlotObject(x,
                           y,
                           label=label,
                           linestyle=linestyle,
                           color=color,
                           )


def us_universities(input_directory='.',
                    start_time=datetime(2000, 1, 1),
                    end_time=datetime(2030, 1, 1),
                    label='',
                    aggregation='1M',
                    linestyle='-',
                    color='k',
                    **kwargs):

    print('--> calculating distinct US universities')

    # load the data based on working directory and subset it if necessary
    df = load_data(input_directory)
    df = subset_by_date(df, start_time, end_time)

    # drop duplicates (except the first occurrence)
    df = df.drop_duplicates(subset='usr_organization', keep='first')

    # load university data
    uni = pandas.read_csv('dat/university-data.csv')
    uni_us = list(uni[uni.country == 'us'].university)

    # subset all organizations to just the approved list of US orgs
    df_us = df[df.usr_organization.isin(uni_us)]

    # group, cumulative sum, and create plot object
    df_us = df_us.sort_index()
    ds_us = df_us.groupby(pandas.Grouper(freq=aggregation)) \
                 .usr_organization.nunique().cumsum()
    x = ds_us.index
    y = ds_us.values.tolist()

    return plot.PlotObject(x,
                           y,
                           label=label,
                           linestyle=linestyle,
                           color=color)


def international_universities(input_directory='.',
                               start_time=datetime(2000, 1, 1),
                               end_time=datetime(2030, 1, 1),
                               label='',
                               aggregation='1M',
                               linestyle='-',
                               color='k',
                               **kwargs):


    print('--> calculating distinct international universities')

    # load the data based on working directory and subset it if necessary
    df = load_data(input_directory)
    df = subset_by_date(df, start_time, end_time)

    # drop duplicates (except the first occurrence)
    df = df.drop_duplicates(subset='usr_organization', keep='first')

    # load university data
    uni = pandas.read_csv('dat/university-data.csv')
    uni_int = list(uni[uni.country != 'us'].university)

    # subset all organizations to just the approved list of international orgs
    df_int = df[df.usr_organization.isin(uni_int)]

    # group, cumulative sum, and create plot object
    df_int = df_int.sort_index()
    ds_int = df_int.groupby(pandas.Grouper(freq=aggregation)) \
                   .usr_organization.nunique().cumsum()
    x = ds_int.index
    y = ds_int.values.tolist()

    return plot.PlotObject(x,
                           y,
                           label=label,
                           linestyle=linestyle,
                           color=color)


def cuahsi_members(input_directory='.',
                   start_time=datetime(2000, 1, 1),
                   end_time=datetime(2030, 1, 1),
                   label='',
                   aggregation='1M',
                   linestyle='-',
                   color='k',
                   **kwargs):

    print('--> calculating CUAHSI members')

    # load the data based on working directory and subset it if necessary
    df = load_data(input_directory)
    df = subset_by_date(df, start_time, end_time)

    # drop duplicates (except the first occurrence)
    df = df.drop_duplicates(subset='usr_organization', keep='first')

    # load cuahsi member data
    mem = pandas.read_csv('dat/cuahsi-members.csv')
    mems = list(mem.name)

    # subset all organizations to just the approved list of CUAHSI orgs
    df_mem = df[df.usr_organization.isin(mems)]

    # group, cumulative sum, and create plot object
    df_mem = df_mem.sort_index()
    ds_mem = df_mem.groupby(pandas.Grouper(freq=aggregation)) \
                   .usr_organization.nunique().cumsum()
    x = ds_mem.index
    y = ds_mem.values.tolist()

    return plot.PlotObject(x,
                           y,
                           label=label,
                           linestyle=linestyle,
                           color=color)
