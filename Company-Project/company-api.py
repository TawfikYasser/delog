from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companiesdb.db'
db = SQLAlchemy(app)
class CompanyModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    location = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(250),nullable=False)
    def __repr__(self) -> str:
        return f"Company Data: {self.id} - {self.name} - {self.location}  - {self.description}"

resource_fields = {
    'id' : fields.Integer,
    'name':fields.String,
    'location':fields.String,
    'description':fields.String
}

class Company(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = CompanyModel.query.order_by(CompanyModel.id).all()
        return result


# Register Resource        
api.add_resource(Company,"/c/")

if __name__ == "__main__":
    app.run(debug=True)
