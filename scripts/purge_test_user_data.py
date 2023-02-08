#!/usr/bin/env python

import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan, bulk


#uids = [62, 1679, 272, 1604, 515, 1130, 983, 943, 575]

if __name__ == "__main__":

    args = sys.argv[1:]
    confirm_delete = 'n'
    if '-y' in args:
        args.remove('-y')
        confirm_delete = 'Y'

    uids = [int(u) for u in args]
    if len(uids) == 0:
        print 'No user ids provided, exiting'
        sys.exit(1)

    host = 'localhost'
    port = '9200'
    es = Elasticsearch([{'host': host, 'port': port}])

    uidx = '*user*latest*'
    ridx = '*resource*latest*'
    aidx = 'www-activity-*'

    fields = {uidx:'usr_id',
              ridx:'usr_id',
              aidx:'user_id'}

    def chunk(seq, size):
        return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

    for uid in uids:
        bulk_deletes = []
        for idx in [uidx, ridx, aidx]:
            for res in scan(es,
                            raise_on_error=False,
                            query={"query": {"match": {fields[idx]: uid}}},
                            index=idx,
                            _source=False,
                            track_scores=False,
                            scroll='10s'):
                res['_op_type'] = 'delete'
                bulk_deletes.append(res)
        if len(bulk_deletes) > 0:
            if confirm_delete == 'n':
                confirm_delete = raw_input('Found %d records for uid = %d. Do you want to remove them? [Y/n/x] ' % (len(bulk_deletes), uid))
            if confirm_delete.lower() == 'x':
                sys.exit(1)
            elif confirm_delete.lower() != 'n':
                print '---> removing %d records...' % (len(bulk_deletes)),
                for grp in chunk(bulk_deletes, 1000):
                    resp = bulk(es, grp)
                print 'done'
        else:
            print('No records to delete for uid = %d' % (uid))
