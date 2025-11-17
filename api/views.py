from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request, decode_token
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from .models import db, UserModel, CategoryModel, RecordModel
from .schemas import UserSchema, CategorySchema, RecordSchema

blp = Blueprint("API", __name__, description="Operations for finance tracking API")

@blp.route("/healthcheck")
def healthcheck():
    """Check the health of the application"""
    return {"status": "OK", "message": "Application is healthy"}


@blp.route("/debug_jwt")
class JWTDebug(MethodView):
    def get(self):
        info = {}

        from flask import current_app
        info["JWT_SECRET_KEY"] = repr(current_app.config.get("JWT_SECRET_KEY"))

        auth_header = request.headers.get("Authorization")
        info["Authorization header"] = repr(auth_header)

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            info["raw_token"] = token
            try:
                decoded = decode_token(token, allow_expired=True)
                info["decoded_token"] = decoded
            except Exception as e:
                info["decoded_error"] = str(e)

            try:
                verify_jwt_in_request()
                info["verify_jwt_in_request"] = "PASSED"
            except Exception as e:
                info["verify_jwt_in_request"] = f"FAILED: {str(e)}"
        else:
            info["token_present"] = False

        return jsonify(info)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema(exclude=("records", "categories")))
    def post(self, user_data):
        """Register a new user"""

        if UserModel.query.filter(UserModel.name == user_data["name"]).first():
            abort(409, "Username already exists")

        user = UserModel(name=user_data["name"])
        user.set_password(user_data["password"])

        db.session.add(user)
        db.session.commit()
        return user

@blp.route("/login")
class UserLogin(MethodView):
    def post(self):
        """Login a user"""
        user_data = request.get_json()

        user = UserModel.query.filter(UserModel.name == user_data["name"]).first()

        if user and user.check_password(user_data["password"]):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        abort(409, "Invalid password or login credentials")



@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get user by ID"""
        return UserModel.query.get_or_404(user_id)

    @jwt_required()
    @blp.response(204)
    def delete(self, user_id):
        """Delete user by ID"""
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return ""

@blp.route("/category")
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        """Get all general categories and user-specific categories"""
        return CategoryModel.query.all()

    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        """Create a new category (general if user_id is null)"""
        category = CategoryModel(**category_data)
        db.session.add(category)
        db.session.commit()
        return category


@blp.route("/category/<int:category_id>")
class Category(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        """Get category by ID"""
        return CategoryModel.query.get_or_404(category_id)

    @jwt_required()
    @blp.response(204)
    def delete(self, category_id):
        """Delete category by ID"""
        category = CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return ""


@blp.route("/record")
class RecordList(MethodView):
    @blp.response(200, RecordSchema(many=True))
    @jwt_required()
    def get(self):
        """Get records, filtered by user_id and/or category_id"""
        user_id = get_jwt_identity()
        category_id = request.args.get('category_id')

        if not user_id and not category_id:
            abort(400, message="At least one parameter (user_id or category_id) is required.")

        query = RecordModel.query
        if user_id:
            query = query.filter(RecordModel.user_id == user_id)
        if category_id:
            query = query.filter(RecordModel.category_id == category_id)

        return query.all()

    @jwt_required()
    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):

        current_user_id = get_jwt_identity()
        """Create a new record"""
        record = RecordModel(user_id = current_user_id, **record_data)
        db.session.add(record)
        db.session.commit()
        return record


@blp.route("/record/<int:record_id>")
class Record(MethodView):
    @jwt_required()
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        """Get record by ID"""
        return RecordModel.query.get_or_404(record_id)

    @jwt_required()
    @blp.response(204)
    def delete(self, record_id):
        """Delete record by ID"""
        record = RecordModel.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return ""