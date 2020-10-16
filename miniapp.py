# 1.- FORMA HTML - Recibir un archivo del usuario - Vista
# 2.- Limitar el tipo de archivo y Guardar archivo PDF en una carpeta - Controlador
# 3.- Extraer datos del archivo - Controlador
# 4.- Almacenamos los datos en la BD - Modelo
# 5.- Mostrar los datos cargados al usuario - Vista

from flask import Flask, render_template, request, session, logging, url_for,redirect,json,flash    
from flaskext.mysql import MySQL
import os
from PyPDF4 import PdfFileReader
from pathlib import Path
import Modelo as Modelo
import time
import re

app = Flask(__name__)

app.secret_key="holayadios"

app.config['UPLOAD_FOLDER'] = 'ArchivosPDF'
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']

def guardarArchivo(_archivo):
    try:
        if _archivo.filename != '':
            file_ext=os.path.splitext(_archivo.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return False
            _archivo.save(os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], _archivo.filename)))
            return True
        return False
    except Exception as e:
        print(str(e))
        return False

def extraerDatos(_nombrearchivo):
    pdf_reader=PdfFileReader(os.path.join(app.config['UPLOAD_FOLDER'], _nombrearchivo))
    output_file_path= Path.cwd() / "TextoParaParseo.txt"
    with output_file_path.open(mode="w") as output_file:
        title = pdf_reader.documentInfo.title
        num_pages = pdf_reader.getNumPages()
        output_file.write(f"{title}\\nNumber of pages: {num_pages}\\n\\n")
        for page in pdf_reader.pages:
            text=page.extractText()
            output_file.write(text)
    print('abriendo archivo...')
    time.sleep(3)
    _textoaparsear=open('TextoParaParseo.txt', 'r')  
    _contenido=_textoaparsear.read()
    print("Contenido ",_contenido)
    return _contenido

def ParseoTexto(_texto):
    _patron = (r"ID CURSO:\n"
	r"\d{3} NOMBRE\n"
	r"\s\n"
	r"CURSO:\n"
	r"\w+ \w+ \w+ FECHA:\d{2}\/\d{2}\/\d{4}\n"
	r"\s\n"
	r"CURSANTES\n"
	r"\s\n"
	r"C\n"
	r"LAVE\n"
	r":\n"
	r"\w+\n"
	r"\s\n"
	r"NOMBRE:\n"
	r"(\w+)\n"
	r"\s\n"
	r"\s\n"
	r"APELLIDOS:\n"
	r"(\w+ \w+)\n"
	r"\s\n"
	r"\s\n"
	r"CORREO:\n"
	r"(^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,3}$)\n"
	r"\s\n"
	r"TELEFONO:\n"
	r"(\d+)\n"
	r"\s\n"
	r"CLAVE: (\w+)\n"
	r"\s\n"
	r"NOMBRE: (\w+)\n"
	r"\s\n"
	r"APELLIDOS: (\w+ \w+)\n"
	r"\s\n"
	r"CORREO: ([a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,3}$)\n"
	r"\s\n"
	r"TELEFONO: (\d+)\n"
	r"\s\n"
	r"CLAVE: (\w+)\n"
	r"\s\n"
	r"NOMBRE: (\w+)\n"
	r"\s\n"
	r"APELLIDOS: (\w+ \w+) \n"
	r"\s\n" 
	r"CORREO: ([a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,3}$)\n"
	r"\s\n"
	r"TELEFONO: (\d+)")
    _todos=re.findall(_patron, _texto, re.MULTILINE)
    return _todos   


@app.route('/1carga', methods=['POST','GET'])
def archivo():
    try:
        _eventos=Modelo.selectALLLecturas()
        if request.method == 'POST':
            _a=request.files['Archivo']
            if guardarArchivo(_a):
               print("Si se guardo!")
               _datos=extraerDatos(_a.filename)
               _encontrados=ParseoTexto(_datos)
               Modelo.InsertarLecturas(_encontrados)
        return render_template('1carga.html',eventos=_eventos)
    except Exception as e:
        print(str(e))
        return render_template('1carga.html')

#registro
@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == 'POST':
            _user=request.form['username']
            _email=request.form['email']
            _pass1=request.form['password']
            print (_user)
            consulta=Modelo.register(_user,_email,_pass1) 
            if consulta:
                return ("<h1>Registro éxitoso </1>")
            return ("<h2>Error al ingresar tus datos</h2>")
    return render_template("register.html")
    


#login

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method== "POST":
        _user=request.form["name"]
        _pass=request.form["password"]
        _cambio=Modelo.login(_user,_pass)
        print(_user)
        print(_pass)
        if _cambio:
            return redirect(url_for("home"))
        else:
            flash("Contraseña incorrecta","error")
    return render_template ("login.html")

@app.route("/cuestionario", methods = ["GET","POST"])
def cuestionario():
    if request.method == 'POST':
            _pregunta1=request.form['pregunta1']
            _pregunta2=request.form['pregunta2']
            _pregunta3=request.form['pregunta3']
            _pregunta4=request.form['pregunta4']
            _pregunta5=request.form['pregunta5']
            print(_pregunta1,_pregunta2,_pregunta3,_pregunta4,_pregunta5)
            consul=Modelo.cuestionario(_pregunta1,_pregunta2,_pregunta3,_pregunta4,_pregunta5)
            if consul:
                return ("<h1>Registro éxitoso </1>")
            return ("<h2>Error al ingresar tus datos</h2>")
    return render_template("cuestionario.html")
   



@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/")
def inicio():
    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True)


