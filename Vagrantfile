# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"

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
    sudo apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    sudo sh -c 'echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list'
    sudo apt-cache policy docker-engine
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install -y docker-engine python-pip
    sudo pip install docker-compose
    sudo usermod -aG docker vagrant
    sudo -u vagrant pip install docker-compose
    sudo docker-compose -f /vagrant/docker-compose.yml up -d
  SHELL

end
