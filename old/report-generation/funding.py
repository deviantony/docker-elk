#!/usr/bin/env python3

import os
import sys
import time
import hs_restclient as hsapi
import pandas as pd
import multiprocessing as mp
import datetime
import signal
import pickle
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
        try:
            resid = q.get(timeout=1)
        except mp.Queue.Empty:
            resid = None

        if resid is None:
            print('X', flush=True, end='')
            return

        with Timeout(10):
            try:
                scimeta = hs.getScienceMetadata(resid)
                funding = scimeta['funding_agencies']

                # add more metadata
                extra = dict(res_title=scimeta['title'],
                             res_id=resid)

                if len(funding) > 0:
                    print('|', end='')
                    for fund in funding:
                        d = {**fund, **extra}
                        out_q.put(d)
                else:
                    print('.', end='', flush=True)

            except Exception:
                print('!', flush=True, end='')


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
#        print(f'\nQUEUE SIZE: {in_q.qsize()}\n')
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
    try:
        df = pd.DataFrame(data)
        df.to_pickle(os.path.join(wrkdir, 'funding.pkl'))
    except Exception as e:
        print(e)

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
            print('X', flush=True, end='')
            break
        try:
            resources = hs.resources(from_date=st, to_date=et)
            print('.', flush=True, end='')
            for resource in resources:
                resid = resource['resource_id']
                out_q.put(resid)
        except Exception:
            print('!', flush=True, end='')


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
        time.sleep(3)

    # dequeue out_q to prevent join from freezing
    print('\n--> dequeuing results...', end='', flush=True)
    res_ids = []
    while not out_q.empty():
        val = out_q.get()
        res_ids.append(val)
    print('done')

    pool.close()
    pool.join()

    print(f'Found {len(res_ids)} resources')
    return res_ids


if __name__ == "__main__":
    st = time.time()

    parser = argparse.ArgumentParser('Collect HS Funding Agency Metrics')
    parser.add_argument('--host',
                        help='host to connect to',
                        default='www.hydroshare.org')
    parser.add_argument('--username',
                        help='HydroShare Username',
                        required=True)
    parser.add_argument('--password',
                        help='HydroShare Password',
                        required=True)
    parser.add_argument('--working-dir',
                        help='working directory',
                        default=None)

    args = parser.parse_args()
    wrkdir = args.working_dir
    uname = args.username
    pwd = args.password
    host = args.host

    while wrkdir is None:
        wrkdir = input('Enter working directory: ') or None
        if not os.path.exists(wrkdir):
            print('Path does not exist, please enter a ' +
                  'valid working directory')
            wrkdir = None
            sys.exit(-1)

    res_pkl = os.path.join(wrkdir, 'resources.pkl')
    resources_list = os.path.join(wrkdir, 'resources_list.pkl')
    fun_pkl = os.path.join(wrkdir, 'funding.pkl')

    resources_list_exists = os.path.exists(resources_list)
    fun_pkl_exists = os.path.exists(fun_pkl)

    # connect to HydroShare
    if not (resources_list_exists and fun_pkl_exists):

        auth = hsapi.HydroShareAuthBasic(username=uname, password=pwd)
        hs = hsapi.HydroShare(hostname=host, auth=auth)
        try:
            hs.getUserInfo()
        except hsapi.exceptions.HydroShareHTTPException:
            print('Authentication failed')
            sys.exit(1)

    # collect or open resource list
    if not os.path.exists(resources_list):
        resources = collect_resource_ids()
        print('--> saving resource ids')
        with open(resources_list, 'wb') as f:
            pickle.dump(resources, f)
    else:
        with open(resources_list, 'rb') as f:
            resources = pickle.load(f)

    # search HS or load funding data
    if not os.path.exists(fun_pkl):
        df = search_hs(resources)
    else:
        df = pd.read_pickle(fun_pkl)

    # create the resources combined file
    res_df = pd.read_pickle(os.path.join(wrkdir, 'resources.pkl'))

    # join with resources dataframe
    print('Creating the funding dataframe')
    df = pd.merge(df, res_df, how='outer', left_on="res_title", right_on="res_title")
    print('Saving the funding dataframe to CSV')
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
    print('Elapsed time: %5.5f seconds' % (time.time() - st))
    print('\n' + 50*'-' + '\n')
