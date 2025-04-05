FROM untergeek/curator:9.0.0

USER root

RUN >>/var/spool/cron/crontabs/nobody \
    echo '* * * * * /curator/curator /.curator/delete_log_files_curator.yml'

ENTRYPOINT ["crond"]
CMD ["-f", "-d8"]
