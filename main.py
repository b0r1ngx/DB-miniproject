# Local
from functools import wraps

from database.db_session import init_database_session
from database import dbi

# stdlib
import base64

# lib
from flask import Flask, request, make_response
from werkzeug.datastructures import FileStorage
from flask_restx.reqparse import RequestParser
from flask_restx import Api, fields, Resource
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "secretKey"

CORS(app)
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
int_list_model = api.model("int_list", {
    "list": fields.List(fields.Integer)
})
theme_model = api.model("theme", {
    "id": fields.Integer,
    "name": fields.String
})
theme_list_model = api.model("theme_list", {
    "list": fields.List(fields.Nested(theme_model))
})
tag_model = api.model("tag", {
    "id": fields.Integer,
    "name": fields.String
})
tag_list_model = api.model("tag_list", {
    "list": fields.List(fields.Nested(tag_model))
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
    "tag_list": fields.List(fields.Integer),
    "theme_list": fields.List(fields.Integer),
    "album_list": fields.List(fields.Integer),
    "comment_list": fields.List(fields.Nested(comment_model))
})

user_api = api.namespace('api', description='API for user')
admin_api = api.namespace('admin_api', description='API for admin')


def check_auth():
    auth = request.authorization
    if not auth or not dbi.login(auth.username, auth.password):
        return False
    return True


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not dbi.login(auth.username, auth.password):
            return make_response({}, )
        return f(*args, **kwargs)

    return decorated


@user_api.route("/login")
@admin_api.route("/login")
class Login(Resource):
    @staticmethod
    @user_api.doc(description="Тут логиниться")
    @user_api.doc(sum="qwerty")
    @user_api.expect(RequestParser()
                     .add_argument(name="email", type=str, location="form", required=True)
                     .add_argument(name="password", type=str, location="form", required=True)
                     )
    @user_api.response(200, "Success", token64_model)  # add token model
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(403, "Wrong email or password", message_model)
    def post():
        f = request.form
        if not ("email" in f and "password" in f):
            return make_response({"message": "Invalid request"}, 400)
        email = f["email"]
        password = f["password"]

        is_correct = dbi.login(email, password)

        if not is_correct:
            return make_response({"message": "Wrong email or password"}, 403)

        token64 = base64.b64encode(f"{email}:{password}".encode('ascii')).decode('ascii')
        return make_response({"token": token64}, 200)


@user_api.route("/registration")
class Registration(Resource):
    @staticmethod
    @user_api.response(200, "Success", token64_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(401, "This email is already taken", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="email", type=str, location="form", required=True)
                     .add_argument(name="password", type=str, location="form", required=True)
                     .add_argument(name="full_name", type=str, location="form", required=True)
                     )
    def post():
        f = request.form
        if not ("email" in f and "password" in f and "full_name" in f):
            return make_response({"message": "Invalid request"}, 400)
        email = f["email"]
        password = f["password"]
        full_name = f["full_name"]

        is_Correct = True  # TODO(Если такой email уже зарегистрирован False, иначе True)
        if not is_Correct:
            return make_response({"message": "This email is already taken"}, 403)
        # TODO(Магия записи в БД) def registration(email, password, full_name)
        token64 = base64.b64encode(f"{email}:{password}".encode('ascii')).decode('ascii')
        return make_response({"token": token64}, 200)


@user_api.route("/user/<int:user_id>")
@admin_api.route("/user/<int:user_id>")
class User(Resource):
    @staticmethod
    @user_api.response(200, "Success", user_model)
    @user_api.response(404, "Not found user with this ID", message_model)
    def get(user_id):
        is_user_exist = True  # TODO(существует ли пользователь с id) def check_user_exist(id)
        if not is_user_exist:
            make_response({"message": "Not found user with this ID"}, 403)

        is_auth = False
        user = {
            "id": 1,
            "name": fields.String,
            "full_name": fields.String,
            "email": fields.String,
            "date": fields.DateTime,
            "photos": fields.List(fields.Nested(photo_preview_model))
        }
        pass

    @staticmethod
    @user_api.doc(doc=False)
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot delete users", message_model)
    @user_api.response(404, "Not found user with this ID", message_model)
    def delete(user_id):
        print(1)
        print(request.authorization)
        print(2)
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
    @api.doc(security='basicAuth')
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
    @api.doc(security='basicAuth')
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
                     .add_argument(name="tag_id", type=int, location="form")  # Поиск по множеству тегов/тем??
                     .add_argument(name="created_at", type=str, location="form")
                     .add_argument(name="amount", type=int, location="form")
                     .add_argument(name="page", type=int, location="form")
                     )
    def get():
        pass


@user_api.route("/photo")
class Photo(Resource):
    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", photo_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="file", type=FileStorage, location="files")
                     .add_argument(name="description", type=str, location="form")
                     .add_argument(name="albums", type=int, location="form", action="append")
                     .add_argument(name="tags", type=int, location="form", action="append")
                     .add_argument(name="themes", type=int, location="form", action="append")
                     .add_argument(name="private or no", type=bool, location="form")
                     )
    def post():
        request.files.get("file").save()
        print(type(request.files.get("file")))
        pass
        return "123"


@user_api.route("/photo/<int:photo_id>")
class PhotoID(Resource):
    @staticmethod
    @user_api.response(200, "Success", photo_model)
    def get(photo_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", photo_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot update this photo", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="description", type=str, location="form")
                     .add_argument(name="albums", type=int, location="form", action="append")
                     .add_argument(name="tags", type=int, location="form", action="append")
                     .add_argument(name="themes", type=int, location="form", action="append")
                     .add_argument(name="private or no", type=bool, location="form")
                     )
    def put(photo_id):
        f = request.form
        albums = f.getlist()
        print(123)
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot delete this photo", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    def delete(photo_id):
        pass


@user_api.route("/photo/<int:photo_id>/accessList")
class AccessList(Resource):
    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", int_list_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot get this list", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    def get(photo_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", int_list_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot create this list", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="user_ids", type=int, location="form", action="append", required=True)
                     )
    def post(photo_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", int_list_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot update this list", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="user_ids", type=int, location="form", action="append", required=True)
                     )
    def put(photo_id):
        pass


@user_api.route("/photo/<int:photo_id>/accessList/<int:user_id>")
class AccessListID(Resource):
    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot change this", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    def delete(photo_id, user_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot change this", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    def put(photo_id, user_id):
        pass


@user_api.route("/photo/<int:photo_id>/comment")
class Comment(Resource):
    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", comment_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You do not have access to this photo", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="text", type=str, location="form", required=True)
                     )
    def post(photo_id):
        pass


@user_api.route("/photo/<int:photo_id>/comment/<int:comment_id>")
class CommentID(Resource):
    @staticmethod
    @user_api.expect(RequestParser()
                     .add_argument(name="text", type=str, location="form", required=True)
                     )
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", comment_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You do not have access to this comment", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    @user_api.response(404, "Not found comment with this ID", message_model)
    def put(photo_id, comment_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", comment_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You do not have access to this comment", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    @user_api.response(404, "Not found comment with this ID", message_model)
    def delete(photo_id, comment_id):
        pass


@user_api.route("/theme")
@admin_api.route("/theme")
class Theme(Resource):
    @staticmethod
    @user_api.response(200, "Success", theme_list_model)
    def get():
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.doc(doc=False)
    @user_api.response(200, "Success", theme_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot create theme", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form", required=True)
                     )
    def post():
        pass


@user_api.route("/theme/<int:theme_id>")
@admin_api.route("/theme/<int:theme_id>")
class ThemeID(Resource):
    @staticmethod
    @user_api.response(200, "Success", photo_list_model)
    def get(theme_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.doc(doc=False)
    @user_api.response(200, "Success", theme_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot create theme", message_model)
    @user_api.response(404, "Not found comment theme this ID", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form", required=True)
                     )
    def put(theme_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.doc(doc=False)
    @user_api.response(200, "Success", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot delete this theme", message_model)
    @user_api.response(404, "Not found comment theme this ID", message_model)
    def delete(theme_id):
        pass


@user_api.route("/tag")
class Tag(Resource):
    @staticmethod
    @user_api.response(200, "Success", tag_list_model)
    def get():
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", tag_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot create tag", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form", required=True)
                     )
    def post():
        pass


@user_api.route("/tag/<int:tag_id>")
class TageID(Resource):
    @staticmethod
    @user_api.response(200, "Success", photo_list_model)
    def get(tag_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", tag_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot create theme", message_model)
    @user_api.response(404, "Not found comment tag this ID", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form", required=True)
                     )
    def put(tag_id):
        pass

    @staticmethod
    @api.doc(security='basicAuth')
    @user_api.response(200, "Success", message_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot delete this theme", message_model)
    @user_api.response(404, "Not found comment tag this ID", message_model)
    def delete(tag_id):
        pass


if __name__ == "__main__":
    # logging.basicConfig(filename="Converter.log", level=logging.DEBUG,
    #                     format="[%(asctime)s] %(levelname)s - %(message)s")
    # print(type(message_model))
    init_database_session()
    app.run(host="localhost", port=5002)
