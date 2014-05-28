# encoding: utf-8
# This file originally created at http://rove.io/2c8d9877d12b1e1c054628682ce4aac9

# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "trusty64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.network :forwarded_port, guest: 3000, host: 3000
  config.vm.network :forwarded_port, guest: 3001, host: 3001
  config.ssh.forward_agent = false

  config.librarian_chef.cheffile_dir = "provisioning"

  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = ["provisioning/cookbooks"]
    chef.add_recipe :apt
    chef.add_recipe 'nodejs'
    chef.json = {
      :nodejs => {
        :version => "0.11.13"
      }
    }
  end

  config.vm.provision :shell, run: 'once', :path => "provisioning/provision.sh"

  # Always starts the app on 'vagrant up'
  config.vm.provision :shell, run: 'always', :inline => <<-SH
    export GITHUB_API_KEY=`cat /vagrant/provisioning/GITHUB_API_KEY.dat`
    forever start -c "node --harmony" -o /vagrant/logs/out.log -e /vagrant/logs/err.log /vagrant/server.js
  SH

  config.vm.post_up_message = "Finished booting VM.  If all went well you should see the site at http://localhost:3000"
end
