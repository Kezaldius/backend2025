from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from .models import db, UserModel, CategoryModel, RecordModel
from .schemas import UserSchema, CategorySchema, RecordSchema

blp = Blueprint("API", __name__, description="Operations for finance tracking API")

@blp.route("/healthcheck")
def healthcheck():
    """Check the health of the application"""
    return {"status": "OK", "message": "Application is healthy"}



@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get list of all users"""
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """Create a new user"""
        if UserModel.query.filter(UserModel.name == user_data["name"]).first():
            abort(409, message="A user with that name already exists.")

        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get user by ID"""
        return UserModel.query.get_or_404(user_id)

    @blp.response(204)
    def delete(self, user_id):
        """Delete user by ID"""
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return ""


@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        """Get all general categories and user-specific categories"""
        return CategoryModel.query.all()

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
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        """Get category by ID"""
        return CategoryModel.query.get_or_404(category_id)

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
    def get(self):
        """Get records, filtered by user_id and/or category_id"""
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')

        if not user_id and not category_id:
            abort(400, message="At least one parameter (user_id or category_id) is required.")

        query = RecordModel.query
        if user_id:
            query = query.filter(RecordModel.user_id == user_id)
        if category_id:
            query = query.filter(RecordModel.category_id == category_id)

        return query.all()

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):
        """Create a new record"""
        record = RecordModel(**record_data)
        db.session.add(record)
        db.session.commit()
        return record


@blp.route("/record/<int:record_id>")
class Record(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        """Get record by ID"""
        return RecordModel.query.get_or_404(record_id)

    @blp.response(204)
    def delete(self, record_id):
        """Delete record by ID"""
        record = RecordModel.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return ""