#!/usr/bin/env python3 

import os
import csv
import pandas
import argparse
import numpy as np
from tabulate import tabulate
from datetime import datetime, timedelta
from workbook import workbook
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class PlotObject(object):
    def __init__(self, x, y, label='', style='b-'):
        self.x = x
        self.y = y
        self.label = label
        self.style = style


class Users(object):

    def __init__(self, workingdir, outxls, st, et):

        self.workingdir = workingdir
        self.outxls = outxls
        self.st = st
        self.et = et
        self.df = self.load_data()

    def load_data(self):

        print('--> reading user statistics ')
        # load the activity data
        path = os.path.join(self.workingdir, 'users.pkl')
        df = pandas.read_pickle(path)

        # convert dates
        df['date'] = pandas.to_datetime(df.usr_created_date).dt.normalize()

        df.usr_created_date = pandas.to_datetime(df.usr_created_date).dt.normalize()
        df.usr_last_login_date = pandas.to_datetime(df.usr_last_login_date).dt.normalize()
        df.report_date = pandas.to_datetime(df.report_date).dt.normalize()
        # fill NA values.  This happens when a user never logs in
        df.usr_last_login_date = df.usr_last_login_date.fillna(0)

        # replace NaN to clean xls output
        df = df.fillna('')

        # add another date column and make it the index
        df['Date'] = df['date']

        # change the index to timestamp
        df.set_index(['Date'], inplace=True)

        return df

    def users_over_time(self):
        """
        Calculate total users over time
        """
        output = OrderedDict()
        df = self.df.sort_index()


        print('--> calculating rolling statistics... ', end='', flush=True)
        res = []
        t = df['usr_created_date'].min()

        activerange = 90
        output['dates'] = []
        output['total-users'] = []
        output['active-users'] = []
        output['new-users'] = []
        output['returning-users'] = []

        while t < self.et:

            output['dates'].append(t)

            # subset all users to those that exist up to the current time, t
            subdf = df[df.usr_created_date <= t]

            # total users up to time, t
            output['total-users'].append(subdf.usr_created_date.count())

            # The number of new users in activerange up to time dateJoined[i] (i.e. the range 1:i) are users who 
            # created their account after dateJoine[i]-activerange
            earliest_date = t - timedelta(days=activerange)
            output['new-users'].append(np.where((subdf.usr_created_date >= earliest_date) &
                                                (subdf.usr_created_date <= t),
                                                1, 0).sum())

            account_age = (t - subdf.usr_created_date).astype('timedelta64[D]')
#            output['new-users'].append(np.where((account_age <= activerange) &
#                                                (account_age >= 0),
#                                                1, 0).sum())

            # The number of users active at time dateJoined[i] is all who created an account before dateJoined[i]
            # i.e. the range 1:i, who have logged in after dateJoine[i]-activerange
            output['active-users'].append((subdf.usr_last_login_date > (t - timedelta(days=activerange))).sum())
#            days_since_login = (t - subdf.usr_last_login_date).astype('timedelta64[D]')


            # Users who were active on the site in the last 90 days,
            # but obtained an account prior to the last 90 days are people who
            # continue to return to and work with HydroShare.
            output['returning-users'].append(output['active-users'][-1] - output['new-users'][-1])
#        output['returning-users'].append(np.where((days_since_login <= activerange) &
#                                                      (days_since_login >= 0) &
#                                                      (account_age > activerange),
#                                                      1, 0).sum())
            t += timedelta(days=1)

        opath = os.path.join(self.workingdir, 'user-stats.csv')
        with open(opath, 'w') as f:
            f.write('%s\n' % (','.join(list(output.keys()))))
            for i in range(0, len(output['dates'])):
                for k in output.keys():
                    f.write('%s,' % str(output[k][i]))
                f.write('\n')
        opath = os.path.join(self.workingdir, 'user-statistics.README')
        with open(opath, 'w') as f:
            f.write('The following assumptions are made when deriving '
                    'HS user statistics:\n\n'
                    '1. New users are those who created an account within the [active range] of the current date [t]. For example, NewUser = True if:\n  - ([t] - [active range]) <= [date joined] <= [t] \n\n'
                    '2. Active users are defined as those who created an account before time [t] and have logged into HS within the [active range] or have created a new account within the [active rage]. For example, ActiveUser = True if:\n  - ([date joined] < [t]) AND ([t] - [active range]) <= [last login] <= [t]\n  - OR ([t] - [active range]) <= [date joined] <= [t]\n')

        print('done', flush=True)

        print('--> creating user statistics figures... ', end='', flush=True)

        def makefig(title, xlabel, ylabel, dic, filename):
            fig = plt.figure()
            plt.xticks(rotation=45)
            plt.subplots_adjust(bottom=0.15)
            plt.ylabel(ylabel)
            plt.xlabel(xlabel)
            plt.title(title)

            xdata = output['dates']
            for s in dic:
                plt.plot(xdata, output[s[0]], color=s[1], linestyle=s[2],
                         label=s[3])
            plt.legend()
            plt.tight_layout()
            outpath = os.path.join(self.workingdir, filename)
            plt.savefig(outpath)

        series = [['total-users', 'k', '-', 'Total'],
                  ['active-users', 'b', '--', 'Active (last 90 days)'],
                  ['new-users', 'r', '--', 'New (last 90 days)']]

        makefig('HydroShare Users as of %s' % (self.et.strftime('%Y-%m-%d')),
                'Date',
                'Number of Users',
                series,
                '1-all-users-overview.png')

        series = [['active-users', 'k', '-', 'Active (last 90 days)'],
                  ['new-users', 'r', '--', 'New (last 90 days)'],
                  ['returning-users', 'b', '--', 'Returned (last 90 days)']]

        makefig('Active HydroShare Users as of %s' % (self.et.strftime('%Y-%m-%d')),
                'Date',
                'Number of Users',
                series,
                '2-active-users-overview.png')

        print('done', flush=True)


    def subset_df_by_date(self, df):

        # select dates between start/end range
        mask = (df.date >= self.st) & (df.date <= self.et)
        df = df.loc[mask]

    def subset_series_by_date(self, series):

        # select dates between start/end range
        mask = (series.index >= self.st) & (series.index <= self.et)
        return series.loc[mask]

    def save(self):

        # save raw data
        print('--> saving raw data')

        # save the activity data for the specified date range
        wb = workbook(self.outxls)
        sheetname = wb.add_sheet('users')

        comments = ['# NOTES',
                    '# Created on %s' % (datetime.now()),
                    '\n']

        # write pandas data
        cols = list(self.df.columns)

        # write comments
        wb.write_column(0, 0, sheetname, comments)

        row_start = len(comments) + 2
        col = 0
        for col_name in cols:
            print('--> writing %s to xlsx' % col_name)
            data = self.df[col_name].tolist()
            data.insert(0, col_name)
            wb.write_column(row_start, col, sheetname, data)
            col += 1
        wb.save()

    def user_stats(self):

        def next_quarter(dt0):
            dt1 = dt0.replace(day=1)
            dt2 = dt1 + timedelta(days=32 * 4)
            dt3 = dt2.replace(day=1)
            dt4 = dt3 - timedelta(days=1)
            return dt4

        df = self.load_data()

        # calculate cumulative users
        df = df.groupby(pandas.TimeGrouper('d')).count().usr_id.cumsum()
        df.index[-1]

        qt = datetime(2016, 1, 31)
        data = []
        while qt < df.index[-1]:
            dtstr = qt.strftime('%Y-%m-%d')
            data.append([dtstr, df[dtstr]])
            qt = next_quarter(qt)
        last = df.index.max().strftime('%Y-%m-%d')
        data.append([last, df[last]])

        for i in range(1, len(data)):
                users0 = data[i-1][1]
                users1 = data[i][1]
                diff = users1 - users0
                pct = round(diff / (users1) * 100, 2)
                data[i].extend([diff, pct])
        headers = ["Date", "Total Users", "New Users", "Percent Change"]
        print(tabulate(data, headers))


#        print(data)


    def all(self):

        self.users_over_time()
        self.users_active()
        self.users_new()

        # determine if a users is new or retained
        self.df['retained'] = np.where((self.df.active90 == 1)
                                       & (self.df.isnew == 0), 1, 0)

        # plot
        print('--> creating figure: users-combined.png')
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.30)
        plt.ylabel('User Count')
        plt.xlabel('Account Creation Date')
        plt.title('HydroShare Users Summary')

        dfm = self.df.groupby(pandas.TimeGrouper('d')).count().usr_id.cumsum()
        dfm = self.subset_series_by_date(dfm)
        dfm = dfm.fillna(method='pad')
        plt.plot(dfm.index, dfm,
                 color='k', linestyle='--', label='All Users')

        dfm = self.df.groupby(pandas.TimeGrouper('d')).sum().active90.cumsum()
        dfm = self.subset_series_by_date(dfm)
        dfm = dfm.fillna(method='pad')
        plt.plot(dfm.index, dfm,
                 color='b', linestyle='-', label='Active Users - 90 days')

#        dfm = self.df.groupby(pandas.TimeGrouper('d')).sum().isnew.cumsum()
#        dfm = dfm.fillna(method='pad')
#        plt.plot(dfm.index, dfm,
#                 color='g', linestyle='-', label='New Users')
#
#        dfm = self.df.groupby(pandas.TimeGrouper('d')).sum().retained.cumsum()
#        dfm = dfm.fillna(method='pad')
#        plt.plot(dfm.index, dfm,
#                 color='r', linestyle='-', label='Retained Users')

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)

        outpath = os.path.join(self.workingdir, "users-combined.png")
        plt.savefig(outpath)

        self.df.to_pickle(os.path.join(self.workingdir, 'df.pkl'))


    def users_active(self):

        """
        Calculate total users over time
        workingdir: directory where the users.pkl file is located
        start_date: start of date range
        end_date: end of date range
        """

        # determine active status
        self.df['active90'] = (self.df.usr_last_login_date - self.df.usr_created_date).astype('timedelta64[D]')
        self.df.loc[(self.df.active90 > 0) & (self.df.active90 < 91), 'active90'] = 1
        self.df.loc[self.df.active90 != 1, 'active90'] = 0

        # save changes back to global df
        dfm = self.df.copy()

        # groupby day, and calculate the cumsum
        dfm = dfm.groupby(pandas.TimeGrouper('W')).sum().active90.cumsum()
        dfm = self.subset_series_by_date(dfm)

        # plot
        print('--> creating figure: users-active.png')
        fig = plt.figure()
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.15)
        plt.ylabel('Number of Total Users')
        plt.xlabel('Account Creation Date')
        plt.title('Users Active in last 90 Days')
        plt.plot(dfm.index, dfm,
                 color='b', linestyle='-')
        outpath = os.path.join(self.workingdir, "users-active.png")
        plt.savefig(outpath)

    def generate_user_overview(self, *args, c=1, n='W'):
        aggregation = '%d%s' % (int(c), n)
        dfa = self.df.groupby(pandas.Grouper(key='date',
                              freq=aggregation))
        df = self.read_user_login_activity(agg_count=int(c),
                                           agg_name=n)
        for arg in args:
            if arg == 'all':
                self.generate_all_user_overview(dfa=dfa, dfu=df)
            elif arg == 'active':
                self.generate_active_user_overview(df)
        if len(args) == 0:
            self.generate_all_user_overview(dfa=dfa, dfu=df)
            self.generate_active_user_overview(df)


    def generate_all_user_overview(self, dfa, dfu):
        """
        Generates a figure that summarizes all users over the
        current time frame.
        """

        # determine the number of active users through time by
        # aggregating the sum of logins from unique users through
        # time.
        print('--> calculating unique ids')
        dfa = dfa.usr_id.nunique()

        # remove the first and last dates because these likely have
        # incomplete data and will skew the figure.
        dfa = dfa[1:-1]

        # create plot object
        plotObj = PlotObject(dfa.index,
                             dfa.cumsum(),
                             label='All Users',
                             style='k.-')

        plts = []
        plts.append(plotObj)

        active_plt = self.get_active_users(dfu)
        active_plt.style = 'b.-'
        plts.append(active_plt)

        plts.append(self.get_new_users(dfu))

#        import pdb; pdb.set_trace()
#        minx = dfu.user_id.nunique().index.min()
#        maxx = dfu.user_id.nunique().index.max()

        minx = dfu.date.min()
        maxx = dfu.date.max()
        self.plot(plts,
                  'hs-all-user-overview',
                  **dict(title='HydroShare Users',
                         xlabel='Time',
                         ylabel='Number of Users'),
                         xlim=(minx, maxx))

    def generate_active_user_overview(self, df):
        """
        Generates a figure that summarizes user activity over the
        current time frame.
        """
        plts = []
        dat = self.get_active_users(df)
        dat.style = 'k-'
        plts.append(dat)

        dat = self.get_new_users(df)
        dat.style = 'r-'
        plts.append(dat)
        
        dat = self.get_returning_users(df)
        dat.style = 'b-'
        plts.append(dat)

        self.plot(plts,
                  'hs-active-user-overview',
                  **dict(title='HydroShare Users',
                         xlabel='Time',
                         ylabel='Number of Users'))

    def read_user_login_activity(self, agg_count=1, agg_name='M'):
        # load the activity logs
        print('--> reading data')
        activity_path = os.path.join(self.workingdir, 'activity.pkl')
        df = pandas.read_pickle(activity_path)

        # create a date column based on the session_timestamp
        # object that is stored in the elasticsearch database.
        # this will be used to group the data by date range.
        print('--> creating date column')
        df['date'] = pandas.to_datetime(df.session_timestamp)

        # select only the data for action=login. This metric
        # will be used to show the number of active users at any
        # given time frame
        print('--> subsetting login actions')
        df = df[df.action == 'login']
        df.to_csv('raw_data.csv')

        return df
    
    def get_active_users(self, df, n=90):

        """
        Calculate total active users based on activity logs
        """

        print('--> calculating active users, n=%d' % n)

        curr_dt = df.date.min().date()
        end_dt = df.date.max().date()
        dates, active_count = ([], [])
        while curr_dt < end_dt:
            print('.', end='', flush=True)
            dt_n = curr_dt - timedelta(days=n)
            d = df[(df['date'] <= curr_dt) &
                   (df['date'] >= dt_n)]
            dates.append(curr_dt)
            active_count.append(d.user_id.nunique())

            curr_dt += timedelta(days=1)

        print('\n')

        # create plot object
        plotObj = PlotObject(dates,
                             active_count,
                             label='Total Active Users',
                             style='k.-')
        return plotObj
    
    def get_new_users(self, df, n=90):

        """
        Calculate total new users based on activity logs
        """

        print('--> calculating new users, n=%d' % n)
        curr_dt = df.date.min().date()
        end_dt = df.date.max().date()
        dates, new_count = ([], [])
        while curr_dt < end_dt:
            print('.', end='', flush=True)
            dt_n = curr_dt - timedelta(days=n)
            d = df[(df['date'] <= curr_dt) &
                   (df['date'] >= dt_n)]

            # isolate the records that are older than "n" days, i.e.
            # < dt_n
            d_old = df[(df['date'] < dt_n)]

            # isolate the users that have been active before the
            # current time period
            old_users = set(d_old.user_id.unique())

            # isolate the users that have been active in the
            # current time period, i.e. dt_n <= dt <= curr_dt
            curr_users = set(d.user_id.unique())

            # calculate curr users that are not in old_users
            new_count.append(len(curr_users - old_users))
            dates.append(curr_dt)

            curr_dt += timedelta(days=1)

        print('\n')

        # create plot object
        plotObj = PlotObject(dates,
                             new_count,
                             label='New Users',
                             style='r.-')
        return plotObj

    def get_returning_users(self, df, n=90):

        """
        Calculate total returning users based on activity logs
        """

        print('--> calculating returning users, n=%d' % n)
        curr_dt = df.date.min().date()
        end_dt = df.date.max().date()
        dates, ret_count = ([], [])
        while curr_dt < end_dt:
            print('.', end='', flush=True)
            dt_n = curr_dt - timedelta(days=n)
            d = df[(df['date'] <= curr_dt) &
                   (df['date'] >= dt_n)]

            # isolate the records that are older than "n" days, i.e.
            # < dt_n
            d_old = df[(df['date'] < dt_n)]

            # isolate the users that have been active before the
            # current time period
            old_users = set(d_old.user_id.unique())

            # isolate the users that have been active in the
            # current time period, i.e. dt_n <= dt <= curr_dt
            curr_users = set(d.user_id.unique())

            # calculate curr users that are not in old_users
            ret_count.append(len(curr_users & old_users))
            dates.append(curr_dt)

            curr_dt += timedelta(days=1)

        print('\n')

        # create plot object
        plotObj = PlotObject(dates,
                             ret_count,
                             label='Returning Users',
                             style='b.-')
        return plotObj


    def plot(self, plotObjs_ax1, filename, plotObjs_ax2=[], **kwargs):
        """
        Creates a figure give plot objects
        plotObjs: list of plot object instances
        filename: output name for figure *.png
        **kwargs: matplotlib plt args, e.g. xlabel, ylabel, title, etc
        """

        # create figure of these data
        print('\n--> making figure...')
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
        print('--> saving figure ...')
        outpath = os.path.join(self.workingdir, filename)
        print(' --> %s' % outpath)
        plt.savefig(outpath)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='general user statistics')
    parser.add_argument('--working-dir', help='path to directory containing elasticsearch data',
            required=True)
    parser.add_argument('--out-xlsx', help='path to output xlsx file', default='stats.xlsx')
    parser.add_argument('--st', help='start time MM-DD-YYYY', default='01-01-2000')
    parser.add_argument('--et', help='start time MM-DD-YYYY', default=datetime.now().strftime('%m-%d-%Y'))
    args = parser.parse_args()

    # check date formats
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

    # save user data, check that pickle files exist before saving
    if not os.path.exists(os.path.join(args.working_dir, 'activity.pkl')):
        print('\n\tcould not find \'activity.pkl\', skipping.'
              '\n\trun \'collect_hs_data\' to retrieve these missing data')
    else:
        print('Running <User> Statistics Using:')
        print('Working Directory: %s' % args.working_dir)
        print('Out Xlsx: %s' % args.out_xlsx)
        print('Start Date: %s' % str(st))
        print('End Date: %s' % str(et))

        # generate statistics
        user = Users(args.working_dir, args.out_xlsx, st, et)
        user.user_stats()
        user.generate_user_overview()








