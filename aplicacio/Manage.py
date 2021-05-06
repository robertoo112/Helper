import json
import os


class Manage:
    def __init__(self, x):
        self.x = x
        self.OS = {'Ubuntu': 'ubuntuimage', 'Centos7':'centosimage'}
        self.unix_commands = {"cp": "ADD","pip": "RUN", "pip3": "RUN", "chmod": "RUN", "apt-get": "RUN",
        "apt": "RUN", "yum": "RUN", "dnf": "RUN", "python": "CMD", "wget": "RUN", "curl": "RUN", "chown": "RUN",
        "chgrp":"RUN", "cd": "WORKDIR", "tar": "RUN", "rm": "RUN", "echo": "RUN", "set": "RUN"}
        self.databases = {'MongoDB':{'deployed': False, 'configMap': 'mongo-config', 'secret':'mongo-user' }, 'MySQL' :{'deployed': False, 'configMap': 'mysql-config', 'secret':'mysql-user' }}
        self.servers = ['apache', 'apache-tomcat']
        self.docker_registry = "trow.kube-public:31000/"
        self.deploys = ['asdas','fasdfasd','fasdfa', 'Robert']
        self.services = ['asdas','fasdfasd','fasdfa']
        self.persistentVolumes = []
        self.pvClaims = ['asdas','fasdfasd','fasdfa']
        self.secrets = [] 
        self.configMaps = ['asdas','fasdfasd','fasdfa']
        self.kubernetesObjects = {'services': self.services,'deploys': self.deploys,'persistentVolumes': self.persistentVolumes,'secrets': self.secrets,'configMaps': self.configMaps }
        self.docker_images = {'iamge1','image2'}
        self.deploy_options = {'Back-end o Front-end con servicio externo y BBDD', 'Front con servicio externo, enlazado con Back-end con BDD', 'Back-end o Front-end con servicio externo'}
        self.used_ports = ['31000','32000']

    def get_image_from_docker_hub(self, image):
        return ""

    def get_kubernetesObejects(self):
        return self.kubernetesObjects
    
    def create_services(self, name, nodePort):
        return""


    def push_image(self, dockerFile, image_name):
        os.mkdir("./dockerfiles/"+image_name)
        file = open("./dockerfiles/"+image_name+"/dockerFile.txt", "a")
        file.write(dockerFile)
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
        for key, value in dict.items():
            print(key)
            if key == "OS":
                os_image = self.OS[value]
                dockerFile += "FROM "+os_image
            elif (key == "nombre"):
                image_name = value
            else:
                print(value)
                action = self.add_command(value)
                if action == "error":
                    return "error"
                dockerFile += "\n"+action
                print(value + "esto es lo que pido")
        self.push_image(dockerFile, image_name)
        return dockerFile

    def kubernetes_deploy(self, args):
        yaml = ""
        print(args)
        deployType = args.get('deploy')
        print(deployType)
        if deployType == '1' or deployType == '3': 
            name = args.get('name')
            nodePort = args.get('nodePort')
            image = args.get('docker')
            containerPort = args.get('containerPort')
            tier = 'polivalente'
            print(args.get('database'))
            database = self.databases.get(args.get('database'))
            vHostname = args.get('hostname-service')
            vUser = args.get('user')
            vPassword = args.get('password')
            yaml += self.create_deployment(tier, name, containerPort, image, database, vHostname, vUser, vPassword)
            yaml += self.create_service(name, nodePort, tier, "", containerPort)
            self.deploy_yaml( yaml, name)
        else:
            yaml += self.create_deployment(tier, name, containerPort, image, database, vHostname, vUser, vPassword)
            yaml += self.create_service(name, nodePort, tier, "", containerPort)
            self.deploy_yaml( yaml, name)
        return ""
    
    def deploy_yaml(self, yaml, yaml_name):
        if os.path.exists("./kubernetes/"+yaml_name) == False:
            os.mkdir("./kubernetes/"+yaml_name)
        file = open("./kubernetes/"+yaml_name+"/deploy-"+yaml_name+".yaml", "a")
        file.write(yaml)
    
    def deploy_database(self, type):
        self.databases.update({type: True})
        """enviar peticion de deploy a la que sea"""

    """ targetPort hace referencia al puerto del Pod al que apuntará el servicio"""
    def create_service(self, name, nodePort, tier, port, targetPort): 
        service = ""
        service ="""\n--- \n
apiVersion: v1
kind: Service
metadata:
    labels:
        app: """+name+"""
        
    name: """+name+"""-svc-add
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

    def create_deployment(self, tier, name, containerPort, image, database, vHostname, vUser, vPassword):
        # if self.databases.get(database).get('deployed') == False:
        #     self.deploy_database(database)
        deploy = ""
        deploy = """\n---\n 
apiVersion: apps/v1
kind: Deployment
metadata:
    name: """+name+"""
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
        if database !=None:
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
        return deploy
                                

