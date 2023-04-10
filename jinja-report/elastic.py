#!/usr/bin/env python3

import os
import sys
import time
import pandas
import argparse
from tqdm import tqdm
from elasticsearch import Elasticsearch
from pandas import json_normalize
from dotenv import load_dotenv

load_dotenv('../.env')

# standard elasticsearch fields to trim from the dataframe
DEFAULT_TRIM = ['@version', 'beat.hostname', 'beat.name', 'count', 'fields',
                'host', 'indextag', 'input_type', 'logname', 'message',
                'source', 'syslog_facility', 'syslog_facility_code',
                'syslog_severity', 'syslog_severity_code', 'tags', 'type']


def convert_binary_string(value):
    """
    This function removes the string encapsulated bytestrings that
    HydroShare sends to ElasticSearch.

    usage: df.applymap(convert_binary_string)
    """
    try:
        if type(value) == str:
            return eval(value).decode('utf-8')
        else:
            return value
    except Exception:
        return value


def print_progress(iteration, total, prefix='', suffix='',
                   decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # print newline on complete
    if iteration == total:
        print('%s |%s| %s%% %s' %
              (prefix, fill*length, '100', suffix), end='\n')


def get_es_data(host,
                port=9200,
                scheme='https',
                index='*',
                query='*',
                outfile=None,
                outpik='usage.pkl',
                prefix={'_source.': ''},
                drop_standard=True,
                drop=[],
                deidentify=False,
                rename_cols={},
                return_es_index=False):

    # connect to the hydroshare elasticsearch server
    elastic_url = f"{scheme}://{host}:{port}"
    print(f"Connecting to: {elastic_url}")
    es = Elasticsearch(elastic_url, basic_auth=(os.getenv('ELASTIC_USERNAME', 'elastic'), os.getenv(
        'ELASTIC_PASSWORD', 'changeme')), verify_certs=False)

    # perform search
    try:
        temp_r = es.search(index=index, q=query, scroll='10m', size=10)
    except Exception as e:
        print(f'Failed to complete search: {e}')
        sys.exit(1)

    # get the total size of dataset
    total_size = temp_r['hits']['total']

    try:
        total_size = int(total_size.get('value'))
    except Exception as e:
        print(f'Error attempting to access total_size: {e}')
        print(f"Total size is: {total_size}")

    # calculate the scroll size
    min_scroll, max_scroll = 1000, 10000
    inc_scroll = int(total_size / 25)
    scroll_size = min(
        inc_scroll, max_scroll) if inc_scroll > min_scroll else min_scroll
    print('--> total number of records = %d' % total_size)
    print('--> scroll_size = %d' % scroll_size)

    # execute the first elasticsearch query and increment the doc_size
    response = es.search(index=index, q=query, scroll='10m', size=scroll_size)

    # save the results in a pandas dataframe
    df = json_normalize(response['hits']['hits'])
    df = df.applymap(convert_binary_string)

    # initialize the progress bar, using ascii so it doesn't break
    # when called from a subprocess.
    pbar = tqdm(ascii=True, total=total_size)
    while 1:
        try:
            # update progress. this is at the beginning because the first
            # call is made before the loop begins
            pbar.update(scroll_size)

            # make the next request using the previous _scroll_id
            sid = response['_scroll_id']
            response = es.scroll(scroll_id=sid, scroll='10m')

            # get the scroll_size of the previous query and exit
            # if it is zero
            scroll_size = len(response['hits']['hits'])

            if scroll_size > 0:
                # save the results in a pandas dataframe and append
                # to previous results
                new_df = json_normalize(response['hits']['hits'])
                new_df = new_df.applymap(convert_binary_string)
                df = pandas.concat([df, new_df], sort=False)
            else:
                break

        except Exception as e:
            print('\nFailed to normalize elasticsearch response.')
            print(e)
            sys.exit(1)

    # close the progress bar
    pbar.close()

    # rename the index
    if return_es_index:
        df.rename(columns={'_index': 'es-index'}, inplace=True)

    # clean and trim the pandas table
    for col in df.columns.values:
        for pre in prefix.keys():
            if pre in col:
                new_name = col.replace(pre, prefix[pre])
                print(f'--> renaming column {col} -> {new_name}')
                df.rename(columns={col: new_name}, inplace=True)
                time.sleep(.05)
                break

    # drop any specified columns
    if drop_standard:
        drop.extend(DEFAULT_TRIM)

    for dropcol in drop:
        if dropcol in df.columns.values:
            print('--> dropping column: %s' % dropcol)
            time.sleep(.05)
            df.drop(dropcol, axis=1, inplace=True)
        else:
            print('--> [skip] drop column.  Could not find %s' % dropcol)

    # rename columns any other columns that were specified in input args
    col_names = df.columns.values
    for old_name, new_name in rename_cols.items():
        if old_name in col_names:
            print(f'--> renaming column {old_name} -> {new_name}')
            df.rename(columns={old_name: new_name}, inplace=True)
        else:
            print(
                f'--> could not find column {old_name}, skipping rename operation')

    # write the dataframe to file if requested
    if outfile is not None:
        print('--> Saving CSV file to: %s' % outfile)
        df.to_csv(outfile)

    if os.path.exists(outpik):
        os.remove(outpik)
    print('--> Saving Binary file to: %s' % outpik)
    df.to_pickle(outpik)

    return df


if __name__ == "__main__":

    u1 = "./elastic -n usagemetrics.hydroshare.org -p 8080 -i 'www-users-details-2017.01.06*' -f all_users.csv"
    parser = argparse.ArgumentParser(
        description="Query elasticsearch server.\n\nSample Usage\n%s" % (u1))
    parser.add_argument('-n', '--host', required=True,
                        help='host address of the elasticsearch server')
    parser.add_argument(
        '-p', '--port', help='port of the elasticsearch server')
    parser.add_argument(
        '-i', '--index', help='elasticsearch index to query', default='*')
    parser.add_argument(
        '-q', '--query', help='elasticsearch query string', default='*')
    parser.add_argument(
        '-x', '--prefix', help='prefix for the fields to return', default=['_source.'], nargs='*')
    parser.add_argument('-f', '--file', help='output file', default=None)
    parser.add_argument('-b', '--binary-file',
                        help='output binary file', default='usage.pkl')
    parser.add_argument(
        '-d', '--drop', help='specific columns to drop', default=[], nargs='*')
    parser.add_argument('-s', '--drop-standard',
                        help='indcates whether or not to drop a standard set of elasticsearch columns', default=True)
    args = parser.parse_args()

    res = get_es_data(args.host, args.port, args.index, args.query, args.file,
                      args.binary_file, list(args.prefix), args.drop_standard,
                      list(args.drop))


# EXAMPLES
# get_es_data('152.54.3.217', 8080, index='www-users-details-2017.02.08', query="*", outfile='all_users.csv',drop=['@timestamp','id','index'])
# ./elastic.py -n 152.54.3.217 -p 8080 -i www-users-details-2017.02.08 -f all_users.csv
