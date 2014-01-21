# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
  config.vm.box = "debian7-dev"
  config.vm.box_url = "http://cdn.quicker.fr/vagrant/virtualbox/debian7-dev.box"
  config.vm.hostname = "colmet-web-devel"

  # shared folders
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  # Provision
  config.vm.provision "shell", privileged: false, inline: <<-EOF
    # prepare sample hdf5 data
    git show sample-data:colmet.hdf5 > /tmp/colmet.hdf5

    sudo easy_install pip==1.3.1 fabtools
    fab -f /vagrant/fabfile.py bootstrap
    cat > ~/.bash_profile <<< "
    export FORCE_AUTOENV=1
    source ~/.profile
    source /vagrant/.env
    cd /vagrant
    "
  EOF

  # Configure provider
  config.vm.provider :virtualbox do |domain|
    domain.memory = 1024
    domain.cpus = 2
  end

  # Network
  config.ssh.forward_agent = true
  config.vm.network :private_network, ip: "10.10.10.140"

  # Improve provision speed
  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.auto_detect = true
    config.cache.enable_nfs  = true
  end

  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http = "http://10.10.10.1:8123/"
    config.proxy.https = "http://10.10.10.1:8123/"
    config.proxy.ftp = "http://10.10.10.1:8123/"
    config.proxy.no_proxy = "localhost,127.0.0.1"
    config.env_proxy.http = "http://10.10.10.1:8123/"
    config.env_proxy.https = "http://10.10.10.1:8123/"
    config.env_proxy.ftp = "http://10.10.10.1:8123/"
    config.env_proxy.no_proxy = "localhost,127.0.0.1"
  end


  # Copy my conf
  if File.exists? File.expand_path('~/.dotfiles')
    config.vm.synced_folder "~/.dotfiles", "/home/vagrant/.dotfiles", type: "nfs"
    config.vm.synced_folder "~/.dotfiles", "/root/.dotfiles", type: "nfs"
    config.vm.provision "shell", privileged: false, inline: "python /home/vagrant/.dotfiles/install.py"
    config.vm.provision "shell", privileged: true, inline: "sudo su - -c 'python /root/.dotfiles/install.py'"
  end
end
