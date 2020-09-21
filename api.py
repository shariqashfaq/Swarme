import os
from flask import Flask, jsonify, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return jsonify({"welcome message": "this is the api"})

"""Users"""

#Create user
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    
    new_user = User(first_name=data["first_name"], last_name=data["last_name"], user_name=data["user_name"], email=data["email"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"Message": "Success"})

#Create workspace
@app.route("/workspace", methods=["POST"])
def create_workspace():
    data = request.get_json()

    new_workspace = Workspace(name=data["name"])
    db.session.add(new_workspace)
    db.session.commit()
    
    return jsonify({"Message": "Successfully created workspace"})

#Add worker to workspace
@app.route("/workspace/addworker", methods=["PUT"])
def add_worker():
    data = request.get_json()

    #get workspace and user info
    workspace_id = data["workspace_id"]
    user_id = data["user_id"]

    workspace = Workspace.query.get(workspace_id)
    user = User.query.get(user_id)

    #append users to workers list
    workspace.workers.append(user)
    db.session.commit()

    return jsonify({"Message": "User successfully added to workspace"})

#get all workers in a workspace
@app.route("/workspace/workers", methods=["GET"])
def get_workers():
    data = request.get_json()

    #get workspace info
    workspace_id = data["workspace_id"]
    workspace = Workspace.query.get(workspace_id)
    worker_dict = {"Workers": []}
    for names in workspace.workers:
        worker_dict["Workers"].append(names.first_name) 
    
    return jsonify(worker_dict)

if __name__=="__main__":
    app.run(debug=True)

