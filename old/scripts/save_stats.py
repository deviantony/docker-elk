#!/usr/bin/env python3

import os
import datetime
import pandas as pd
from workbook import workbook


def save_anon_users(working_dir, out_xls_path):
    """
    Anonymize user metrics and save to excel document
    working_dir: path of the current working directory.  This assumes that,
                 users.pkl exists in this directory.
    """

    # prepare the workbook
    wb = workbook(out_xls_path)
    sheetname = wb.add_sheet('users')

    # read data
    u = pd.read_pickle(os.path.join(working_dir, 'users.pkl'))

    u['created_dt'] = pd.to_datetime(u['usr_created_date'])
    u['login_dt'] = pd.to_datetime(u['usr_last_login_date'])
    u['days_since_login'] = (u['login_dt'] - u['created_dt']).dt.days
    u['account_activated'] = True

    # replace negatives (strange there are many negatives)
    u.ix[u.days_since_login < 1, 'days_since_login'] = -998

    # fill na
    u.ix[u.days_since_login.isnull(), 'account_activated'] = False
    u['days_since_login'] = u['days_since_login'].fillna(value=-999)

    # remove sensitive info
    u = u.drop('usr_email', 1)
    u = u.drop('usr_firstname', 1)
    u = u.drop('usr_lastname', 1)

    # remove unnecessary data
    u = u.drop('@timestamp', 1)
    u = u.drop('offset', 1)
    u = u.drop('report_date', 1)
    u = u.drop('rpt_dt_str', 1)
    u = u.drop('usr_created_date', 1)
    u = u.drop('usr_last_login_date', 1)
    u = u.drop('usr_last_login_dt_str', 1)
    u = u.drop('usr_created_dt_str', 1)

    # reopen temp and add header notes
    comments = ['# NOTES',
                '# Created on %s' % (datetime.datetime.now()),
                '# All personally identifiable information has been removed' +
                ' from these data',
                '# days_since_login is negative where the lastlogin is equal' +
                ' to the account creation date',
                '# login vs created dates appear to be using different' +
                ' timezones which results in lastlogin dates before account' +
                ' creation date.  These are treated as equivalent,' +
                ' i.e. lastlogin = account created.',
                '\n']

    # write comments
    wb.write_column(0, 0, sheetname, comments)

    # write pandas data
    row_start = len(comments) + 2
    col = 0
    for col_name in u:
        data = u[col_name].tolist()
        data.insert(0, col_name)
        wb.write_column(row_start, col, sheetname, data)
        col += 1

    # save the xls file
    wb.save()


def save_anon_resources(working_dir, out_xls_path):
    """
    Anonymize resource metrics and save to excel document
    working_dir: path of the current working directory.  This assumes that,
                 resources.pkl exists in this directory.
    """

    # prepare the workbook
    wb = workbook(out_xls_path)
    sheetname = wb.add_sheet('resources')

    # read data
    r = pd.read_pickle(os.path.join(working_dir, 'resources.pkl'))

    # remove unnecessary data
    r = r.drop('@timestamp', 1)
    r = r.drop('offset', 1)
    r = r.drop('report_date', 1)
    r = r.drop('res_created_dt_str', 1)
    r = r.drop('rpt_dt_str', 1)

    # reopen temp and add header notes
    comments = ['# NOTES',
                '# Created on %s' % (datetime.datetime.now()),
                '# Res_size is reported in bytes',
                '\n']

    # write comments
    wb.write_column(0, 0, sheetname, comments)

    # write pandas data
    row_start = len(comments) + 2
    col = 0
    for col_name in r:
        data = r[col_name].tolist()
        data.insert(0, col_name)
        wb.write_column(row_start, col, sheetname, data)
        col += 1

    # save the workbook
    wb.save()
