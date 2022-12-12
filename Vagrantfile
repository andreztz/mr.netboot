# -*- mode: ruby -*-
# vi: set ft=ruby :


# VAGRANT_BOX = "debian/buster64"
VAGRANT_BOX = "archlinux/archlinux"
# VAGRANT_BOX = "ubuntu/xenial64"


Vagrant.configure("2") do |config|
  config.vm.box = VAGRANT_BOX
  # config.vm.provider :libvirt do |domain|
  #   domain.uri = 'qemu+unix:///system'
  #   domain.driver = 'kvm'
  #   domain.host = "pxeserver"
  #   domain.cpus = 1
  #   domain.memory = 512
  # end 
  # config.vm.network :public_network, 
  #   :type => "bridge" , 
  #   :dev => "bridge0", 
  #   :mode => "bridge"
  config.vm.synced_folder "data/www", "/www", 
     owner: "ztz", group: "wheel"
  config.vm.network :public_network, :bridge => "bridge0", :ip => "192.168.1.100"
  config.vm.provision "ansible", playbook: "bootstrap.yaml"
end
