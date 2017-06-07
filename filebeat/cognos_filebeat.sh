#!/usr/bin/env bash
mkdir -p ./cognos_logs
mkdir -p ./cognos_logs/wlp
mkdir -p ./cognos_logs/workarea
mkdir -p ./fb_temp

rsync -avzr -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress cognos1.contoso.com:/opt/ibm/cognos/analytics/logs/ ./cognos_logs
rsync -avzr -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress cognos1.contoso.com:/opt/ibm/cognos/analytics/wlp/usr/servers/cognosserver/logs/ ./cognos_logs/wlp
rsync -avzr -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress cognos1.contoso.com:/opt/ibm/cognos/analytics/wlp/usr/servers/cognosserver/workarea/*.log .cognos_logs/wlp/workarea
echo "filebeat starting"
filebeat.sh -path.config ./ -path.data ./fb_temp -path.logs ./fb_temp -E=cognos_filebeat -once
echo "filebeat done"