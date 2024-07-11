from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------------------------------------------------------------------------------
#get -> consultar - 15 puntos
@app.route('/productos', methods=['GET'])
def ver_productos():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='comercio'
    )

    cursor = db.cursor(dictionary=True) #en lugar de tener una lista con tuplas, tener un diccionario con clave(campo) y valor(dato)
    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    cursor.close()
    return jsonify(productos) #generamos un json como respuesta
# -------------------------------------------------------------------------------

#delete -> eliminar un producto
@app.route('/eliminar_productos/<int:id>', methods=['DELETE'])
def eliminar_productos(id):
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='comercio'
    )

    cursor = db.cursor() 
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))

    db.commit()
    cursor.close()
    return jsonify("Registro eliminado con exito!!") #generamos un json como respuesta
# -------------------------------------------------------------------------------

#post -> crear un nuevo elemento en el servidor
@app.route('/agregar_producto', methods=['POST'])
def crear_producto():
    info = request.json
    '''
    info = { "n": "monitor", "c": 45 , "p":100500}
    '''
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='comercio'
    )

    cursor = db.cursor() 
    cursor.execute("INSERT INTO productos(nombre,cantidad,precio) VALUES(%s,%s,%s)", (info["nombre"],info["cantidad"],info["precio"]))
    
    db.commit()
    cursor.close()
    return jsonify({"mensaje: REGISTRO CREADO CON EXITO!!!"}) 
# -------------------------------------------------------------------------------

#put -> actualizar/modificar
@app.route('/actualizar_producto/<int:id>', methods=['PUT'])
def modificar_producto(id):
    info = request.json
    '''
    info = { "nombre": "monitor", "cantidad": 45 , "precio":100500}
    '''
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='comercio'
    )

    cursor = db.cursor() 
    cursor.execute("UPDATE productos SET nombre= %s, cantidad= %s, precio= %s WHERE id = %s", (info["nombre"],info["cantidad"],info["precio"]))
   
    db.commit()
    cursor.close()
    return jsonify({"mensaje: REGISTRO ACTUALIZADO CON EXITO!!!"}) 

# -------------------------------------------------------------------------------

#desde donde se ejecuta nuestro proyecto
if __name__ == '__main__':
    app.run(debug=True) 