from marshmallow import Schema, fields

class PlainCategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
class PlainUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

class RecordSchema(Schema):
    id = fields.Integer(dump_only=True)
    sum = fields.Float(required=True)
    created_at = fields.Str(dump_only=True)

    user_id = fields.Integer(required=True,load_only=True)
    category_id = fields.Integer(required=True,load_only=True)

    user = fields.Nested(PlainUserSchema(), dump_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)


class CategorySchema(PlainCategorySchema):
    user_id = fields.Int(required=False, allow_none=True)
    records = fields.List(fields.Nested(RecordSchema(exclude=("category",))), dump_only=True)

class UserSchema(PlainUserSchema):
    records = fields.List(fields.Nested(RecordSchema(exclude=("user",))), dump_only=True)
    categories = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)