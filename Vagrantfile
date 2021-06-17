# -*- mode: ruby -*-
# vi: set ft=ruby :
IMAGE_NAME = "bento/ubuntu-20.04"

NODES = 2

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.ssh.insert_key = false



  config.vm.provider "virtualbox" do |v|
      v.memory = 1624
      v.cpus = 2
  end
 
  config.vm.box_check_update = false




  config.vm.define "k8s-master" do |master|
        master.vm.box = IMAGE_NAME
        master.vm.network "private_network", ip: "192.168.50.20"
        master.vm.hostname = "k8s-master"
   end

   (1..NODES).each do |i|
       config.vm.define "node-#{i}" do |node|
           node.vm.box = IMAGE_NAME
           node.vm.network "private_network", ip: "192.168.50.#{i + 20}"
           node.vm.hostname = "node-#{i}"
	   
	   if i == NODES
	     node.vm.provision "ansible" do |ansible|
	         ansible.limit = "all"
	         ansible.playbook = "./ansible/site.yaml"
           #ansible.tags = "app"
           #ansible.verbose = "vvv"
		 ansible.host_vars = {
		    "k8s-master" => {"ansible_ssh_host" => "192.168.50.20", "ansible_port" => "22", "ansible_ssh_pass" => "vagrant"},
		    "node-1" => {"ansible_ssh_host" => "192.168.50.21", "ansible_port" => "22", "ansible_ssh_pass" => "vagrant"},
		    "node-2" =>  {"ansible_ssh_host" => "192.168.50.22", "ansible_port" => "22", "ansible_ssh_pass" => "vagrant"}
                 }
                 ansible.groups = {
		   "master" => ["k8s-master"],
		   "nodes" => ["node-1", "node-2"]
		 }
             end 
           end
     end
   end
#   config.vm.provision "ansible" do |ansible|
#       ansible.playbook = "./ansible/site.yaml"
#       ansible.host_vars = {
#          "k8s-master" => {"ansible_host" => "192.168.50.10"},
#	  "node-1" => {"ansible_host" => "192.168.50.11"},
#	  "node-2" =>  {"ansible_host" => "192.168.50.12"}
#       }
#       ansible.groups = {
#       "master" => ["k8s-master"],
#       "nodes" => ["node-1", "node-2"]
#       }
#   end
end
