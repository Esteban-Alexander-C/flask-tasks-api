import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Para que no haya errores con la creacion de la BD lo ponemos primero
db = SQLAlchemy()

#Despues de crearlo lo importamos
from .routes import register_routes #Le decimos a Flask que las rutas estan en otro archivo

def create_app(): #Creamos una función 
    app = Flask(__name__, instance_relative_config=True)

    #Creamos carpeta instance si no existe
    os.makedirs(app.instance_path, exist_ok=True)

    #Ruta absoluta(CLAVE)
    db_path = os.path.join(app.instance_path, "tasks.db")

    #Configuración de base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"  + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    register_routes(app)
    
    return app #Devolvemos la aplicacion app que hemos creado arriba

