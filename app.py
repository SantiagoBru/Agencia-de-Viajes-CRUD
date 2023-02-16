from flask import Flask 
from flask import render_template,request,redirect
from flaskext.mysql import MySQL


app=Flask(__name__)

mysql= MySQL()
app.config ['MYSQL_DATABASE_HOST'] = 'localhost'
app.config ['MYSQL_DATABASE_USER'] = 'root'
app.config ['MYSQL_DATABASE_PASSWORD'] = ''
app.config ['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

@app.route('/')
def index():

    sql = "SELECT *FROM `usuarios`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    usuarios=cursor.fetchall()
    print(usuarios)

    conn.commit()
    return render_template('usuarios/index.html', usuarios=usuarios)

@app.route('/destroy/<int:id>') #Eliminar un Usuario
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id))
    conn.commit()
    return redirect ('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id))
    usuarios=cursor.fetchall()
    conn.commit()
    return render_template('usuarios/edit.html', usuarios=usuarios)
    
@app.route('/update', methods=['POST']) #Modificar un usuario
def update():
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _correo = request.form['txtCorreo']
    _rol = request.form['txtRol']
    id=request.form['txtID']

    sql ="UPDATE usuarios SET nombre=%s, apellido=%s, correo=%s, rol=%s WHERE id=%s ;"

    datos=(_nombre,_apellido,_correo,_rol,id)

    conn= mysql.connect()
    cursor=conn.cursor()

    cursor.execute(sql,datos)

    conn.commit()

    return redirect('/')

@app.route('/create')
def create():
    return render_template('usuarios/create.html')

@app.route('/store', methods=['POST'])  # Ingresar un usuario
def storage():
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _correo = request.form['txtCorreo']
    _rol = request.form['txtRol']


    sql ="INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `correo`, `rol`) VALUES (NULL, %s, %s , %s , %s );"

    datos=(_nombre,_apellido,_correo,_rol)

    conn= mysql.connect()
    cursor=conn.cursor()

    cursor.execute(sql,datos)

    conn.commit()

    """return render_template('usuarios/index.html')"""
    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)


