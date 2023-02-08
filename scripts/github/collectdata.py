#!/usr/bin/env python3

import creds
import issue
import requests
import datetime


def get_data(url, outpath):
    dat = []
    idx = []

#    AUTH = (creds.username, creds.password)

    headers = {'Authorization': 'token %s' % creds.token}

    r = requests.get('%s?state=all&per_page=50&page=%d' % (url, 1),
                     headers=headers)
    jdat = r.json()
    for d in jdat:
        dat.append(issue.Issue(d))

    # loop through github issue pages and save issue json
    if 'link' in r.headers:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
        print('--> collecting data.', end='', flush=True)
        while 'last' in pages and 'next' in pages:
            pg = pages['next'].split('=')[-1]
            r = requests.get(pages['next'], headers=headers)
            jdat = r.json()

            # save the issue
            for d in jdat:
                dat.append(issue.Issue(d))
            print('.', end='', flush=True)

            # exit when the last page is reached
            if pages['next'] == pages['last']:
                break

            pages = dict(
                [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])

        print('done')

    ## save to pickle
    #with open('issues.pkl', 'wb') as f:
    #    pickle.dump(dat, f)

    # save to csv
    print('--> writing issues to csv...', end='', flush=True)
    with open(outpath, 'w') as f:
        f.write('#\n# Generated on %s\n' % datetime.datetime.now())
        f.write('# Notes: each issue is listed below once for each git label'
                ' that it has. This makes analysis with pandas easier\n#\n')
        headers = list(dat[0].get()[0].keys())
        f.write('%s\n' % ','.join(headers))
        for item in dat:
            for label in item.get():
                txt_list = [str(label[h]) for h in headers]
                f.write('%s\n' % ','.join(txt_list))
    print('done')
    
if __name__ == "__main__":
    url = "https://api.github.com/repos/hydroshare/hydroshare/issues"
    outpath = 'hydroshare_git_issues.csv'
    get_data(url, outpath)
