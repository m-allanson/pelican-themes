# encoding: utf-8
# This file originally created at http://rove.io/2c8d9877d12b1e1c054628682ce4aac9

# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.network :forwarded_port, guest: 3000, host: 3000
  config.vm.network :forwarded_port, guest: 3001, host: 3001
  config.ssh.forward_agent = false

  config.librarian_chef.cheffile_dir = "provisioning"

  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = ["provisioning/cookbooks"]
    chef.add_recipe :apt
    chef.add_recipe 'unattended-upgrades'
    chef.add_recipe 'vim'
    chef.add_recipe 'nodejs'
    chef.add_recipe 'git'
    chef.json = {
      :git => {
        :prefix => "/usr/local"
      }
    }
  end

  # config.vm.provision :shell, :path => "provisioning/provision.sh"
  config.vm.provision :shell, :inline => <<-SH
    export GITHUB_API_KEY=`cat /vagrant/provisioning/GITHUB_API_KEY.dat`
    /vagrant/provisioning/provision.sh
  SH
end
