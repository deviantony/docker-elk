#!/usr/bin/env python

"""
Test URL:
    https://geodeepdive.org/api/snippets?full_results=true&inclusive=true&term=CUAHSI

"""

import sys
import json
import pandas
import requests
import argparse

results = []



def get_results(url):
    """
    Recursive function that queries the geodeepdive dive API
    for all term matches and returns
    """

    # make request
    r = requests.get(url)

    if r.status_code == 200:
        # load the data
        data = json.loads(r.content)

        res = data['success']['data']

        # get the next page
        if data['success']['next_page'].strip() != '':
            next_page = data['success']['next_page']

            res.extend(get_results(next_page))

        return res
    else:
        return []


#def search_gdd(terms):
#
#    base = 'https://geodeepdive.org/api/snippets'
#
##    full_results=true&inclusive=true&min_published=2020-01-01&clean
#    params = {'term': '',
#              'full_results': True,
#              'inclusive': True
#              }
#
#    for term in terms:
#        params['term'] = term
#
#        # make request
#        r = requests.get(base, params=params)
#
#        if r.status_code == 200:
#            # load the data
#            data = json.loads(r.content)
#            
#            results.append(pandas.from_dict(data['success']['data']))
#
#            # get the next page
#            next_page = data['success']['next_page']
#            # todo call recursively
#
#            import pdb; pdb.set_trace()
#        else:
#            print(r.status_code)
#            break
#

if __name__ == '__main__':


    p = argparse.ArgumentParser()
    p.add_argument('-f',
                   default='',
                   help='path to list of search terms')
    p.add_argument('-t',
                   default='',
                   nargs='+',
                   help='space separated list of search terms')

    args = p.parse_args()

    # exit early if -f and -t are not provided
    if not (args.f or args.t):
        print('Must supply either -f or -t argument')
        p.print_usage()
        sys.exit(1)

    if args.f:
        with open(args.f, 'r') as f:
            terms = [l.strip() for l in f.readlines()]
    elif args.t:
        terms = args.t

    # run search
    dfs = []
    root_url = 'https://geodeepdive.org/api/snippets'
    for term in terms:

        print(f'Searching term: {term}... ', end='', flush=True)

        # build url
        params = dict(full_results=True,
                      inclusive=True,
                      term=term)
        s = requests.Session()
        p = requests.Request('GET', root_url,
                             params=params).prepare()
        hits = get_results(p.url)

        # add the search term to the results
        df = pandas.DataFrame(hits)
        df['search_term'] = term

        dfs.append(df)

        print(f'{len(df)} matches')

    # merge all dataframes
    merged = pandas.concat(dfs)
    merged.reset_index(inplace=True)

    merged = merged.groupby('doi').agg({
                                        'pubname': 'first',
                                        'publisher': 'first',
                                        '_gddid': 'first',
                                        'title': 'first',
                                        'coverDate': 'first',
                                        'URL': 'first',
                                        'authors': 'first',
                                        'highlight': 'sum',
                                        'search_term': list})
#    cols = ['pubname', 'publisher',
#            '_gddid', 'title', 'doi', 'coverDate',
#            'URL', 'authors', 'highlight', 'search_term']
#    
#    merged.drop(merged.columns.difference(cols), 1, inplace=True)

    # save merged dataframe to csv
    merged.to_csv('gdd_matches.csv')


