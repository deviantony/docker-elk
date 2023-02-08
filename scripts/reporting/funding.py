#!/usr/bin/env python3

import os
import sys
import time
import hs_restclient as hsapi
import getpass
import pandas as pd
import multiprocessing as mp
import datetime
import pdb
import signal
import argparse


# global so that it can be called via processes
hs = None
df = None
wrkdir = None


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


def search_hs(resources):
    global hs

    print('\n--> searching HS for funding sources')

    # configure the multiprocessing environment
    NCORE = mp.cpu_count()
    in_q = mp.Queue()
    out_q = mp.Queue()
    pool = mp.Pool(NCORE, initializer=check_pub,
                   initargs=(in_q, out_q))

    # build queue of resource ids for the pool workers
    for resid in resources:
        in_q.put(resid)

    # tell workers to exit
    for _ in range(NCORE):
        in_q.put(None)

    # wait for all processes to finish
    while not in_q.empty():
        time.sleep(1)

    # dequeue the out_q to prevent the underlying pipe from freezing join
    time.sleep(3)
    data = []
    while not out_q.empty():
        val = out_q.get()
        data.append(val)
    pool.close()
    pool.join()

    # saving results to at data frame
    df = pd.DataFrame(data)
    df.to_pickle(os.path.join(wrkdir, 'funding.pkl'))
    df.to_csv(os.path.join(wrkdir, 'funding.csv'))

    return df


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


def query_resource_ids(in_q, out_q, hs):
    while True:
        st, et = in_q.get()
        if st is None:
            break

        resources = hs.resources(from_date=st, to_date=et)
        for resource in resources:
            resid = resource['resource_id']
            out_q.put(resid)
            print('.', end='', flush=True)


def collect_resource_ids():
    global hs

    NCORE = mp.cpu_count()
    in_q = mp.Queue()
    out_q = mp.Queue()

    print('--> populating job queue...', end='')
    # split the date range of HS resources
    dates = split_date_range(1000)
    for date in dates:
        in_q.put(date)
    # tell workers to exit
    for _ in range(NCORE):
        in_q.put([None, None])
    print('done')

    print('--> collecting resource ids')
    pool = mp.Pool(NCORE, initializer=query_resource_ids,
                   initargs=(in_q, out_q, hs))

    # wait for all processes to finish
    while not in_q.empty():
        time.sleep(1)

    # dequeue out_q to prevent join from freezing
    res_ids = []
    while not out_q.empty():
        val = out_q.get()
        res_ids.append(val)
    pool.close()
    pool.join()
    return res_ids


def authenticate():
    tries = 0
    host = 'www.hydroshare.org'
    while 1:
        u = input('Enter HS username: ')
        p = getpass.getpass('Enter HS password: ')
        auth = hsapi.HydroShareAuthBasic(username=u, password=p)
        hs = hsapi.HydroShare(hostname=host, auth=auth)
        try:
            hs.getUserInfo()
            break
        except hsapi.exceptions.HydroShareHTTPException:
            print('Authentication failed, attempt %d' % (tries+1))
            tries += 1

        if tries >= 3:
            print('Number of attempts exceeded, exiting')
            sys.exit(1)
    return hs


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--working-dir',
                        help='path to directory containing elasticsearch data',
                        required=True)
    parser.add_argument('-c',
                        help='force collection of data',
                        action='store_true')
    args = parser.parse_args()

    wrkdir = args.working_dir


    if not os.path.exists(os.path.join(wrkdir, 'funding.pkl')) or \
            args.c:
        # collect resource ids and search for funding agencies
        hs = authenticate()
        resources = collect_resource_ids()
        df = search_hs(resources)
    else:
        df = pd.read_pickle(os.path.join(wrkdir, 'funding.pkl'))

    if os.path.exists(os.path.join(wrkdir, 'resources.pkl')):
        res_df = pd.read_pickle(os.path.join(wrkdir, 'resources.pkl'))
    else:
        print('Could not locate resources.pkl, please run collect_data.py')
        sys.exit(0)

    # join with resources dataframe
    df = pd.merge(df, res_df, how='outer', left_on="res_title", right_on="res_title")
    df.to_csv(os.path.join(wrkdir, 'funding.csv'))

    # print some statistics
    print('\n\n' + 50*'-')
    print('HS Funding Statistics Summary:')
    print(50*'-')
    for col in ['agency_name', 'agency_url', 'award_number', 'award_title']:
        stats = df[col].describe()
        print('\n%s' % col.upper())
        for key in ['count', 'unique', 'top', 'freq']:
            print('{:<10} {:<10}'.format(key, stats[key]))
    print('Number of resources containing funding metadata: %d' % len(df))
    print('\n' + 50*'-' + '\n')
