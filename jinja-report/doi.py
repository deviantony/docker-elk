#!/usr/bin/env python3

import os
import pickle
#import signal
import requests
#import argparse
import pandas as pd
from lxml import etree
import hs_restclient as hsapi
from datetime import datetime
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
from urllib3.exceptions import InsecureRequestWarning
from pandas.plotting import register_matplotlib_converters


import plot
import creds
import utilities

register_matplotlib_converters()
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def load_data(working_dir, pickle_file='doi.pkl'):

    # return existing doi data
    path = os.path.join(working_dir, pickle_file)
    if os.path.exists(path):
        return pd.read_pickle(path)

    # doi data was not found, download it.
    print('--> collecting doi\'s from HydroShare')
    hs = hsapi.HydroShare(hostname='www.hydroshare.org',
                          prompt_auth=False,
                          use_https=False,
                          verify=False)
    resources = hs.resources(published=True)
    dat = []
    for resource in resources:
        meta = hs.getScienceMetadata(resource['resource_id'])
        dates = {}
        for dt in meta['dates']:
            dates[dt['type']] = dt['start_date']
        if 'published' not in dates:
            continue
        
        dat.append(dict(resource_id=resource['resource_id'],
                        owner_id=meta['creators'][0]['hydroshare_user_id'],
                        created_dt=dates['created'],
                        last_modified_dt=dates['modified'],
                        published_dt=dates['published'],
                        doi=resource['doi']))

    df = pd.DataFrame(dat)

    # convert columns to datetime objects
    df['created_dt'] = pd.to_datetime(df['created_dt'])
    df['last_modified_dt'] = pd.to_datetime(df['last_modified_dt'])
    df['Date Published'] = pd.to_datetime(df['published_dt'])

    with open(os.path.join(working_dir, 'doi.pkl'), 'wb') as f:
        pickle.dump(df, f)

    return df


def published_resources(input_directory='.',
                        start_time=datetime(2000, 1, 1),
                        end_time=datetime(2030, 1, 1),
                        aggregation='1M',
                        label='Monthly published resources',
                        color='b',
                        **kwargs):
    print(f'--> calculating published resources per {aggregation}')
    df = load_data(input_directory)
    df = utilities.subset_by_date(df,
                                  start_time,
                                  end_time,
                                  date_column='Date Published')
    df.set_index('Date Published', inplace=True)

    # group and sum
    df = df.sort_index()
    df = df.groupby(pd.Grouper(freq=aggregation)).count()['resource_id']

    # create plot object
    x = df.index
    y = df.values.tolist()

    return plot.PlotObject(x, y,
                           label=label,
                           color=color)


def citations(input_directory='.',
              start_time=datetime(2000, 1, 1),
              end_time=datetime(2030, 1, 1),
              label='Citations of published resources',
              color='b',
              **kwargs):

    print(f'--> calculating published resource citation count')

    if not os.path.exists(os.path.join(input_directory, 'doi-citations.pkl')):
        df = load_data(input_directory)
        df = utilities.subset_by_date(df,
                                      start_time,
                                      end_time,
                                      date_column='Date Published')
        df.set_index('Date Published', inplace=True)
        df['citations'] = 0
        df['citing_dois'] = ''

        # collect citations for each doi
        for idx, row in df.iterrows():
            doi = row['doi']
            url = ('https://doi.crossref.org/servlet/getForwardLinks?'
                   f'usr={creds.username}&pwd={creds.password}&'
                   f'doi={doi}')
            try:
                res = requests.get(url)
                root = etree.fromstring(res.text.encode())
                citations = root.findall('.//body/forward_link',
                                        namespaces=root.nsmap)
                dois = []
                for citation in citations:
                    doi = citation.find('.//doi', namespaces=root.nsmap).text
                    dois.append(doi)

                df.at[idx, 'citations'] = len(dois)
                df.at[idx, 'citing_dois'] = ','.join(dois)
            except ConnectionError as e:
                print(f'Warning: issue with DOI connection: {e}')
                continue

        df.to_pickle(os.path.join(input_directory, 'doi-citations.pkl'))
    else:
        df = pd.read_pickle(os.path.join(input_directory,
                                         'doi-citations.pkl'))

    # generate plot
    x = df.index
    y = df.citations.tolist()

    return plot.PlotObject(x, y,
                           dataframe=df,
                           label=label,
                           color=color)
