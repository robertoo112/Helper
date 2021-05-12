
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

@app.route("/external/<action>", methods = ["POST"])
def external(action):
    if action == "mongo":
        message = ops.mongo_external()
    else:
        message = ops.mysql_external()
    flash(message, category='error')        
    return render_template('index2.html', kubernetesObjects = ops.get_kubernetesObejects() , docker_images = ops.docker_images)

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
        if ops.deploys.count(form.get('name')) < 0 or form.get('name') == None:
            flash("Nombre de deploy repetido o Incompleto", category='error')
        elif (ops.used_ports.count(form.get('nodePort')) > 0) or form.get('nodePort') == None or (31000 >= int(form.get('nodePort')) >= 32000):
            flash("Puerto ya usado o Incompleto", category='error')
        elif form.get('deploy') != '3' and (form.get('hostname-service') == None or form.get('user') == None or form.get('password') == None):
            flash("Es necesario introducir las variables para la base de datos",category='error')
        else:
            ops.kubernetes_deploy(form)
            flash("Deploy generado, accesible desde http://master-ip:"+form.get('nodePort'), category='success')
            return render_template('index2.html', kubernetesObjects = ops.get_kubernetesObejects(), images = ops.docker_images, databases = ops.databases, ports = ops.used_ports)
        
    return render_template('create_deploy.html', kubernetesObjects = ops.get_kubernetesObejects(), docker_images = ops.docker_images, databases = ops.databases, ports = ops.used_ports)

@app.route("/add_Image",  methods = ["POST", "GET"])
def add_Image():
    if request.method == "POST":
        form = request.form.to_dict()
        print(form)
        base_image = form.get('OS')
        giturl = form.get('git')
        # b = giturl.split('/')
        # if b[-1].split('.').count('git') != 1:
        #     form.update({'git':"./"+b[-1]})
        # else:
        #     form.update({'git':"./"+b[-1].split('.')[0]})
        form.update({'git': './gitrepo'})
        form['url'] = giturl
        if base_image ==  "Apache":
            if form.get('git_conf') != "":
                form.update({'git_conf': "cp "+form.get('git_conf')+" /usr/local/apache2/conf/httpd.conf"})
            else: 
                form.pop('git_conf')
            form.update({'git': "cp "+form.get('git')+" /usr/local/apache2/htdocs"})        
        elif base_image ==  "Tomcat":
            form.update({'git': "cp "+form.get('git')+" /usr/local/tomcat/webapps"})
        else: 
            if form.get('path') == None:
                form.update({"git": "cp "+form.get('git')+" /opt/source_code/"})
            else:
                form.update({"git": "cp "+form.get('git')+" "+form.pop('path')}) 
        if ops.docker_images.count(form.get('nombre')) > 0 or form.get('nombre') == None:
            flash("Nombre de imagen repetido", category='error')
        out = ops.generate_image(form)
        print("desoues")
        #return redirect(url_for('app.default'))
        return""
        #return redirect(url_for('default'))
    return render_template('add_Image.html', kubernetesObjects = ops.get_kubernetesObejects(), images = list(ops.OS.keys()), databases = ops.databases, ports = ops.used_ports)
        
    flash("algooo")

@app.route("/provide_service")
def create_service():
    return ""

@app.route("/remove_app")
def rm_app():
    return ""

@app.route("/kubernetes_dashboard")
def dashboard():
    return ""
        

#@app.route("/deploy")



if __name__ == "__main__":
    if os.path.exists("./dockerfiles") == False:
        os.mkdir("dockerfiles")
    if os.path.exists("./kubernetes") == False:
        os.mkdir("./kubernetes")
        
    app.run(host="0.0.0.0", port = 8080, debug = True)

