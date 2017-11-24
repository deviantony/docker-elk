# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |v|
    v.name = "ELK_vagrant"
    v.memory = 4096
    v.cpus = 2
  end

  config.vm.box_check_update = true

  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "forwarded_port", guest: 5601, host: 5601
  config.vm.network "forwarded_port", guest: 9200, host: 9200
  config.vm.network "forwarded_port", guest: 9300, host: 9300

  #SSH
  config.ssh.forward_agent = true

  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  #Provision
  config.vm.provision "shell", inline: <<-SHELL
    sudo touch /var/lib/cloud/instance/locale-check.skip
    echo "vm.max_map_count=262144" | sudo tee /etc/sysctl.d/10-elasticsearch.conf
    sudo sysctl -p --system
    sudo apt update
    sudo apt -y full-upgrade
    sudo apt -y install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install -y docker-ce python-pip
    sudo pip install docker-compose
    sudo usermod -aG docker vagrant
    pip install docker-compose
    cd /vagrant && docker-compose up -d
  SHELL

end
