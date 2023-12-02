# Importación de módulos necesarios
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
import datetime

#Creacion de APP Flask
app = Flask(__name__)
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/test'
#engine = create_engine('mysql+pymysql://root@localhost:3306/conferencia')
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/conferencia'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

#Definimo el modelo de datos
class Orador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido= db.Column(db.String(100))
    email= db.Column(db.String(30))
    tema= db.Column(db.String(200))
    fecha_alta= db.Column(db.Date)
    
    def __init__(self,nombre,apellido,email,tema,fecha_alta):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.tema = tema
        self.fecha_alta = fecha_alta

#Definimos el esquema
class OradorSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','apellido','email','tema','fecha_alta')


#Crear esquemas para la db
orador_schema = OradorSchema() #trae un orador
oradores_schema = OradorSchema(many=True) #Para traer más de un orador

#Creamos la tablas
with app.app_context():
    db.create_all() 

#Endpoint Get
@app.route('/oradores', methods=['GET'])
def get_all_oradores():
    try:
        oradores = Orador.query.all()
        if oradores:
            return oradores_schema.jsonify(oradores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Endpoint Get by Id
@app.route('/oradores/<id>', methods=['GET'])
def get_empleado(id):
    try:
        orador = Orador.query.get(id)

        if orador:
            return orador_schema.jsonify(orador)
        else:
            return jsonify({'error': 'Orador no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo orador mediante una solicitud POST
@app.route('/oradores', methods=['POST'])
def create_orador():
    try:
        json_data = request.get_json()
        nombre = json_data['nombre']
        apellido = json_data['apellido']
        email = json_data['email']
        tema = json_data['tema']
        fecha_alta = datetime.datetime.strptime(json_data['fecha_alta'], "%Y-%m-%d").date()

        # Cargar datos JSON en un objeto Orador
        nuevo_orador = Orador(nombre, apellido, email, tema, fecha_alta)

        # Realizar validaciones adicionales si es necesario

        db.session.add(nuevo_orador)
        db.session.commit()

        return orador_schema.jsonify(nuevo_orador), 201  # Devolver el orador creado con el código 201 (creado)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400  # Devolver mensajes de error de validación con el código 400 (error de solicitud)

# Ruta para actualizar un orador mediante una solicitud PUT
@app.route('/oradores/<id>', methods=['PUT'])
def update_orador(id):
    try:
        orador = Orador.query.get(id)

        # Verificar si el orador existe en la base de datos
        if orador:
            json_data = request.get_json()
            orador.nombre = json_data.get('nombre', orador.nombre)
            orador.apellido = json_data.get('apellido', orador.apellido)
            orador.email = json_data.get('email', orador.email)
            orador.tema = json_data.get('tema', orador.tema)
            orador.fecha_alta = datetime.datetime.strptime(json_data['fecha_alta'], "%Y-%m-%d").date()

            # Realizar validaciones según tus requerimientos

            db.session.commit()
            return orador_schema.jsonify(orador)
        else:
            return jsonify({'error': 'orador no encontrado'}), 404  # Devolver código 404 si el orador no existe

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400  # Devolver mensajes de error de validación con el código 400 (error de solicitud)

# Ruta para eliminar un orador mediante una solicitud DELETE
@app.route('/oradores/<id>', methods=['DELETE'])
def delete_orador(id):
    try:
        orador = Orador.query.get(id)

        # Verificar si el empleado existe en la base de datos
        if orador:
            db.session.delete(orador)
            db.session.commit()
            return orador_schema.jsonify(orador)
        else:
            return jsonify({'error': 'Orador no encontrado'}), 404  # Devolver código 404 si el orador no existe

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Devolver código 500 si hay un error durante la eliminación


if __name__ == '__main__':
    app.run(debug=True)

