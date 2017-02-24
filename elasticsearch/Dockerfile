FROM elasticsearch:5.2

COPY config/ /etc/elasticsearch

RUN elasticsearch-plugin install --batch com.floragunn:search-guard-5:5.2.0-10

RUN printf "#!/bin/bash\n/usr/share/elasticsearch/plugins/search-guard-5/tools/sgadmin.sh -cd /etc/elasticsearch -ts /etc/elasticsearch/truststore.jks -ks /etc/elasticsearch/kirk-keystore.jks -nhnv -icl" > /init_sg.sh

RUN chmod +x /usr/share/elasticsearch/plugins/search-guard-5/tools/sgadmin.sh
RUN chmod +x /init_sg.sh

CMD ["-E", "path.conf=/etc/elasticsearch", "-E", "network.host=0.0.0.0", "-E", "discovery.zen.minimum_master_nodes=1"]
