function actualizar() {
    var somePorts = '{{ ports }}';
    var a = document.getElementById('typedeploy');
    var imp = document.getElementById('imprimir');
    if (a.value == 1){
        imp.innerHTML = "<div>\n" +
           "               <h1>Datos del Back-end o Front-end</h1>\n" +
           "               <p>Imagen \n" +
           "                 <select name=\"cositas\" id=\"typedeploy\">\n" +
           "                   {% for image in docker_images %}\n" +
           "                   <option>{{ image }}</option>\n" +
           "                   {% endfor %}\n" +
           "                 </select>\n" +
           "               </p>\n" +
           "               <p>Puerto para acceder al servidor de la imagen <input type=\"text\" name=\"containerPort\" size=\"20\"></p>\n" +
           "               <p>Puerto para acceder a la aplicación desde una url http://master-ip:puerto/ (consultar puertos disponibles)<input type=\"text\" name=\"nodePort\" size=\"20\"></p>\n" +
           "               <aside>\n" +
           "                <h4>Puertos disponibles para Kubernetes 31000-32767. Puertos usados {{ ports }}</h4>\n" +
           "               </aside>" +
           "                <p> Selecciona la base de datos disponibles en el sistema\n"+
           "                   <select name=\"database\" id=\"basededatos\">\n"+
           "                      {% for key, value in databases.items() %}\n"+
           "                      <option>{{ key }}</option>\n"+
           "                      {% endfor %}\n"+
           "                   </select>\n"+
           "                </p>\n"+
           "               <h4>Nombre de las Variables de entorno para acceder a la base de datos</h4>\n" +
           "               <p>Variable para hacer referencia al Hostname de la BBDD<input type=\"text\" name=\"hostname-service\" size=\"20\"></p>\n" +
           "               <p>Variable para hacer referencia al Usuario root <input type=\"text\" name=\"user\" size=\"20\"></p>\n" +
           "               <p>Variable para hacer referencia al Password <input type=\"text\" name=\"password\" size=\"20\"></p>\n" +
           "             </div>\n ";
           
     }
     if (a.value == 2){
        imp.innerHTML = '<div>Hola32321</div>';
    }
     if (a.value == 3){
        imp.innerHTML = '<div>Hola3</div>';
     }
}
let i = 1;
let s = false;

function createNewElement() {
    // First create a DIV element.
  var txtNewInputBox = document.createElement('div');
  //s = "<input type='text' name='default"+i.toString();"'/>
    // Then add the content (a new input box) of the element.
  txtNewInputBox.innerHTML = "<input type='text' name='default"+i+"'>";

    // Finally put it where it is supposed to appear.
  document.getElementById("newElementId").appendChild(txtNewInputBox);
  i ++
}

function gitPath() {
  // First create a DIV element.
if (s == false)
    var txtNewInputBox = document.createElement('div');
    //s = "<input type='text' name='default"+i.toString();"'/>
      // Then add the content (a new input box) of the element.
    txtNewInputBox.innerHTML = "<p>Path de git:<input type='text' name='path'></p>";
  
      // Finally put it where it is supposed to appear.
    document.getElementById("newElementId").appendChild(txtNewInputBox);
    s = true;  
}