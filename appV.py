from flask import Flask 
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os 


app=Flask(__name__)

mysql= MySQL()
app.config ['MYSQL_DATABASE_HOST'] = 'localhost'
app.config ['MYSQL_DATABASE_USER'] = 'root'
app.config ['MYSQL_DATABASE_PASSWORD'] = ''
app.config ['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route ('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

@app.route('/')
def indexV():

    sql = "SELECT *FROM `vehiculos`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    vehiculos=cursor.fetchall()
    print(vehiculos)

    conn.commit()
    return render_template('vehiculos/indexV.html', vehiculos=vehiculos)


@app.route('/destroy/<int:id>') #Eliminar un Vehiculo
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT imagenes FROM vehiculos WHERE id=%s",id)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))

    cursor.execute("DELETE FROM vehiculos WHERE id=%s", (id))
    conn.commit()
    return redirect ('/')

@app.route('/editV/<int:id>')
def edit(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculos WHERE id=%s", (id))
    vehiculos=cursor.fetchall()
    conn.commit()
    return render_template('vehiculo/edit.html', vehiculos=vehiculos)

  

@app.route('/update', methods=['POST']) #Modificar un vehiculos
def update():
    _nombre = request.form['txtNombre']
    _marca = request.form['txtMarca']
    _modelo = request.form['txtModelo']
    _imagenes = request.files['txtImagenes']
    _preciopordia = request.form['txtPreciopordia']
    _capacidadpersonas = request.form['txtCapacidadPersonas']
    _tipocaja = request.form['txtTipoCaja']
    _cantidadpuertas = request.form['txtCantidadPuertas']
    _aireacondicionado = request.form ['txtAireAcondicionado']
    _kilometraje = request.form ['txtkilometraje']
    _capacidadequipaje =request.form ['txtcapacidadequipaje']
    id=request.form['txtID']

    sql ="UPDATE vehiculos SET nombre=%s, marca=%s, modelo=%s, imagenes=%s, preciopordia=%s, _capacidadpersonas=%s, _tipocaja=%s, _cantidadpuertas=%s, _aireacondicionado=%s, _kilometraje=%s, _capacidadequipaje=%s WHERE id=%s ;"

    datos=(_nombre,_marca, _modelo, _imagenes, _preciopordia, _capacidadpersonas, _tipocaja, _cantidadpuertas, _aireacondicionado, _kilometraje, _capacidadequipaje, id)

    conn= mysql.connect()
    cursor=conn.cursor()

    now= datetime.now()                 #Agrega el timpo de subida al nombre, para no Sobre escribir fotos
    tiempo=now.strftime("%Y%H%M%S")

    if _imagenes.filename!= '':

        nuevoNombreFoto=tiempo+_imagenes.filename
        _imagenes.save("uploads/"+nuevoNombreFoto)

        cursor.execute("SELECT imagenes FROM vehiculos WHERE id=%s",id)
        fila=cursor.fetchall()
        
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE vehiculos SET imagenes=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()

    cursor.execute(sql,datos)

    conn.commit()

    return redirect('/')

@app.route('/createV')
def create():
    return render_template('vehiculos/createV.html')

@app.route('/store', methods=['POST'])  # Ingresar un Vehiculo
def storage():
    _nombre = request.form['txtNombre']
    _marca = request.form['txtMarca']
    _modelo = request.form['txtModelo']
    _imagenes = request.files['txtImagenes']
    _preciopordia = request.form['txtPreciopordia']
    _capacidadpersonas = request.form['txtCapacidadPersonas']
    _tipocaja = request.form['txtTipoCaja']
    _cantidadpuertas = request.form['txtCantidadPuertas']
    _aireacondicionado = request.form ['txtAireAcondicionado']
    _kilometraje = request.form ['txtkilometraje']
    _capacidadequipaje =request.form ['txtcapacidadequipaje']

    now= datetime.now()                 #Agrega el timpo de subida al nombre, para no Sobre escribir fotos
    tiempo=now.strftime("%Y%H%M%S")

    if _imagenes.filename!= '':
        nuevoNombreFoto=tiempo+_imagenes.filename
        _imagenes.save("uploads/"+nuevoNombreFoto)

    sql ="INSERT INTO `vehiculos` (`id`, `nombre`, `marca`, `modelo`, `imagenes`,`preciopordia`, `capacidadpersonas`, `tipocaja`, `cantidadpuertas`, `aireacondicionado`, `kilometraje`, `capacidadequipaje` ) VALUES (NULL, %s, %s , %s , %s, %s, %s, %s , %s , %s, %s, %s);"

    datos=(_nombre,_marca, _modelo, _imagenes, _preciopordia, _capacidadpersonas, _tipocaja, _cantidadpuertas, _aireacondicionado, _kilometraje, _capacidadequipaje )

    conn= mysql.connect()
    cursor=conn.cursor()

    cursor.execute(sql,datos)

    conn.commit()

    """return render_template('vehiculo/indexV.html')"""
    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)