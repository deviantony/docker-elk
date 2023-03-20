#!/usr/bin/env python3 

import os
import pandas
import numpy as np
from datetime import datetime
from workbook import workbook
import matplotlib.pyplot as plt


def fig_actions_by_university(workingdir, st, et):

    """
    Create plot for sessions over time
    workingdir: directory where the activity.pkl file is located
    start_date: start of date range
    end_date: end of date range
    """

    # load the activity data
    apath = os.path.join(workingdir, 'activity.pkl')
    df = pandas.read_pickle(apath)

    # convert dates
    df['date'] = pandas.to_datetime(df.session_timestamp)

    # select dates between start/end range
    mask = (df.date >= st) & (df.date <= et)
    df = df.loc[mask]

    # replace NaN to clean xls output
    df = df.fillna('')

    # create a new column with clean university names
    df['university'] = df.edu_domain.str[:-4]

    # --- Sessions By University ---

    # isolate the session actions
    df_session = df[df.action == 'begin_session']

    # group data by edu domain
    df_session = df_session.groupby(['university']).count()

    # sort descending
    df_session = df_session.sort_values(by='session_id', ascending=False)

    # save raw data
    print('--> saving raw data')
    df_session.to_excel(os.path.join(workingdir, 'activity_by_university.xlsx'))

    # plot
    print('--> creating figure: sessions_by_university_bar.png')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df_session.session_id[1:15].plot(ax=ax, kind='barh')
    plot_margin = 1.0
    plt.xlabel('Session Count')
    plt.ylabel('University')
    plt.title('HydroShare Sessions per University')
    plt.xlabel('Session Count')
    plt.title('Number of HydroShare Sessions per University')
    plt.tight_layout()
    outpath = os.path.join(workingdir, "sessions_by_university_bar.png")
    plt.savefig(outpath)


    # --- Resource Actions By University ---

    # isolate resource actions
    action_list = ['create', 'delete', 'download']
    df_res_action = df[df.action.isin(action_list)].copy()

    # create columns for the specific actions
    df_res_action['create'] = np.where(df_res_action.action == 'create', 1, 0)
    df_res_action['delete'] = np.where(df_res_action.action == 'delete', 1, 0)
    df_res_action['download'] = np.where(df_res_action.action == 'download',
                                         1, 0)
    df_res_action['total'] = np.where(df_res_action.action.isin(action_list),
                                      1, 0)

    # group data by edu domain
    df_res_action = df_res_action.groupby(['university']).sum()

    # sort descending
    df_res_action = df_res_action.sort_values(by='total', ascending=False)

    print('--> creating figure: resource_actions_by_university_bar.png')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df_res_action[['create', 'download', 'delete']][1:15].plot(kind='barh',
                                                               stacked=True,
                                                               ax=ax)

    plt.xlabel('Session Count')
    plt.ylabel('University')
    plt.title('Resource Actions per University')
    plt.xlabel('Total Actions')
    plt.title('Total HydroShare Actions')
    plt.tight_layout()
    outpath = os.path.join(workingdir,
                           "resource_actions_by_university_bar.png")
    plt.savefig(outpath)


def fig_session_by_month(workingdir, st, et):

    """
    Create plot for sessions over time
    workingdir: directory where the activity.pkl file is located
    start_date: start of date range
    end_date: end of date range
    """

    # load the activity data
    apath = os.path.join(workingdir, 'activity.pkl')
    df = pandas.read_pickle(apath)

    # convert dates
    df['date'] = pandas.to_datetime(df.session_timestamp)

    # select dates between start/end range
    mask = (df.date >= st) & (df.date <= et)
    df = df.loc[mask]

    # replace NaN to clean xls output
    df = df.fillna('')

    # isolate the session actions
    df = df[df.action == 'begin_session']

    # change the index to timestamp
    df.set_index(['date'], inplace=True)

    # groupby month
    dfm = df.groupby(pandas.TimeGrouper('M')).count()

    # make plots
    print('--> creating figure: sessions_by_month_lines.png')
    fig = plt.figure()
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel('Session Count')
    plt.title('Number of HydroShare Sessions per Month')
    plt.plot(dfm.index, dfm.session_id,
             color='b', marker='o', linestyle='-')
    outpath = os.path.join(workingdir, "sessions_by_month_line.png")
    plt.savefig(outpath)

    print('--> creating figure: sessions_by_month_bars.png')
    fig = plt.figure()
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel('Session Count')
    plt.title('Number of HydroShare Sessions per Month')
    plt.bar(dfm.index, dfm.session_id, align='center',
            width=10, color='b')
    plt.tight_layout()
    outpath = os.path.join(workingdir, "sessions_by_month_bar.png")
    plt.savefig(outpath)


def sessions_by_month(workingdir, outxls, st, et):
    """
    Calculates total sessions by month for given date range
    start_date: start of date range
    end_date: end of date range
    """

    # load the activity data
    apath = os.path.join(workingdir, 'activity.pkl')
    df = pandas.read_pickle(apath)

    # convert dates
    df['date'] = pandas.to_datetime(df.session_timestamp)

    # select dates between start/end range
    mask = (df.date >= st) & (df.date <= et)
    df = df.loc[mask]

    # replace NaN to clean xls output
    df = df.fillna('')

    df_sessions = df[df.action == 'begin_session']
    df_applaunch = df[df.action == 'app_launch']
    df_create = df[df.action == 'create']
    df_download = df[df.action == 'download']
    df_delete = df[df.action == 'delete']

    print('--> found %d sessions ' % (df_sessions['action'].count()))
    print('--> found %d app_launch ' % (df_applaunch['action'].count()))
    print('--> found %d creates ' % (df_create['action'].count()))
    print('--> found %d downloads ' % (df_download['action'].count()))
    print('--> found %d deletes ' % (df_delete['action'].count()))

    print('--> saving session activity to xls')

    # save the activity data for the specified date range
    wb = workbook(outxls)
    sheetname = wb.add_sheet('activity')

    comments = ['# NOTES',
                '# Created on %s' % (datetime.now()),
                '\n']

    # write pandas data
#    print('--> writing dataframe to xlsx')
    cols = ['@timestamp', 'action', 'edu_domain', 'filename',
            'geoip.city_name', 'geoip.country_name', 'geoip.region_name',
            'session_id', 'session_timestamp', 'user_email_domain',
            'user_id', 'user_type']
#    df = df[cols]
#    wb.write_pandas(sheetname, df, comments)

    # write comments
    wb.write_column(0, 0, sheetname, comments)

    row_start = len(comments) + 2
    col = 0
    cols = ['@timestamp', 'action', 'edu_domain', 'filename',
            'geoip.city_name', 'geoip.country_name', 'geoip.region_name',
            'session_id', 'session_timestamp', 'user_email_domain',
            'user_id', 'user_type']
    for col_name in cols:
        print('--> writing %s to xlsx' % col_name)
        data = df[col_name].tolist()
        data.insert(0, col_name)
        wb.write_column(row_start, col, sheetname, data)
        col += 1
    wb.save()


def resource_types_by_month(workingdir, outxls, st, et):
    """
    Calculates total sessions by month for given date range
    start_date: start of date range
    end_date: end of date range
    """
    
    print('--> loading resource statistics')

    # load the activity data
    apath = os.path.join(workingdir, 'resources.pkl')
    df = pandas.read_pickle(apath)

    # convert dates
    df['date'] = pandas.to_datetime(df.res_date_created)

    # select dates between start/end range
    mask = (df.date >= st) & (df.date <= et)
    df = df.loc[mask]

    # replace NaN to clean xls output
    df = df.fillna('')

    # change the index to timestamp
    df.set_index(['date'], inplace=True)

    # groupby month
    dfm = df.groupby([pandas.TimeGrouper('M'), df.res_type]).count()

#    df_sessions = df[df.action == 'begin_session']
#    df_applaunch = df[df.action == 'app_launch']
#    df_create = df[df.action == 'create']
#    df_download = df[df.action == 'download']
#    df_delete = df[df.action == 'delete']
#
#    print('--> found %d sessions ' % (df_sessions['action'].count()))
#    print('--> found %d app_launch ' % (df_applaunch['action'].count()))
#    print('--> found %d creates ' % (df_create['action'].count()))
#    print('--> found %d downloads ' % (df_download['action'].count()))
#    print('--> found %d deletes ' % (df_delete['action'].count()))
#
    print('--> saving resource statistics')

    # save the activity data for the specified date range
    wb = workbook(outxls)
    sheetname = wb.add_sheet('resource_types')

    comments = ['# NOTES',
                '# Created on %s' % (datetime.now()),
                '\n']

    # write pandas data
#    print('--> writing dataframe to xlsx')
    cols = ['@timestamp', 'res_created_dt_str',
            'res_date_created', 'res_pub_status',
            'res_size', 'usr_id', 'usr_type']

    # write comments
    wb.write_column(0, 0, sheetname, comments)

    row_start = len(comments) + 2
    col = 0
    for col_name in cols:
        print('--> writing %s to xlsx' % col_name)
        data = df[col_name].tolist()
        data.insert(0, col_name)
        wb.write_column(row_start, col, sheetname, data)
        col += 1
    wb.save()
