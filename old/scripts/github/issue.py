from datetime import datetime as dt


class Issue(object):
    def __init__(self, issue_dict):
        self.number = issue_dict['number']
        self.state = issue_dict['state']
        self.url = issue_dict['url']
        self.labels = issue_dict['labels']
        self.description = issue_dict['body'] or ""
        self.description = self.description.replace('\r', '') \
                                           .replace('\n', '') \
                                           .replace(',', ' ')
        self.title = issue_dict['title']
        self.title = self.title.replace('\r','') \
                               .replace('\n', '') \
                               .replace(',', ' ')

        self.created_dt = issue_dict['created_at']
        if self.created_dt is not None:
            self.created_dt = dt.strptime(self.created_dt,
                                          '%Y-%m-%dT%H:%M:%SZ')

        self.closed_dt = issue_dict['closed_at']
        if self.closed_dt is not None:
            self.closed_dt = dt.strptime(self.closed_dt,
                                         '%Y-%m-%dT%H:%M:%SZ')

    def __issue_to_dict(self, i=None):
        if i is None:
            l = ''
        else:
            l = self.labels[i]['name']

        return dict(number=self.number,
                    created_dt=self.created_dt,
                    closed_dt=self.closed_dt,
                    description=self.description,
                    state=self.state,
                    title=self.title,
                    url=self.url,
                    label=l)

    def get(self):
        data = []
        if len(self.labels) > 0:
            for i in range(0, len(self.labels)):
                data.append(self.__issue_to_dict(i))
        else:
            data.append(self.__issue_to_dict())
        return data





