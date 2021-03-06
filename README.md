# Helper
The purpose of this project is about a system to prepare environments in which a developer can do his own tests or releases.
The developer will be able to launch two or more machines locally in which a cluster of Kubernetes will be established, a tool for error control and performance monitoring on deployed applications, where he will be able to launch his own software. It will also incorporate a web interface already launched within the environment with which make application deployments more easily.

For the local environment, there is a Vagrantfile that creates the specified virtual machines and then runs an Ansible script that configures the entire system.  
Vagrant is a tool that helps us create and manage virtual machines with the same work environment. Ansible is a software that automates software provisioning, configuration management, and application deployment.

To execute the environment, is required to have installed Vagrant, Ansible and Oracle VM VirtualBox 6.0.10. To start the environment just execute vagrant up at the same directory where de Vagrantfile is located.
It is also necessary have all the images used (centos, httpd, mongo, mysql, tomcat and ubuntu from Docker Hub) in tar files at /ansible/files/docker_images.
