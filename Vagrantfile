# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_plugin 'vagrant-libvirt'
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'libvirt'

# # This is only needed if you are using the plugin from sources with bundler
# Vagrant.require_plugin 'vagrant-lxc'

Vagrant.configure("2") do |config|
  config.vm.box = "debian7-dev"
  config.vm.box_url = "http://cdn.quicker.fr/vagrant/libvirt/debian7-dev.box"
  config.vm.hostname = "colmet-web-devel"


  # shared folders
  config.vm.synced_folder ".", "/vagrant", :nfs => true

  # Provision
  config.vm.provision "shell", privileged: false, inline: <<-EOF
    sudo easy_install pip==1.3.1 fabtools virtualenvwrapper
    fab -f /vagrant/fabfile.py bootstrap
    cat > ~/bash_profile <<< "
    source ~/.profile
    source /vagrant/.env
    cd /vagrant
    workon colmet
    "
  EOF

  # Configure provider
  config.vm.provider :libvirt do |domain|
    domain.memory = 1024
    domain.cpus = 2
  end

  # Network
  config.ssh.forward_agent = true
  config.vm.network :private_network, ip: "10.10.10.140"

  # Copy my conf
  if File.exists? File.expand_path('~/.dotfiles')
    config.vm.synced_folder "~/.dotfiles", "/home/vagrant/.dotfiles", :nfs => true
    config.vm.synced_folder "~/.dotfiles", "/root/.dotfiles", :nfs => true
    config.vm.provision "shell", privileged: false, inline: "python /home/vagrant/.dotfiles/install.py"
    config.vm.provision "shell", privileged: true, inline: "sudo su - -c 'python /root/.dotfiles/install.py'"
  end

end
