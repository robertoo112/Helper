
from flask import Flask, Response, request, render_template, redirect, url_for, flash
import json
from Manage import Manage
import os

# https://upcommons.upc.edu/handle/2099.1/1442
app = Flask(__name__)
ops = Manage(5)
app.secret_key = 'mysecretkey'

@app.route("/")
def default():
    data = ops.get_kubernetesObejects()
    data2 = ops.docker_images
    print(data)
    return render_template('index2.html', kubernetesObjects = ops.get_kubernetesObejects() , docker_images = ops.docker_images)

@app.route("/upload_docker_image")
def upload_docker_image():
    return ""

@app.route("/do/<action>")
def do(action):
    deploys = ops.deploy_options
    images = ops.docker_images
    nodePorts = ops.used_ports
    data = ops.databases
    return render_template(action+'.html', options = deploys, docker_images = images, ports = nodePorts, databases = ops.databases)

@app.route("/create_deploy", methods = ["POST", "GET"])
def create_deploy():
    if request.method == "POST":
        form = request.form.to_dict()
        if ops.deploys.count(form.get('nombre')) > 0 or form.get('nombre') == '':
            flash("Nombre de deploy repetido", category='error')
        elif ops.used_ports.count(form.get('nodePort')) > 0 or (31000 >= int(form.get('nodePort')) >= 32000):
            flash("Puerto ya usado", category='error')
        elif form.get('hostname-service') == "" or form.get('user') == "" or form.get('password') == "":
            flash("Es necesario introducir las variables para la base de datos",category='error')
        else:
            ops.kubernetes_deploy(form)
            flash("Deploy generado, accesible desde http://master-ip:"+form.get('nodePort'), category='success')
            return render_template('index2.html', kubernetesObjects = ops.get_kubernetesObejects(), images = ops.docker_images, databases = ops.databases, ports = ops.used_ports)
        
    return render_template('create_deploy.html', kubernetesObjects = ops.get_kubernetesObejects(), docker_images = ops.docker_images, databases = ops.databases, ports = ops.used_ports)

@app.route("/provide_service")
def create_service():
    return ""

@app.route("/remove_app")
def rm_app():
    return ""

@app.route("/kubernetes_dashboard")
def dashboard():
    return ""

@app.route("/add_Image",  methods = ["POST"])
def add_Image():
    if request.method == "POST":
        print("antes")
        form = request.form.to_dict()
        if form.get("path") == None:
            actualizar = "cp "+form.get("git")+" /opt/source_code"
        else:
            actualizar = "cp "+form.get("git")+" "+form.pop("path")
        form.update({"git": actualizar})
        out = ops.generate_image(form)
        print("desoues")
        #return redirect(url_for('app.default'))
        
    flash("algooo")
    return redirect(url_for('default'))
        

#@app.route("/deploy")



if __name__ == "__main__":
    if os.path.exists("./dockerfiles") == False:
        os.mkdir("dockerfiles")
    if os.path.exists("./kubernetes") == False:
        os.mkdir("./kubernetes")
        
    app.run(port = 3000, debug = True)

