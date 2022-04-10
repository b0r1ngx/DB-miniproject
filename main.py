from flask import Flask, request, make_response
from flask_restx import Api, fields, Resource
from flask_restx.reqparse import RequestParser
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from constants import db

app = Flask(__name__)
app.secret_key = "secretKey"


# app.config['SQLALCHEMY_DATABASE_URI'] = db
#
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


authorizations = {
    'basicAuth': {
        'type': 'basic'
    }
}

api = Api(
    app,
    authorizations=authorizations,
    version="0.1",
    title="Photo Service API",
    default="Photo Service",
    doc="/doc"
)

message_model = api.model("message", {
    "message": fields.String
})
token64_model = api.model("token64", {
    "token": fields.String
})
user_info_model = api.model("user_ifo", {
    "id": fields.Integer,
    "name": fields.String
})
photo_preview_model = api.model("preview", {
    "id": fields.Integer,
    "url": fields.Url
})
user_model = api.model("user", {
    "id": fields.Integer,
    "name": fields.String,
    "full_name": fields.String,
    "email": fields.String,
    "date": fields.DateTime,
    "photos": fields.List(fields.Nested(photo_preview_model))
})
album_model = api.model("album", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "date": fields.DateTime,
    "photos": fields.List(fields.Nested(photo_preview_model))
})
album_list_model = api.model("album_list", {
    "list": fields.List(fields.Nested(album_model))
})
photo_list_model = api.model("photo_list", {
    "list": fields.List(fields.Nested(photo_preview_model))
})


comment_model = api.model("comment", {
    "id": fields.Integer,
    "user": fields.Nested(user_info_model),
    "photo_id": fields.Integer,
    "text": fields.String
})

photo_model = api.model("photo", {
    "id": fields.Integer,
    "url": fields.Url,
    "user": fields.Nested(user_info_model),
    "teg_list": fields.List(fields.Integer),
    "theme_list": fields.List(fields.Integer),
    "album_list": fields.List(fields.Integer),
    "comment_list": fields.List(fields.Nested(comment_model))
})

user_api = api.namespace('api', description='API for user')
admin_api = api.namespace('admin_api', description='API for admin')


@user_api.route("/login")
@admin_api.route("/login")
class Login(Resource):
    @staticmethod
    @user_api.expect(RequestParser()
                     .add_argument(name="username", type=str, location="form", required=True)
                     .add_argument(name="password", type=str, location="form", required=True)
                     )
    @user_api.response(200, "Success", token64_model)  # add token model
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(403, "Wrong username or password", message_model)
    def post():
        pass


@user_api.route("/registration")
class Registration(Resource):
    @staticmethod
    @user_api.response(200, "Success", token64_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(401, "This username is already taken", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="username", type=str, location="form", required=True)
                     .add_argument(name="password", type=str, location="form", required=True)
                     .add_argument(name="full_name", type=str, location="form", required=True)
                     )
    def post():
        pass


@user_api.route("/user/<int:user_id>")
@admin_api.route("/user/<int:user_id>")
class User(Resource):
    @staticmethod
    @user_api.response(200, "Success", user_model)
    @user_api.response(404, "Not found user with this ID", message_model)
    def get(user_id):
        pass

    @staticmethod
    @user_api.doc(doc=False)
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot delete users", message_model)
    @user_api.response(404, "Not found user with this ID", message_model)
    def delete(user_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.expect(RequestParser()
                     .add_argument(name="full_name", type=str, location="form", required=True)
                     )
    @user_api.response(200, "Success", user_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot update this users", message_model)
    @user_api.response(404, "No user found with this id", message_model)
    def put(user_id):
        pass


@user_api.route("/user/<int:user_id>/album")
class UserAlbum(Resource):
    @staticmethod
    @user_api.response(200, "Success", album_list_model)
    @user_api.response(404, "Album with this id not found", message_model)
    def get(user_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form", required=True)
                     .add_argument(name="description", type=str, location="form")
                     )
    @user_api.response(200, "Success", album_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot create album for this user", message_model)
    @user_api.response(404, "No user found with this id", message_model)
    def post():
        pass


@user_api.route("/user/<int:user_id>/album/<int:album_id>")
@admin_api.route("/user/<int:user_id>/album/<int:album_id>")
class UserAlbumID(Resource):
    @staticmethod
    @user_api.response(200, "Success", album_model)
    @user_api.response(404, "Not found", message_model)
    def get(user_id, album_id):
        pass

    @staticmethod
    @user_api.response(200, "Success", album_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot update this album", message_model)
    @user_api.response(404, "Not found", message_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form", required=True)
                     .add_argument(name="description", type=str, location="form")
                     )
    def put(user_id, album_id):
        pass

    @staticmethod
    @user_api.response(200, "Success", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot delete this album", message_model)
    @user_api.response(404, "Not found", message_model)
    def delete(user_id, album_id):
        pass


@user_api.route("/search")
class Search(Resource):
    @staticmethod
    @user_api.response(200, "Success", photo_list_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="theme_id", type=int, location="form", required=True)
                     .add_argument(name="tag_id", type=int, location="form")
                     .add_argument(name="created_at", type=str, location="form")
                     .add_argument(name="amount", type=int, location="form")
                     .add_argument(name="page", type=int, location="form")
                     )
    def get():
        pass


@user_api.route("/photo")
class Photo(Resource):
    @staticmethod
    @user_api.expect(RequestParser()
                     .add_argument(name="file", type=str, location="form")#File???
                     # TODOha
                     )
    def post():
        pass


@user_api.route("/photo/<int:photo_id>")
class PhotoID(Resource):
    pass


@user_api.route("/photo/<int:photo_id>/accessList")
class AccessList(Resource):
    pass


@user_api.route("/photo/<int:photo_id>/accessList/<int:user_id>")
class AccessListID(Resource):
    pass


@user_api.route("/photo/<int:photo_id>/comment")
class Comment(Resource):
    pass


@user_api.route("/photo/<int:photo_id>/comment/<int:comment_id>")
class CommentID(Resource):
    pass


@user_api.route("/theme")
class Theme(Resource):
    pass


@user_api.route("/theme/<int:theme_id>")
class ThemeID(Resource):
    pass


@user_api.route("/tag")
class Tag(Resource):
    pass


@user_api.route("/tag/<int:tag_id>")
class TageID(Resource):
    pass


# @user_api.route("/user/<int:user_id>")
# class Temp(Resource):
#     @staticmethod
#     def get(user_id):
#         return f'{user_id}'


# @api.route("/registration")
# class UserRegistration(Resource):
#     @staticmethod
#     @api.response(200, "Success")  # add token model
#     @api.response(400, "Invalid request", message_model)
#     @api.response(401, "This username is already taken", message_model)
#     @api.expect(RequestParser()
#                 .add_argument(name="username", type=str, location="form")
#                 .add_argument(name="password", type=str, location="form")
#                 )
#     @api.doc("asd")
#     def post():
#         f = request.form
#         if not ("username" in f and "password" in f):
#             return make_response({"message": "Invalid request"}, 400)
#
#         username = f["username"]
#         password = f["password"]
#         pass
#         return f'hello'
#
#     @staticmethod
#     @api.doc(security='basicAuth')
#     def get():
#         return "protected"
#
#
# @np.route("/search")
# class Search(Resource):
#     @staticmethod
#     @np.expect(RequestParser()
#                .add_argument(name="user_id", type=int, location="args")
#                .add_argument(name="album_id", type=int, location="args")
#                .add_argument(name="theme_id", type=int, location="args")
#                .add_argument(name="tag_id", type=int, location="args")
#                .add_argument(name="page", type=int, location="args")
#                .add_argument(name="amount", type=int, location="args")
#                )
#     def get():
#         args = request.args
#         DEFAULT_AMOUNT = 10
#         DEFAULT_PAGE = 1
#
#         amount = int(args["amount"]) if "amount" in args else DEFAULT_AMOUNT
#         page = int(args["page"]) if "page" in args else DEFAULT_PAGE
#         pass
#         return f'page:{page} amount:{amount}'


if __name__ == "__main__":
    # logging.basicConfig(filename="Converter.log", level=logging.DEBUG,
    #                     format="[%(asctime)s] %(levelname)s - %(message)s")
    # print(type(message_model))
    app.run(host="localhost", port=5002)
