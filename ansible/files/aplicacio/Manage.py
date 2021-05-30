import json
import os
import time
import subprocess as sp

class Manage:
    def __init__(self, x):
        self.x = x
        self.OS = {'Ubuntu': 'ubuntu', 'Centos7':'centos', 'Apache': 'httpd', 'Tomcat': 'tomcat'}
        self.unix_commands = {"cp": "ADD","pip": "RUN", "pip3": "RUN", "chmod": "RUN", "apt-get": "RUN",
        "apt": "RUN", "yum": "RUN", "dnf": "RUN", "python": "CMD", "wget": "RUN", "curl": "RUN", "chown": "RUN", "python3" : "CMD",
        "chgrp":"RUN", "cd": "WORKDIR", "tar": "RUN", "rm": "RUN", "echo": "RUN", "set": "RUN", "httpd": "CMD", "catalina.sh": "CMD", "node": "CMD", "npm" : "run"}
        self.databases = {'MongoDB':{'deployed': False, 'configMap': 'mongo-config', 'secret':'mongo-user', 'external': False, 'nodePort':'30017', 'user': 'admin', 'password': 'admin'},
                          'MySQL' :{'deployed': False, 'configMap': 'mysql-config', 'secret':'mysql-user', 'external': False, 'nodePort':'30036', 'user': 'root', 'password': 'admin'  }}
        self.docker_registry = "trow.kube-public:31000/"
        self.deploys = ['asdas','fasdfasd','fasdfa', 'Robert']
        self.deploy = [{'App': 'nombre','deployments':['deploy1-back','deploy1-front'],'services':['svc-back','svc-front'], 'images':['imagen1']}]
        self.services = ['asdas','fasdfasd','fasdfa']
        self.persistentVolumes = []
        self.pvClaims = ['asdas','fasdfasd','fasdfa']
        self.secrets = [] 
        self.configMaps = ['asdas','fasdfasd','fasdfa']
        self.kubernetesObjects = {'services': self.services,'deploys': self.deploys,'persistentVolumes': self.persistentVolumes,'secrets': self.secrets,'configMaps': self.configMaps }
        self.docker_images = []
        self.deploy_options = {'Back-end o Front-end con servicio externo y BBDD', 'Front con servicio externo, enlazado con Back-end con BDD', 'Back-end o Front-end con servicio externo'}
        self.used_ports = []

    def get_image_from_docker_hub(self, image):
        return ""

    def get_kubernetesObejects(self):
        return self.kubernetesObjects
    
    def create_services(self, name, nodePort):
        return""

    def get_dashboard_token(self):
        # try:
        #     token = subprocess.check_output('kubectl describe secret admin-user-token -n kubernetes-dashboard | grep token: -A1')
        # except subprocess.CalledProcessError as err:
        #     return err
        token = sp.getoutput('kubectl describe secret admin-user-token -n kubernetes-dashboard | grep token: -A1')
        return token.split()[1]

    
    def delete_app(self, index):
        var = self.deploy.pop(int(index))
        services = var.get("services")
        deployments = var.get("deployments")
        for service in services:
            os.system("kubectl delete svc "+service)
        for deployment in deployments:
            os.system("kubectl delete deployment "+deployment)
        return "Aplicacion eliminada"

    def push_image(self, dockerFile, image_name, url):
        os.mkdir("./dockerfiles/"+image_name)
        file = open("./dockerfiles/"+image_name+"/Dockerfile", "a")
        file.write(dockerFile)
        file.close()
        os.system("git clone "+url+" ./dockerfiles/"+image_name+"/gitrepo")
        time.sleep(1)
        os.system("sudo docker build ./dockerfiles/"+image_name+"/ -t "+self.docker_registry+image_name)
        time.sleep(1)
        register = os.system("sudo docker push "+self.docker_registry+image_name)
        # print(register)
        self.docker_images.append(image_name)
        return ""

    def add_command(self, command):
        provisional = command.split()
        if provisional[0] == "cp" or provisional[0] == "cd":
            command = command[3:]
        print(self.unix_commands.get(provisional[0]))
        print(type(self.unix_commands.get(provisional[0])))
        print(type(command))
        return self.unix_commands.get(provisional[0])+" "+ command


    def generate_image(self, dict): # docker build -f dockerFile -t direccionRepositorio
        #j_dict = json.dumps(dict)
        print(dict)
        image_name = ""
        os_image = ""
        dockerFile = ""
        url = ""
        for key, value in dict.items():
            print(key)
            if key == "OS":
                os_image = self.OS[value]
                dockerFile += "FROM "+self.docker_registry+os_image
            elif (key == "nombre"):
                image_name = value
            elif key == "url":
                url = value
            else:
                print(value)
                action = self.add_command(value)
                if action == "error":
                    return "error"
                dockerFile += "\n"+action
                print(value + "esto es lo que pido")
        
        if dict.get('OS') == "Tomcat":
            dockerFile+= "\nCMD [“catalina.sh”, “run”]"
        self.push_image(dockerFile, image_name, url)
        return dockerFile

    def kubernetes_deploy(self, args):
        yaml = ""
        deploy = {}
        print(args)
        deployType = args.get('deploy')
        print(deployType)
        database = self.databases.get(args.get('database'))
        if database != None and self.databases.get(args.get('database')).get('deployed') == False:
            self.deploy_database(args.get('database'))
        name = args.get('name')
        if deployType == '1' or deployType == '3': 
            nodePort = args.get('nodePort')
            image = args.get('docker')
            containerPort = args.get('containerPort')
            tier = 'polivalente'
            print(args.get('database'))
            vHostname = args.get('hostname-service')
            vUser = args.get('user')
            vPassword = args.get('password')
            yaml += self.create_deployment(tier, name, name, containerPort, image, database, vHostname, vUser, vPassword)
            yaml += self.create_service(name, name, nodePort, tier, "", containerPort)
            deploy = {'App': name,'deployments':[name],'services':[name+"-svc-add"], 'images' : [image], 'port': nodePort}
            self.deploy_yaml( yaml, name)
            self.deploy.append(deploy)
            self.used_ports.append(nodePort)
        else:
            """front"""
            name_front = args.get('name')+"-front"
            image_front = args.get('docker-front')
            containerPort_front = args.get('containerPort')
            nodePort = args.get('nodePort')
            vHostname_back = args.get('hostname-service-back')
            tier = 'front'
            yaml += self.create_deployment(tier, name, name_front, containerPort_front, image_front, None, vHostname_back, "vUser", "vPassword")
            yaml += self.create_service(name, name_front, nodePort, tier, "port", containerPort_front)
            """back"""
            tier = 'back'
            name_back = args.get('name')+"-back"
            image_back = args.get('docker-back')
            containerPort_back = args.get('port-back')
            vHostname = args.get('hostname-service')
            vUser = args.get('user')
            vPassword = args.get('password')
            yaml += self.create_deployment(tier, name, name_back, containerPort_back, image_back, database, vHostname, vUser, vPassword)
            yaml += self.create_service(name, name_back, "", tier, containerPort_back, containerPort_back)
            deploy = {'App': name,'deployments':[name_back,name_front],'services':[name_back+"-svc-add",name_front+"-svc-add"], 'images' : [image_back, image_front], 'port': nodePort}
            self.deploy_yaml( yaml, name)
            self.deploy.append(deploy)
            self.used_ports.append(nodePort)
        return ""
    
    def deploy_yaml(self, yaml, yaml_name):
        if os.path.exists("./kubernetes/"+yaml_name) == False:
            os.mkdir("./kubernetes/"+yaml_name)
        file = open("./kubernetes/"+yaml_name+"/deploy-"+yaml_name+".yaml", "a")
        file.write(yaml)
        file.close()
        os.system("kubectl create -f ./kubernetes/"+yaml_name+"/deploy-"+yaml_name+".yaml")
    
    def mysql_external(self):
        if self.databases.get("MySQL").get("deployed") == False: 
            return "MySQL no esta activa"
        elif self.databases.get("MySQL").get("external") == True:
            return "MySQL visible en el puerto "+self.databases.get("MySQL").get("nodePort")+" con usuario root y contraseña"+ self.databases.get("MySQL").get("password")           
        else:
            os.system("kubectl create -f ./templates/nodeport-mysql.yaml")
            return "MySQL visible en el puerto "+self.databases.get("MySQL").get("nodePort")+" con usuario root y contraseña"+ self.databases.get("MySQL").get("password")

    def mongo_external(self):
        if self.databases.get("MongoDB").get("deployed") == False: 
            return "MongoDB no esta activa"
        elif self.databases.get("MongoDB").get("external") == True:
            return "MongoDB visible en el puerto "+self.databases.get("MongoDB").get("nodePort")+" con usuario admin y contraseña"+ self.databases.get("MongoDB").get("password")           
        else:
            os.system("kubectl create -f ./templates/nodeport-mongo.yaml")
            return "MongoDB visible en el puerto "+self.databases.get("MongoDB").get("nodePort")+" con usuario admin y contraseña"+ self.databases.get("MongoDB").get("password")
    
    def deploy_database(self, type):
        self.databases.get(type).update({'deployed': True})
        if type == "MySQL":
            os.system('kubectl apply -f ./templates/mysql.yaml')
        else:
            os.system('kubectl apply -f ./templates/mongodb.yaml')
        """enviar peticion de deploy a la que sea"""
        time.sleep(5)

    """ targetPort hace referencia al puerto del Pod al que apuntará el servicio"""
    def create_service(self, name, deployName, nodePort, tier, port, targetPort): 
        service = ""
        service ="""\n--- \n
apiVersion: v1
kind: Service
metadata:
    labels:
        app: """+name+"""
        
    name: """+deployName+"""-svc-add
spec:
    selector:
        app: """+name+"""
        type: """+tier
        if nodePort != "":
            service += """
    type: NodePort
    ports:
        - port: """+targetPort+"""
          targetPort: """+targetPort+"""
          nodePort: """+nodePort
        else:
            service += """
    type: ClusterIP
    ports:
        - port: """+port+"""
          targetPort: """+targetPort
        
        return service

    def create_deployment(self, tier, name, deployName, containerPort, image, database, vHostname, vUser, vPassword):
        deploy = ""
        deploy = """\n---\n 
apiVersion: apps/v1
kind: Deployment
metadata:
    name: """+deployName+"""
    labels:
        app: """+name+"""
        type: """+tier+"""
spec:
    replicas: 1
    selector:
        matchLabels:
            app: """+name+"""
            type: """+tier+ """
    template:
        metadata:
            labels:
                app: """+name+ """
                type: """+tier+ """
        spec:
            containers:
                - name: """+name+ """-container
                  image: """+self.docker_registry+image+"""
                  ports:
                  - containerPort: """+containerPort+"""
                    name: """+name+"""-port"""
        if database != None:
            deploy += """
                  env:
                    - name: """+vHostname+"""
                      valueFrom:
                        configMapKeyRef:
                            name: """+ database.get('configMap') +"""
                            key: hostname
                    - name: """+vUser+"""
                      valueFrom:
                        secretKeyRef:
                            name: """+ database.get('secret') +"""
                            key: username
                    - name: """+vPassword+"""
                      valueFrom:
                        secretKeyRef:
                            name: """+database.get('secret')+"""
                            key: password"""
        elif deployName.split('-') == [name,"front"]:
            deploy += """
                    env:
                      - name: """+vHostname+"""
                        value: """+name+"""-back-svc-add"""
        return deploy
                                

