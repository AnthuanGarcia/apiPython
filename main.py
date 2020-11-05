import db_config as db
from random import randint
from app import create_app
from bson.json_util import dumps
from flask_pymongo import pymongo
from flask import jsonify, request, render_template, redirect

app = create_app()
auth = db.AUTH

@app.route("/")
def index():
    consoles = list(db.db.before2005.find())
    colors = [randint(1, 10) for x in range(len(consoles))]

    return render_template('index.html', consolas = consoles, lon = len(consoles), color = colors)

@app.route("/home")
def home():
    return render_template("home.html")

# Captura de datos de formulario
@app.route("/auth", methods = ['POST'])
def verificar():
    
    identify = request.form.get("auth")
    if identify == auth:
        return redirect(f"{identify}/panel")
    else:
        return "<h1>Auth string incorrecto</h1>"

@app.route(f"/{auth}/panel")
def panel():
    return render_template("panel.html")

@app.route("/api/showConsoles/")
def showConsoles():
    consoles = dumps(list(db.db.before2005.find()))
    return consoles

@app.route("/api/console/<string:name>/")
def showConsole(name):
    console = dumps(db.db.before2005.find_one({"name" : name}))
    if console == "null":
        return jsonify({
            "error" : 400,
            "message" : "Consola no encontrada :("
        })
    else:
        return console

@app.route("/<string:identity>/api/newConsole/", methods = ["POST"])
def addConsole(identity):

    if identity == auth:

        if len(request.json) == 4:
            db.db.before2005.insert_one({
                "name" : request.json["name"],
                "company" : request.json["company"],
                "age" : request.json["age"],
                "img" : request.json["img"]
            })
        else:
            return jsonify({
                "error" : "¡Faltan datos!",
            })

        return jsonify({
            "status" : 200,
            "message" : f"La consola {request.json['name']} ha sido añadida"
        })

    else:
        return jsonify({
            "error" : "Autorizacion invalida, ingresa el string de identidad"
        })

@app.route("/<string:identity>/api/console/update/<string:name>/", methods = ["PUT"])
def updateConsole(name, identity):
    if identity == auth:

        if db.db.before2005.find_one({"name" : name}):
            db.db.before2005.update_one({"name" : name},
            {"$set" : {
                "name" : request.json["name"],
                "company" : request.json["company"],
                "age" : request.json["age"],
                "img" : request.json["img"]
            }})
        else:
            return jsonify({
                "error" : 400,
                "message" : f"La Consola {name} no ha sido encontrada :(",
            })

        return jsonify({
            "status" : 200,
            "message" : f"La consola {name} ha sido actualizada"
        })
    else:
        return jsonify({
            "error" : "Autorizacion invalida, ingresa el string de identidad"
        })

@app.route("/<string:identity>/api/console/delete/<string:name>/", methods = ["DELETE"])
def deleteConsole(name, identity):
    if identity == auth:

        if db.db.before2005.find_one({"name" : name}):
            db.db.before2005.delete_one({"name" : name})
        else:
            return jsonify({
                "error" : 400,
                "message" : f"La Consola {name} no ha sido encontrada :(",
            })

        return jsonify({
            "status" : 200,
            "message" : f"La consola {name} ha sido eliminada"
        })
        
    else:
        return jsonify({
            "error" : "Autorizacion invalida, ingresa el string de identidad"
        })

if __name__ == "__main__":
    app.run(load_dotenv=True, port=3030)