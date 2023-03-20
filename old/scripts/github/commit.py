from datetime import datetime as dt


class Commit(object):
    def __init__(self, dict, branch=''):
        self.sha = dict['sha']
        self.date = dt.strptime(dict['commit']['author']['date'],
                                '%Y-%m-%dT%H:%M:%SZ')
        self.author = dict['commit']['author']['name']
        self.message = dict['commit']['message'].replace(',',' ').replace('#','')
        self.branch = branch

    def __issue_to_dict(self, i=None):
        return dict(sha=self.sha,
                    date=self.date,
                    author=self.author,
                    branch=self.branch,
                    message=self.message)

    def get(self):
        data = []
        data.append(self.__issue_to_dict())
        return data
