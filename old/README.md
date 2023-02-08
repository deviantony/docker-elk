# hydroshare-usagemetrics
ELK stack install and configuration files for HydroShare


## Configure Logrotate for Logstash

```
cp /etc/logrotate.d/nginx /etc/logrotate.d/logstash
```

```
$ vim /etc/logrotate.d/logstash  
/var/log/logstash/*log /var/log/logstash/*.err /var/log/logstash/*.stdout{  
  daily  
  rotate 10  
  copytruncate  
  compress  
  delaycompress  
  missingok  
  notifempty  
 }
```

# Purge ES data
```
# select activity for the last 10 days
GET www-activity-*/_search
{
"query": {
        "range" : {
            "@timestamp" : {
                "gte" : "now-50d/d",
                "lt" :  "now/d"
            }
        }
    }
}
```

# Delete by query
```
POST /www-activity-*/_delete_by_query
{
"query": {
        "range" : {
            "@timestamp" : {
                "gte" : "now-50d/d",
                "lt" :  "now/d"
            }
        }
    }
}
```
