from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Create App
app = Flask(__name__)
api = Api(app)
# DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
class VideoModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    views = db.Column(db.Integer,nullable=False)
    likes = db.Column(db.Integer,nullable=False)
    def __repr__(self) -> str:
        return f"Video => [Name: {self.name} | Views: {self.views} | Likes: {self.likes}]"
db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Please add video's name!",required=True)
video_put_args.add_argument("likes",type=int,help="Please add video's likes!",required=True)
video_put_args.add_argument("views",type=int,help="Please add video's views!",required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name",type=str)
video_update_args.add_argument("likes",type=int)
video_update_args.add_argument("views",type=int)


resource_fields = {
    'id' : fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}

class Video(Resource):

    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="Video is not found!")
        return result

    @marshal_with(resource_fields)    
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message="Video already exists!")
        video = VideoModel(id=video_id, name = args['name'], views = args['views'], likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self,video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not request:
            abort(404,message="Video is not found!")
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result

    def delete(self,video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="Video is not found!")
        db.session.delete(result)
        db.session.commit()
        return '', 204


# Register Resource        
api.add_resource(Video,"/v/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
