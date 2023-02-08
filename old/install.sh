#!/usr/bin/env bash


# see for more info: http://www.tecmint.com/install-elasticsearch-logstash-and-kibana-elk-stack-on-centos-rhel-7/

set -eu
set -o pipefail
sudo ls > /dev/null # get sudo rights before user walks away

CONFIGS_DIR="configs" # relative path in this repo to our configuration directory
USAGE="Usage: $0 [elasticsearch, kibana, nginx, logstash]\nNo arguments defaults to installing everything."


prepare() {
  sudo yum update -y  
  sudo yum install wget -y
  sudo yum install httpd-tools -y
}

java8() {
  
    printf "\nInstalling Java Development Kit 8\n"
    prepare
    wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u73-b02/jdk-8u73-linux-x64.rpm"
    sudo yum -y localinstall jdk-8u73-linux-x64.rpm
    rm ./*.rpm
}

elasticsearch() {
  printf "\nInstalling Elasticsearch \n"
  prepare
  
  if [[ $(java -version 2>&1) == *"1.8."* ]]; then 
    printf -- '--> JDK 8 is already installed\n'; 
  else 
    printf -- '--> Installing JDK 8\n'; 
    java8;
  fi
  
  sudo rpm --import http://packages.elastic.co/GPG-KEY-elasticsearch
  
  ELASTIC="elasticsearch.repo"
  ELASTIC_CONFIG="/etc/elasticsearch"
  ELASTIC_DEST="/etc/yum.repos.d/elasticsearch.repo"
  if [ ! -f /etc/yum.repos.d/elasticsearch.repo ]; then
     echo "[elasticsearch-5x]" >> $ELASTIC 
     echo "name=Elasticsearch repository for 5.x packages" >> $ELASTIC
     echo "baseurl=https://artifacts.elastic.co/packages/5.x/yum" >> $ELASTIC
     echo "gpgcheck=1" >> $ELASTIC
     echo "gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch" >> $ELASTIC
     echo "enabled=1" >> $ELASTIC
     echo "autorefresh=1" >> $ELASTIC
     echo "type=rpm-md" >> $ELASTIC

     sudo mv $ELASTIC $ELASTIC_DEST
  fi

  printf -- "--> installing elasticsearch from packages.elastic.co\n"  
  sudo yum install -y elasticsearch
  sudo chkconfig --add elasticsearch

  printf -- "--> moving elasticsearch configutation files\n"
  sudo cp -r configs/elasticsearch/elasticsearch.yml $ELASTIC_CONFIG
  sudo cp -r configs/elasticsearch/logging.yml $ELASTIC_CONFIG

  printf -- "--> starting the elasticsearch server\n" 
  sudo systemctl start elasticsearch

  IP=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')
  printf -- "--> elasticsearch installation complete.\n\nTest the server by issuing the following command:\n   curl -i $IP:9200\n"

}

kibana5() {
  printf "\nInstalling Kibana v5\n"
  prepare
  
  KIBANA="kibana.repo"
  KIBANA_CONFIG="/etc/kibana"
  KIBANA_DEST="/etc/yum.repos.d/kibana.repo"
  if [ ! -f /etc/yum.repos.d/kibana.repo ]; then
     echo "[kibana]" >> $KIBANA 
     echo "name=Kibana repository" >> $KIBANA
     echo "baseurl=http://packages.elastic.co/kibana/4.4/centos" >> $KIBANA
     echo "gpgcheck=1" >> $KIBANA
     echo "gpgkey=http://packages.elastic.co/GPG-KEY-elasticsearch" >> $KIBANA
     echo "enabled=1" >> $KIBANA

     sudo mv $KIBANA $KIBANA_DEST
  fi

  printf -- "--> installing kibana from packages.elastic.co"
  sudo yum install -y kibana

  printf -- "--> moving kibana configutation files\n"
  sudo cp -r configs/kibana/kibana.yml $KIBANA_CONFIG
  
  printf -- "--> starting kibana\n" 
  sudo systemctl daemon-reload
  sudo systemctl start kibana
  sudo systemctl enable kibana

  IP=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')
  printf -- "--> kibana installation complete.\n\nTest the server by issuing the following command:\n   curl -i $IP:5601\n"
}

nginx() {
  printf "\nInstalling Nginx\n" 

  prepare

  printf -- "--> installing nginx from epel-release\n"
  sudo yum install -y epel-release  
  sudo yum install -y nginx  

  printf -- "--> moving nginx configuration files\n"
  NGINX_CONFIG="/etc/nginx/conf.d"
  NGINX="/etc/nginx"
  sudo cp -r configs/nginx/kibana.conf $NGINX_CONFIG
  sudo cp -r configs/nginx/es.conf $NGINX_CONFIG
  sudo cp -r configs/nginx/nginx.conf $NGINX

  sudo systemctl start nginx
  sudo systemctl enable nginx

  IP=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')
  printf -- "--> nginx installation complete.\n\nTest the server by issuing the following commands:\n   curl -i $IP:80\n   curl -i $IP:8080\n"


  printf -- "--> creating a user account for kibana\n"
  printf -- "    username: hydroadmin\n"
  sudo htpasswd -c /etc/nginx/htpasswd.users hydroadmin 
}

logstash() {
  printf "\nInstalling Logstash\n"

  LOGSTASH="logstash.repo"
  LOGSTASH_CONFIG="/etc/logstash/conf.d"
  LOGSTASH_DEST="/etc/yum.repos.d/logstash.repo"
  if [ ! -f /etc/yum.repos.d/logstash.repo ]; then
     echo "[logstash]" >> $LOGSTASH
     echo "name=Logstash" >> $LOGSTASH
     echo "baseurl=http://packages.elasticsearch.org/logstash/2.2/centos" >> $LOGSTASH
     echo "gpgcheck=1" >> $LOGSTASH
     echo "gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch" >> $LOGSTASH
     echo "enabled=1" >> $LOGSTASH

     sudo mv $LOGSTASH $LOGSTASH_DEST
  fi

  printf -- "--> installing elasticsearch 2.2 from packages.elasticsearch.org\n"
  sudo yum install -y logstash  

  printf -- "--> moving logstash configuration files\n"
  sudo cp -r configs/logstash/*.conf $LOGSTASH_CONFIG 
  sudo cp -r configs/logstash/*.json /etc/logstash/

#  printf -- "--> testing the logstash configuration\n"
#  sudo /usr/share/logstash/bin/logstash --configtest -f $LOGSTASH_CONFIG 

  printf -- "--> starting the logstash service\n"
  sudo systemctl daemon-reload
  sudo systemctl start logstash
  sudo systemctl enable logstash
}

update_logstash_configs() {

  LOGSTASH_CONFIG="/etc/logstash/conf.d"

  printf -- "--> moving logstash configuration files\n"
  sudo cp -r configs/logstash/*.conf $LOGSTASH_CONFIG 
  sudo cp -r configs/logstash/*.json /etc/logstash/

  printf -- "--> starting the logstash service\n"
  sudo systemctl restart logstash
  
  sleep 3
  isactive logstash

  printf -- "--> testing the logstash configuration\n"
  sudo /usr/share/logstash/bin/logstash -t -f $LOGSTASH_CONFIG 


}

isactive() {
  RED='\033[0;31m'
  GRN='\033[0;32m'
  NC='\033[0m' # No Color

  if [ "`sudo systemctl is-active ${1}`" != "active" ]; then
    echo -e "${RED} [-] ${1} is not running${NC}\n"
  else  
    echo -e "${GRN} [+] ${1} is running${NC}\n" 
  fi
}

firewall() {

  printf "\nStarting Firewalld\n" 
  sudo systemctl start firewalld
  sudo systemctl enable firewalld

  printf "\nConfiguring Firewall\n"
  sudo firewall-cmd --zone=public --add-port=5044/tcp --permanent
  sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
  sudo firewall-cmd --zone=public --add-port=81/tcp --permanent
  sudo firewall-cmd --zone=public --add-port=8080/tcp --permanent
  sudo firewall-cmd --reload

  printf -- "--> opened ports\n"
  sudo firewall-cmd --zone=public --list-ports
}


get_status() {

  IP=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')

  isactive elasticsearch
  isactive kibana
  isactive nginx
  isactive logstash
  isactive firewalld
  
  printf -- "--> To watch ES indices build, issue the following command: \n"
  printf -- "    $ watch curl -XGET $IP:9200/_cat/indices?v\n\n" 
  printf -- "   Kibana (readonly) \n"
  printf -- "   $IP:80 \n"
  printf -- "   Kibana (hydroadmin, password protected) \n"
  printf -- "   $IP:81 \n"
  printf -- "   Kibana API (readonly) \n"
  printf -- "   $IP:8080 \n\n"

}

all() {
  # Install everything
  elasticsearch
  kibana5
  nginx
  logstash
  firewall
}

display_usage() {
   echo "*** HydroShare ELK Metrics Control Script ***"
   echo "usage: $0 install-elastic      # install and configure elasticsearch v5.x"
   echo "usage: $0 install-kibana       # install and configure Kibana v5"
   echo "usage: $0 install-nginx        # install and configure nginx"
   echo "usage: $0 install-logstash     # install and configure logstash v2.2"
   echo "usage: $0 install-firewall     # install and configure firewalld"
   echo "usage: $0 install-all          # install and configure all ELK components"
   echo "usage: $0 configure-logstash   # copy logstash configurations and restart logstash"
   echo "usage: $0 status               # display the status of the ELK services"
   echo "***"
}

#echo $1 ${2:-}
if [ $# -eq 0 ] ; then
    display_usage
    exit 1
fi

case "$1" in
    "install-elastic") elasticsearch
        ;;
    "install-kibana") kibana5
        ;;
    "install-nginx") nginx
        ;;
    "install-logstash") logstash
        ;;
    "install-firewall") firewall
        ;;
    "install-all") all 
        ;;
    "configure-logstash") update_logstash_configs
    ;;
    "status") get_status
    ;;
    *) display_usage
        ;;
esac

exit 0;




