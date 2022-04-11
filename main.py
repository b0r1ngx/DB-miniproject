# Local
import os
from functools import wraps

from werkzeug.utils import secure_filename

from database.db_session import init_database_session
from database import dbi

# stdlib
import base64

# lib
from flask import Flask, request, make_response, url_for
from werkzeug.datastructures import FileStorage
from flask_restx.reqparse import RequestParser
from flask_restx import Api, fields, Resource
from flask_cors import CORS
from flask import send_from_directory
from helpers import email_is_valid

app = Flask(__name__)
app.secret_key = "secretKey"

UPLOAD_FOLDER = './uploadsPhoto'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

api = Api(
    app,
    authorizations={
        'basicAuth': {
            'type': 'basic'
        }
    },
    version="0.1",
    title="Photo Service API",
    default="Photo Service",
    doc="/doc",
    security='basicAuth'
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


def requires_auth(f):
    @user_api.response(401, "You must be logged in", message_model)
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not dbi.login(auth.username, auth.password):
            return make_response({"message": "You must be logged in"}, 401)
        return f(*args, **kwargs)

    return decorated


def check_user_exist(user_id):
    # TODO check check_user_exist
    if not dbi.is_user_exist(user_id):
        return make_response({"message": "Not found user with this ID"}, 404)


def check_album_exist(user_id, album_id):
    # TODO check check_user_exist
    if not dbi.is_album_exist(user_id, album_id):
        return make_response({"message": "Not found album with this ID"}, 404)


def check_photo_exist(photo_id):
    if not dbi.is_photo_exist(photo_id):  # TODO check check_photo_exist
        return make_response({"message": "Not found photo with this ID"}, 404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@user_api.route("/login")
@admin_api.route("/login")
class Login(Resource):
    @staticmethod
    @user_api.doc(description="Залогиниться", security=False)
    # @user_api.doc(summary="qwerty")
    # @user_api.
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

        new_user_id = dbi.login(email, password)

        if not new_user_id:
            return make_response({"message": "Wrong email or password"}, 403)

        token64 = base64.b64encode(f"{email}:{password}".encode('ascii')).decode('ascii')
        return make_response({"token": token64}, 200)


@user_api.route("/registration")
class Registration(Resource):
    @staticmethod
    @user_api.doc(description="Зарегистрироваться", security=False)
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

        user_id = dbi.get_user_id(email)
        if user_id:
            return make_response({"message": "This email is already taken"}, 403)

        dbi.registration(full_name, email, password)
        token64 = base64.b64encode(f"{email}:{password}".encode('ascii')).decode('ascii')
        return make_response({"token": token64}, 200)


@user_api.route("/user/<int:user_id>")
@user_api.response(404, "Not found user with this ID", message_model)
class User(Resource):
    @staticmethod
    @user_api.doc(description="Получить информацию о пользователе")
    @user_api.response(200, "Success", user_model)
    def get(user_id):
        check_user_exist(user_id)

        auth = request.authorization
        viewer_id = 0 if not auth else dbi.get_user_id(request.authorization.username)

        user = dbi.do_user_have_access_to_other_user_photos(user_id, viewer_id)
        # TODO do_user_have_access_to_other_user_photos check

        #     {
        #     "id": 1,
        #     "full_name": fields.String,
        #     "email": fields.String,
        #     "date": fields.DateTime,
        #     "photos": fields.List(fields.Nested(photo_preview_model))  #
        # }
        # TODO Преобразовать user к dict правильной формы
        return make_response(user, 200)

    @staticmethod
    @user_api.doc(description="Удалить пользователя")
    @requires_auth
    @user_api.response(200, "Success", message_model)
    @user_api.response(403, "You cannot delete users", message_model)
    def delete(user_id):
        check_user_exist(user_id)

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)  # TODO check is_admin

        if viewer_id == user_id or viewer_is_admin:
            dbi.delete_user(user_id)  # TODO check delete_user
            return make_response({"message": "Success"}, 200)

        return make_response({"message": "You cannot delete users"}, 403)

    @staticmethod
    @user_api.doc(description="Перезаписать информацию о пользователе")
    @requires_auth
    @user_api.expect(RequestParser()
                     .add_argument(name="full_name", type=str, location="form")
                     .add_argument(name="email", type=str, location="form")
                     .add_argument(name="password", type=str, location="form")
                     )
    @user_api.response(200, "Success", message_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(403, "You cannot update this users", message_model)
    def put(user_id):
        check_user_exist(user_id)

        f = request.form
        if not ("full_name" in f or "email" in f or "password" in f):
            return make_response({"message": "Invalid request"}, 400)

        new_full_name = None if "full_name" not in f else f["full_name"]
        new_email = None if "email" not in f else f["email"]
        new_password = None if "password" not in f else f["password"]

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)  # TODO check is_admin

        if viewer_id == user_id or viewer_is_admin:
            dbi.change_user(user_id,
                            full_name=new_full_name,
                            password=new_password,
                            email=new_email
                            )  # TODO check change_user
            return make_response({"message": "Success"}, 200)

        return make_response({"message": "You cannot delete users"}, 403)


@user_api.route("/user/<int:user_id>/album")
@user_api.response(404, "User with this id not found", message_model)
class UserAlbum(Resource):
    @staticmethod
    @user_api.doc(description="Получить все альбомы пользователя")
    @user_api.response(200, "Success", album_list_model)
    def get(user_id):
        check_user_exist(user_id)

        auth = request.authorization
        viewer_id = 0 if not auth else dbi.get_user_id(request.authorization.username)

        album_list = dbi.get_albums_by_user_id(user_id, viewer_id)  # TODO chek get_albums_by_user_id
        # TODO преобразовать в нужный формат
        return make_response(album_list, 200)

    @staticmethod
    @user_api.doc(description="Создать новый альбом для пользователя")
    @requires_auth
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form", required=True)
                     .add_argument(name="description", type=str, location="form")
                     )
    @user_api.response(200, "Success", album_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(403, "You cannot create album for this user", message_model)
    def post(user_id):
        check_user_exist(user_id)

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)

        f = request.form
        if "name" not in f:
            return make_response({"message": "Invalid request"}, 400)
        name = f["full_name"]
        description = None if "description" not in f else f["description"]

        if viewer_id == user_id or viewer_is_admin:
            album = dbi.create_album(user_id, name=name, description=description)
            # TODO check create_album
            return make_response({"message": "Success"}, 200)

        return make_response({"message": "You cannot create album for this user"}, 403)


@user_api.route("/user/<int:user_id>/album/<int:album_id>")
@admin_api.route("/user/<int:user_id>/album/<int:album_id>")
@user_api.response(404, "User with this id not found", message_model)
@user_api.response(404, "Album with this id not found", message_model)
class UserAlbumID(Resource):
    @staticmethod
    @user_api.doc(description="Получить информацию о альбоме")
    @user_api.response(200, "Success", album_model)
    @user_api.response(403, "You cannot get this album", message_model)
    def get(user_id, album_id):
        check_user_exist(user_id)
        check_album_exist(user_id, album_id)

        auth = request.authorization
        viewer_id = 0 if not auth else dbi.get_user_id(request.authorization.username)

        is_album_access = dbi.get_album_access(viewer_id, album_id)  # TODO check get_album_access
        if is_album_access:
            album = dbi.get_album(album_id)  # TODO check get_album
            # TODO преобразовать в нужный формат
            return make_response(album, 200)

        return make_response({"message": "You cannot get this album"}, 403)

    @staticmethod
    @user_api.doc(description="Изменить информацию о альбоме")
    @requires_auth
    @user_api.response(200, "Success", message_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.response(403, "You cannot update this album", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form")
                     .add_argument(name="description", type=str, location="form")
                     )
    def put(user_id, album_id):
        check_user_exist(user_id)
        check_album_exist(user_id, album_id)

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)  # TODO check is_admin

        f = request.form
        if not ("full_name" in f or "email" in f or "password" in f):
            return make_response({"message": "Invalid request"}, 400)
        name = None if "name" not in f else f["name"]
        description = None if "description" not in f else f["description"]

        if viewer_id == user_id or viewer_is_admin:
            dbi.change_album(album_id,
                             name=name,
                             description=description
                             )  # TODO check change_album
            return make_response({"message": "Success"}, 200)

        return make_response({"message": "You cannot update this album"}, 403)

    @staticmethod
    @user_api.doc(description="Удалить альбом")
    @requires_auth
    @user_api.response(200, "Success", message_model)
    @user_api.response(403, "You cannot delete this album", message_model)
    def delete(user_id, album_id):
        check_user_exist(user_id)
        check_album_exist(user_id, album_id)

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)  # TODO check is_admin

        if viewer_id == user_id or viewer_is_admin:
            dbi.delete_user(album_id)  # TODO check delete_album
            return make_response({"message": "Success"}, 200)

        return make_response({"message": "You cannot delete this album"}, 403)


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
    @user_api.doc(description="Загрузить фото")
    @requires_auth
    @user_api.response(200, "Success", photo_model)
    @user_api.response(400, "Invalid request", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="file", type=FileStorage, location="files")
                     .add_argument(name="description", type=str, location="form")
                     .add_argument(name="album", type=int, location="form", action="append")
                     .add_argument(name="tag", type=int, location="form", action="append")
                     .add_argument(name="theme", type=int, location="form", action="append")
                     .add_argument(name="private", type=bool, location="form")
                     )
    def post():
        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)  # TODO check is_admin

        f = request.form
        description = None if "description" not in f else f["description"]
        album_list = None if "album" not in f else f.getlist("album")
        tag_list = None if "tag" not in f else f.getlist("tag")
        theme_list = None if "theme" not in f else f.getlist("album")
        is_private = False if "private" not in f else len(f.get("private")) <= 4

        if "file" not in request.files:
            return make_response({"message": "Invalid request"}, 400)
        file = request.files["file"]

        if not (file and allowed_file(file.filename)):
            return make_response({"message": "Invalid request"}, 400)

        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        while os.path.exists(path):
            filename = str(viewer_id) + filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        new_url = api.url_for(UploadFile, filename=filename)

        if is_private and (not (album_list or tag_list or theme_list)):
            return make_response({"message": "Invalid request"}, 400)
        if not is_private and (album_list or tag_list or theme_list):
            return make_response({"message": "Invalid request"}, 400)

        is_tags_exist = True if not tag_list else dbi.tags_exist(tag_list)
        is_albums_exist = True if not album_list else dbi.albums_exist(album_list)
        is_themes_exist = True if not theme_list else dbi.themes_exist(theme_list)

        if not (is_tags_exist and is_albums_exist and is_themes_exist):
            return make_response({"message": "Invalid request"}, 400)

        photo = dbi.create_photo(viewer_id,
                                 url=new_url,
                                 description=description,
                                 album_list=album_list,
                                 tag_list=tag_list,
                                 theme_list=theme_list,
                                 is_private=is_private)  # TODO check create_photo
        # TODO Преобразовать к формату
        return make_response(photo, 200)


@api.route("/uploads/<filename>", doc=False)
class UploadFile(Resource):
    @staticmethod
    def get(filename):
        print(filename)
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename)


@user_api.route("/photo/<int:photo_id>")
@user_api.response(404, "Not found photo with this ID", message_model)
class PhotoID(Resource):
    @staticmethod
    @user_api.doc(description="Получить полную информацию о фото")
    @user_api.response(200, "Success", photo_model)
    def get(photo_id):
        check_photo_exist(photo_id)

        auth = request.authorization
        viewer_id = 0 if not auth else dbi.get_user_id(request.authorization.username)

        photo = dbi.get_photo(photo_id, viewer_id)
        # TODO преобразовать к нужному формату
        return make_response(photo, 200)

    @staticmethod
    @user_api.doc(description="Изменить информацию о фото")
    @requires_auth
    @user_api.response(200, "Success", photo_model)
    @user_api.response(403, "You cannot update this photo", message_model)
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
    @user_api.doc(description="Удалить фото")
    @requires_auth
    @user_api.response(200, "Success", message_model)
    @user_api.response(403, "You cannot delete this photo", message_model)
    def delete(photo_id):
        pass


@user_api.route("/photo/<int:photo_id>/accessList")
@user_api.response(404, "Not found photo with this ID", message_model)
class AccessList(Resource):
    @staticmethod
    @user_api.doc(description="Получить список пользователей с доступом к фото")
    @requires_auth
    @user_api.response(200, "Success", int_list_model)
    @user_api.response(403, "You cannot get this list", message_model)
    def get(photo_id):
        check_photo_exist(photo_id)

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)  # TODO check is_admin

        user_id = dbi.get_user_id_by_photo_id(photo_id)  # TODO check get_user_id_by_photo_id
        if viewer_id == user_id or viewer_is_admin:
            photo_acces_list = dbi.get_photo_access_list(photo_id)  # TODO check get_photo_access_list
            return make_response({"message": "Success"}, 200)

        return make_response({"message": "You cannot get this list"}, 403)

    @staticmethod
    @user_api.doc(description="Установить список пользователей с доступом к фото")
    @requires_auth
    @user_api.response(200, "Success", int_list_model)
    @user_api.response(403, "You cannot interact with this list", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="user_ids", type=int, location="form", action="append", required=True)
                     )
    def post(photo_id):
        check_photo_exist(photo_id)

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)

        f = request.form
        if "user_ids" not in f:
            return make_response({"message": "Invalid request"}, 400)
        user_id_list = f["user_ids"]

        user_id = dbi.get_user_id_by_photo_id(photo_id)  # TODO check get_user_id_by_photo_id

        if viewer_id == user_id or viewer_is_admin:
            dbi.set_photo_access_list(photo_id, user_id_list)
            # TODO check set_photo_access_list
            return make_response({"message": "Success"}, 200)

        return make_response({"message": "You cannot set this list"}, 403)


# @user_api.route("/photo/<int:photo_id>/accessList/<int:user_id>")
# @user_api.response(404, "Not found photo with this ID", message_model)
# @user_api.response(404, "Not found user with this ID in list", message_model)
# class AccessListID(Resource):
#     @staticmethod
#     @user_api.doc(description="Удалить пользователя из списка доступа к фото")
#     @requires_auth
#     @user_api.response(200, "Success", message_model)
#     @user_api.response(403, "You cannot change this", message_model)
#     @user_api.response(404, "Not found photo with this ID", message_model)
#     def delete(photo_id, user_id):
#         check_photo_exist(photo_id)
#         pass
#
#     @staticmethod
#     @api.doc(security='basicAuth')
#     @user_api.response(200, "Success", message_model)
#     @user_api.response(401, "You must be logged in", message_model)
#     @user_api.response(403, "You cannot change this", message_model)
#     @user_api.response(404, "Not found photo with this ID", message_model)
#     def post(photo_id, user_id):
#         pass


@user_api.route("/photo/<int:photo_id>/comment")
class Comment(Resource):
    @staticmethod
    @user_api.doc(description="Написать комментарий")
    @requires_auth
    @user_api.response(200, "Success", comment_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You do not have access to this photo", message_model)
    @user_api.response(404, "Not found photo with this ID", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="text", type=str, location="form", required=True)
                     )
    def post(photo_id):
        check_photo_exist(photo_id)

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)

        f = request.form
        if "text" not in f:
            return make_response({"message": "Invalid request"}, 400)
        text = f["text"]

        is_access = dbi.get_access_to_photo_by_user_id(photo_id, viewer_id)
        # TODO check get_access_to_photo_by_user_id

        if is_access or viewer_is_admin:
            dbi.add_comment(viewer_id, photo_id, text) # TODO check add_comment
            return make_response({"message": "Success"}, 200)
        return make_response({"message": "You do not have access to this photo"}, 403)


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
    @user_api.doc(description="Получить список тем")
    @user_api.response(200, "Success", theme_list_model)
    def get():
        theme_list = dbi.get_theme_list() # TODO check get_theme_list
        # TODO Форматировать
        return make_response(theme_list, 200)

    @staticmethod
    @user_api.doc(description="Создать новую тему")
    @requires_auth
    @user_api.doc(doc=False)
    @user_api.response(200, "Success", theme_model)
    @user_api.response(401, "You must be logged in", message_model)
    @user_api.response(403, "You cannot create theme", message_model)
    @user_api.expect(RequestParser()
                     .add_argument(name="name", type=str, location="form", required=True)
                     )
    def post():

        viewer_id = dbi.get_user_id(request.authorization.username)
        viewer_is_admin = dbi.is_admin(viewer_id)

        f = request.form
        if "name" not in f:
            return make_response({"message": "Invalid request"}, 400)
        theme_name = f["name"]

        if viewer_is_admin:
            dbi.create_theme(theme_name)  # TODO check create_theme
            return make_response({"message": "Success"}, 200) # TODO Возвращать мб id?

        return make_response({"message": "You cannot create theme"}, 403)


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
