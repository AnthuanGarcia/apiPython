import db_config as db
from app import create_app
from bson.json_util import dumps
from flask_pymongo import pymongo
from flask import jsonify, request

app = create_app()
auth = db.AUTH

@app.route("/<string:identity>/api/showConsoles/")
def showConsoles(identity):
    if identity == auth:
        consoles = dumps(list(db.db.before2005.find()))
        return consoles
    else:
        return jsonify({
            "error" : "Autorizacion invalida, ingresa el string de identidad"
        })

@app.route("/<string:identity>/api/console/<string:name>/")
def showConsole(name, identity):

    if identity == auth:

        console = dumps(db.db.before2005.find_one({"name" : name}))
        if console == "null":
            return jsonify({
                "error" : 400,
                "message" : "Consola no encontrada :("
            })
        else:
            return console

    else:
        return jsonify({
            "error" : "Autorizacion invalida, ingresa el string de identidad"
        })


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