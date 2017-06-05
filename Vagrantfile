# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision :shell, :inline => "sudo apt-get update"
  config.vm.provision :shell, :inline => "sudo apt-get install curl -y"
  config.vm.provision :shell, :inline => "sudo apt-get install vim -y"

  config.vm.provision :shell, :inline => "curl -sSL https://get.docker.com/gpg | sudo apt-key add -"
  config.vm.provision :shell, :inline => "curl -sSL https://get.docker.com/ | sh"
  config.vm.provision :shell, :inline => "curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` > docker-compose; chmod +x docker-compose; sudo mv docker-compose /usr/local/bin/docker-compose"
  config.vm.provision :shell, :inline => "sudo usermod -aG docker vagrant"
    
  config.vm.provision :shell, :inline => "cd /vagrant/ && docker-compose up -d"  
  
  config.vm.provision :shell, :inline => "echo All done, go visit http://localhost:5601 !"

  config.vm.forward_port 5000, 5000 # Logstash
  config.vm.forward_port 9200, 9200 # Elasticsearch HTTP
  config.vm.forward_port 9300, 9300 # Elasticsearch TCP transport
  config.vm.forward_port 5601, 5601 # Kibana
  
end

Vagrant.configure("2") do |config|

config.vm.provider :virtualbox do |virtualbox|

virtualbox.customize ["modifyvm", :id, "--memory", "1024"]

end
end
