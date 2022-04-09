from flask import Flask, request, make_response
from flask_restx import Api, fields, Resource
from flask_restx.reqparse import RequestParser

app = Flask(__name__)
app.secret_key = "secretKey"

api = Api(
    app,
    version="0.1",
    title="Photo Service API",
    default="Photo Service",
    doc="/doc"
)

message_model = api.model("message", {
    "message": fields.String
})
user_info_model = api.model("user_ifo", {
    "id": fields.Integer,
    "name": fields.String
})
comment_model = api.model("comment", {
    "id": fields.Integer,
    "user": fields.Nested(user_info_model),
    "photo_id": fields.Integer,
    "text": fields.String
})
photo_preview_model = api.model("preview", {
    "id": fields.Integer,
    "url": fields.Url
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


@api.route("/registration")
class UserRegistration(Resource):
    @staticmethod
    @api.response(200, "Success")  # add token model
    @api.response(400, "Invalid request", message_model)
    @api.response(401, "This username is already taken", message_model)
    @api.expect(RequestParser()
                .add_argument(name="username", type=str, location="form")
                .add_argument(name="password", type=str, location="form")
                )
    @api.doc("asd")
    def post():
        f = request.form
        if not ("username" in f and "password" in f):
            return make_response({"message": "Invalid request"}, 400)

        username = f["username"]
        password = f["password"]
        pass
        return f'123'


@api.route("/search")
class Search(Resource):
    @staticmethod
    @api.expect(RequestParser()
                .add_argument(name="user_id", type=int, location="args")
                .add_argument(name="album_id", type=int, location="args")
                .add_argument(name="theme_id", type=int, location="args")
                .add_argument(name="tag_id", type=int, location="args")
                .add_argument(name="page", type=int, location="args")
                .add_argument(name="amount", type=int, location="args")
                )
    def get():
        args = request.args
        DEFAULT_AMOUNT = 10
        DEFAULT_PAGE = 1

        amount = int(args["amount"]) if "amount" in args else DEFAULT_AMOUNT
        page = int(args["page"]) if "page" in args else DEFAULT_PAGE
        pass
        return f'page:{page} amount:{amount}'


if __name__ == "__main__":
    # logging.basicConfig(filename="Converter.log", level=logging.DEBUG,
    #                     format="[%(asctime)s] %(levelname)s - %(message)s")
    # print(type(message_model))
    app.run(host="localhost", port=5002)
