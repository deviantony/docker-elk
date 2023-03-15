#!/usr/bin/env python3

import sys
import os
import argparse
from elasticsearch import Elasticsearch
from pandas.io.json import json_normalize
import time
import pandas

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
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # print newline on complete
    if iteration == total:
        print('%s |%s| %s%% %s' % (prefix, fill*length, '100', suffix), end='\n')


def get_es_data(host, scheme='http', port=9200, index='*', query='*', outfile=None,
                outpik='usage.pkl', prefix=['_source.'], drop_standard=True,
                drop=[], deidentfy=False):

    # connect to the hydroshare elasticsearch server
    es = Elasticsearch([{'host': host, 'port': port, 'scheme': scheme}])

    # perform search
    try:
        temp_r = es.search(index=index, q=query, scroll='10m', size=10)
    except Exception:
        print('Failed to complete search.')
        sys.exit(1)

    # get the total size of dataset
    doc_size = 0
    total_size = temp_r['hits']['total']

    # calculate the scroll size
    min_scroll, max_scroll = 1000, 10000
    inc_scroll = int(total_size / 25)
    scroll_size = min(inc_scroll, max_scroll) if inc_scroll > min_scroll else min_scroll
    print('--> total number of records = %d' % total_size)
    print('--> scroll_size = %d' % scroll_size)

    # execute the first elasticsearch query and increment the doc_size
    response = es.search(index=index, q=query, scroll='10m', size=scroll_size)
    doc_size += len(response['hits']['hits'])

    # save the results in a pandas dataframe
    df = json_normalize(response['hits']['hits'])
    df = df.applymap(convert_binary_string)

    while 1:
        try:
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

            # calculate the total size that has been downloaded so far
            doc_size += len(response['hits']['hits'])
            doc_size = total_size if doc_size > total_size else doc_size

            # print progress
            print_progress(doc_size, total_size,
                           prefix='downloading', length=50,
                           suffix='[ %d of %d ]    ' % (doc_size, total_size))

            # exit if the total downloaded size is equal to the
            # total known size of the data
            if doc_size == total_size:
                break

        except Exception:
            print('\nFailed to normalize elasticsearch response.')
            sys.exit(1)

#    # TODO: filter www-activity-\d{4}.\d{2}

    # clean and trim the pandas table
    for col in df.columns.values:
        for pre in prefix:
            if col[0:len(pre)] == pre:
                print('--> renaming column %s to %s' % (col, col[len(pre):]))
                time.sleep(.05)
                df.rename(columns={col: col[len(pre):]}, inplace=True)
                break
        else:
            print('--> dropping column: %s' % col)
            time.sleep(.05)
            df.drop(col, axis=1, inplace=True)

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
    parser = argparse.ArgumentParser(description="Query elasticsearch server.\n\nSample Usage\n%s" % (u1))
    parser.add_argument('-n', '--host', required=True, help='host address of the elasticsearch server')
    parser.add_argument('-p', '--port', help='port of the elasticsearch server')
    parser.add_argument('-i', '--index', help='elasticsearch index to query', default='*')
    parser.add_argument('-q', '--query', help='elasticsearch query string', default='*')
    parser.add_argument('-x', '--prefix', help='prefix for the fields to return', default=['_source.'], nargs='*')
    parser.add_argument('-f', '--file', help='output file', default=None)
    parser.add_argument('-b', '--binary-file', help='output binary file', default='usage.pkl')
    parser.add_argument('-d', '--drop', help='specific columns to drop', default=[], nargs='*')
    parser.add_argument('-s', '--drop-standard', help='indcates whether or not to drop a standard set of elasticsearch columns', default=True)
    args = parser.parse_args()

    res = get_es_data(args.host, args.port, args.index, args.query, args.file, 
                      args.binary_file, list(args.prefix), args.drop_standard, 
                      list(args.drop))



# EXAMPLES
# get_es_data('152.54.3.217', 8080, index='www-users-details-2017.02.08', query="*", outfile='all_users.csv',drop=['@timestamp','id','index'])
# ./elastic.py -n 152.54.3.217 -p 8080 -i www-users-details-2017.02.08 -f all_users.csv








