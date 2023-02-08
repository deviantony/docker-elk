#!/usr/bin/env python3

import creds
import requests
import datetime
import commit


def get_branches(url):

    branches = {}

    page = 1
    print('collecting branches', flush=True, end='')
    while 1:
        print('.', flush=True, end='')

        r = requests.get('%s/branches?page=%d' % (url, page),
                         headers={'Authorization': 'token %s' % creds.token})
        branch_json = r.json()

        # exit if no data is found
        if len(branch_json) == 0:
            break

        for branch in branch_json:
            branches[branch['name']] = branch['commit']['sha']

        page += 1
    print('')

    return branches


def get_data(url, outpath, in_branches=[]):
    dat = []
    idx = []


    # collect branches
    branches = get_branches(url)

    # filter branches by in_branches
    if len(in_branches) > 0:
        branches = {k: branches[k] for k in in_branches if k in branches}
        print(branches)

    for k, v in branches.items():
        branch_name = k
        branch_sha = v

        # get info from the current branch.
        r = requests.get('%s/branches/%s' % (url, branch_name),
                         headers={'Authorization': 'token %s' % creds.token})

        # get the last commit sha from the master branch
        jdat = r.json()
        sha = jdat['commit']['sha']
        old_sha = ''

        print('collecting commits for branch %s' % branch_name,
              flush=True, end='')
        while sha != old_sha:
            print('.', flush=True, end='')
            # get the first batch of commits
            r = requests.get('%s/commits?per_page=100&sha=%s' %
                             (url, sha),
                             headers={'Authorization': 'token %s' % creds.token})
                             
            jdat = r.json()
            for d in jdat:
                import pdb; pdb.set_trace()
                dat.append(commit.Commit(d, branch_name))

            # get the new_sha
            old_sha = sha
            sha = dat[-1].sha
        print('')

    print('\nFound %d commits' % len(dat))

    # save to csv
    print('--> writing commits to csv...', end='', flush=True)
    with open(outpath, 'w') as f:
        f.write('#\n# Generated on %s\n' % datetime.datetime.now())
        headers = list(dat[0].get()[0].keys())
        f.write('%s\n' % ','.join(headers))
        for item in dat:
            for label in item.get():
                txt_list = [str(label[h]).replace('\n', '') for h in headers]
                f.write('%s\n' % ','.join(txt_list))
    print('done')

if __name__ == "__main__":
    url = "https://api.github.com/repos/hydroshare/hydroshare"
    outpath = 'hydroshare_commits.csv'
    get_data(url, outpath, in_branches=['master'])
