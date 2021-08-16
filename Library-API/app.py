import os
from flask import Flask, jsonify
from flask_restful import Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libdb.db'
db = SQLAlchemy(app)
class LibraryModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    version = db.Column(db.String(100),nullable=False)
    link = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(250),nullable=False)

resource_fields = {
    'id' : fields.Integer,
    'name':fields.String,
    'version':fields.String,
    'link':fields.String,
    'description':fields.String
}

@marshal_with(resource_fields)
@app.route('/libs', methods=['GET'])
def get_all():
    return jsonify(get_data_from_db()), 200


@app.route('/lib/<name>', methods=['GET'])
def createcm(name=None):
    final_data_get = get_data_from_db()
    flag = False
    for i in final_data_get:
        if i["Library Name"] != name:
            pass
        else:
            flag = True
            break
    if flag:
        os.system(f"start /B start cmd.exe @cmd /k pip install {name} | exit()")
        return f"{name} INSTALLED SUCCESSFULLY." , 200
    else:
        return "Library Not Found", 404


def get_data_from_db():
    result = LibraryModel.query.order_by(LibraryModel.id).all()
    ids = []
    names = []
    versions = []
    links = []
    descs = []
    for i in range(len(result)):
        ids.append(result[i].id)
        names.append(result[i].name)
        versions.append(result[i].version)
        links.append(result[i].link)
        descs.append(result[i].description)
    final_data = [{'Id':id, 'Library Name': name, 'Library Version': ver, 'Library Link': link, "Library Description": desc} for id, name, ver, link, desc in zip(ids,names, versions, links,descs)]
    return final_data

if __name__ == "__main__":
    app.run(debug=True)
