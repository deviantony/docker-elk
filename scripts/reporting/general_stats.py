#!/usr/bin/env python3

import os
import argparse
import pandas as pd
from tabulate import tabulate

import latex


def print_table(df, columns, headers=[], orderby=None):

    headers.insert(0, 'Use Metric')
    data = []
    if orderby is None:
        idx_data = list(df.index)
        vals = list(df[columns].values)
        for i in range(0, len(df.index)):
            data.append([idx_data[i]] + list(vals[i]))
    else:
        for idx in orderby:
            try:
                vals = list(df.loc[idx][columns])
            except KeyError:
                vals = [0] * len(columns)
            data.append([idx] + vals)

    table = tabulate(data, headers=headers, tablefmt='psql')
    print(table)


def run(wrkdir, write_latex=0):

    totals = []
    dfu = pd.read_pickle(os.path.join(wrkdir, 'users.pkl'))

    user_types = [
                  'University Faculty',
                  'University Professional or Research Staff',
                  'Post-Doctoral Fellow',
                  'University Graduate Student',
                  'University Undergraduate Student',
                  'Commercial/Professional',
                  'Government Official',
                  'School Student Kindergarten to 12th Grade',
                  'School Teacher Kindergarten to 12th Grade',
                  'Other',
                  'Unspecified']

    resource_types = [
                      'GenericResource',
                      'SWATModelInstanceResource',
                      'CompositeResource',
                      'MODFLOWModelInstanceResource',
                      'CollectionResource',
                      'ModelProgramResource',
                      'ModelInstanceResource',
                      'GeographicFeatureResource',
                      'NetcdfResource',
                      'TimeSeriesResource',
                      'ToolResource',
                      'RasterResource',
                      'ScriptResource'
                      ]


    ########################
    ######  USERS ##########
    ########################
    print('--> calculating user statistics... ', end='', flush=True)

    # change invalid user types to 'Other'
    dfu.loc[~dfu.usr_type.isin(user_types), 'usr_type'] = 'Other'

    # group by user type
    dfu_grouped = dfu.groupby(['usr_type']).count()

    totals.append('Total Users: %d' % (dfu_grouped.usr_id.sum()))

    user_data = pd.DataFrame(index=dfu_grouped.index)
    user_data['num_users'] = dfu_grouped.usr_id

    print('done')

    ########################
    ######  RESOURCES ######
    ########################

    print('--> calculating resource statistics... ', end='', flush=True)
    # load resources
    dfr = pd.read_pickle(os.path.join(wrkdir, 'resources.pkl'))

    # convert non-user types to 'Other'
    dfr.loc[~dfr.usr_type.isin(user_types), 'usr_type'] = 'Other'

    # convert res_size to GB
    dfr.res_size = dfr.res_size.apply(lambda x: x/1000000000)

    # calculate resource count
    dfr_grouped = dfr.groupby(['usr_type']).count()
    totals.append('Total Resources: %d' % (dfr_grouped.usr_id.sum()))

    user_data['num_resources'] = dfr_grouped.usr_id

    user_data.join(dfr_grouped)

    # calculate resource size
    dfr_grouped = dfr.groupby(['usr_type']).sum()
    totals.append('Total Resource Size: %d' % (dfr_grouped.res_size.sum()))

    user_data['res_size'] = dfr_grouped.res_size

    dfr_grouped = dfr.groupby(['res_type']).count()
    totals.append('Total Resources: %d' % (dfr_grouped.usr_id.sum()))

    res_data = pd.DataFrame(index=dfr_grouped.index)
    res_data['res_count'] = dfr_grouped.usr_id

    # calculate resource size
    dfr_grouped = dfr.groupby(['res_type']).sum()
    totals.append('Total Resource Size: %d' % (dfr_grouped.res_size.sum()))

    res_data['res_size'] = dfr_grouped.res_size

    print('done')

    ########################
    ####### ACTIVITY #######
    ########################

    print('--> calculating activity statistics... ', end='', flush=True)

    # load activity
    dfa = pd.read_pickle(os.path.join(wrkdir, 'activity.pkl'))

    # convert non-user types to 'Other'
    dfa.loc[~dfa.user_type.isin(user_types), 'user_type'] = 'Other'

    # calculate user logins
    dfa_login = dfa[dfa.action == 'login']
    dfa_grouped = dfa_login.groupby(['user_type']).count()

    totals.append('Total Logins: %d' % (dfa_grouped.user_id.sum()))

    user_data['num_logins'] = dfa_grouped.action

    print('done')

    ##########################
    ##### SUMMARY TABLES #####
    ##########################

    # print in tabular form directly to the terminal
    print_table(user_data,
                columns=['num_users', 'num_resources',
                         'res_size', 'num_logins'],
                headers=['Number of Users', 'Number of Resources',
                         'Resource Size (GB)', 'Login Count'],
                orderby=user_types)

    print_table(res_data,
                columns=['res_count', 'res_size'],
                headers=['Number of Resources', 'Resource Size (GB)'],
                orderby=resource_types)

    # create pdfs using LaTex
    if write_latex:
        print('--> writing to LaTex')

        user_data = user_data.rename(columns={'num_users': 'Number of Users',
                                              'num_resources': 'Number of Resources',
                                              'res_size': 'Resource Size (GB)',
                                              'num_logins': 'Login Count'})

        ofile = latex.write_table(
                                  fname=os.path.join(wrkdir, 'user_statistics_table.tex'),
                                  dat=user_data,
                                  index_list=user_types,
                                  fmt=['%3.0f', '%3.0f', '%3.5f', '%3.0f'],
                                  lcol='User Type',
                                  pdfwidth=200,
                                  pdfheight=55,
                                  hoffset=-45,
                                  voffset=-40)

        latex.build_latex_pdf(ofile, wrkdir)

        res_data = res_data.rename(columns={'res_count': 'Number of Resources',
                                            'res_size': 'Resource Size (GB)'})

        ofile = latex.write_table(
                                  fname=os.path.join(wrkdir,
                                        'resource_statistics_table.tex'),
                                  dat=res_data,
                                  index_list=resource_types,
                                  fmt=['%3.0f', '%3.5f'],
                                  lcol='Resource Type',
                                  pdfwidth=135,
                                  pdfheight=65,
                                  hoffset=-45,
                                  voffset=-40)

        latex.build_latex_pdf(ofile, wrkdir)



    print('\nTotals')
    for t in totals:
        print(t)

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='general hydroshare statistics')
    parser.add_argument('--working-dir', help='path to directory containing elasticsearch data',
            required=True)
    args = parser.parse_args()

    run(args.working_dir, write_latex=1)
