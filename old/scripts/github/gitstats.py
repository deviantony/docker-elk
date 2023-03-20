#!/usr/bin/env python3

import os
import sys
import shutil

import pandas
from tabulate import tabulate

import collectdata
import plot
import tabular

import argparse

from datetime import datetime


def run_statistics(csv, dirname, st, et):

    # load the csv file into a pandas dataframe
    df = pandas.read_csv(csv, sep=',', comment='#')
    df['created_dt'] = pandas.to_datetime(df.created_dt, errors='coerce') \
                             .dt.normalize()
    df['closed_dt'] = pandas.to_datetime(df.closed_dt, errors='coerce') \
                            .dt.normalize()

    # summarize all issues by label
    d = df.groupby('label').count().number.to_frame()
    d.columns = ['all_issues']

    # summarize all open issues
    d1 = df[df.state == 'open'].groupby('label').count().number.to_frame()
    d1.columns = ['open_issues']

    d = d.merge(d1, left_index=True, right_index=True)

    # indicate issues as either 'open' or 'closed'
    df.loc[df.state == 'open', 'open'] = 1
    df.loc[df.state == 'closed', 'closed'] = 1

    # make plots
    plot.open_issues(df, dirname)
    plot.all_issues(df, dirname)

    # make tabular statistics
    tabular.all_resolved_issues(df, st, et, dirname)
    tabular.resolved_bugs(df, st, et, dirname)
    tabular.resolved_features(df, st, et, dirname)


def get_working_directory():

    # create a directory for these data
    dirname = datetime.now().strftime('%m.%d.%Y')
    issues_bak = None
    if os.path.exists(dirname):
        msg = 'The directory "{0}" already exist. Would you like to ' \
              'remove it? [y/N]'.format(dirname)

        res = input(msg)
        if res == 'y':

            # copy git issues out of directory if it exists
            issues_csv = os.path.join(dirname, 'hydroshare_git_issues.csv')
            issues_bak = './hydroshare_git_issues.csv.%s.bak' % dirname
            if os.path.exists(issues_csv):
                shutil.move(issues_csv, issues_bak)

            # remove the directory
            shutil.rmtree(dirname)
        else:
            return dirname


    # build clean directory
    os.makedirs(dirname)

#    # copy git issues back into clean directory
#    if issues_bak is not None:
#        if os.path.exists(issues_bak):
#            shutil.move(issues_bak, issues_csv)

    print('Metrics will be saved into: %s' % dirname)

    return dirname


def validate_date_inputs(st, et):

    try:
        st = datetime.strptime(st, '%m-%d-%Y')
    except ValueError:
        st = datetime.strptime('01-01-2000', '%m-%d-%Y')
        print('\tincorrect start date format, ' +
              'using default start date: 01-01-2000')
    try:
        et = datetime.strptime(et, '%m-%d-%Y')
    except ValueError:
        et = datetime.now()
        print('\tincorrect end date format, using default start date: %s' %
              et.strftime('%m-%d-%Y'))

    return st, et


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--st',
                        help='start time MM-DD-YYYY',
                        default='01-01-2000')
    parser.add_argument('--et',
                        help='start time MM-DD-YYYY',
                        default=datetime.now().strftime('%m-%d-%Y'))
    parser.add_argument('--working-dir',
                        help='path to directory containing elasticsearch data',
                        required=False)
    args = parser.parse_args()

    # check working directory
    if args.working_dir:
        dirname = args.working_dir
    else:
        # prepare the working directory
        dirname = get_working_directory()

    # validate the date inputs
    st, et = validate_date_inputs(args.st, args.et)


    # run statistics
    print(dirname)

    csv = os.path.join(dirname, 'hydroshare_git_issues.csv')

    if not os.path.exists(os.path.join(csv)):
        print('\nCould not find %s, proceeding to download git '
              'tickets.\n' % csv)

        # collect data
        url = "https://api.github.com/repos/hydroshare/hydroshare/issues"
        #collectdata.get_data(url, csv, st, et)
        collectdata.get_data(url, csv)
    else:
        print('\nFound %s, proceeding to re-use. ' % csv)
        print('If this is not the desired functionality, '
              'remove %s and re-run.\n' % csv)

    # run the statistics routine to generate plots
    run_statistics(csv, dirname, args.st, args.et)

