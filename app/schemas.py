from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError,
)
import re




def validate_color(value):
    pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
    if not pattern.match(value):
        raise ValidationError("Invalid color format. Use #RRGGBB")

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
        )
    description = fields.Str(
        load_default='',
        validate=validate.Length(max=500)
    )
    due_date = fields.DateTime(format='iso', allow_none=True)
    category_id = fields.Int(load_default=None, allow_none=True)
    completed = fields.Bool()
    created_at = fields.DateTime(format='iso', dump_only=True)
    updated_at = fields.DateTime(format='iso', dump_only=True)

    @validates('category_id')
    def validate_category_id(self, value, **kwargs):
        if value is not None:
            from app.models import CategoryModel
            cat = CategoryModel.query.get(value)
            if not cat:
                raise ValidationError('Category does not exist')
        return value



class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )
    color = fields.Str(
        allow_none=True,
        validate=validate_color
    )
    task_count = fields.Int(dump_only=True)

    @validates('name')
    def validate_category_name(self, value, **kwargs):
        from app.models import CategoryModel
        nam = CategoryModel.query.filter_by(name=value).first()
        if nam:
            raise ValidationError('Category with this name already exists.')
        return value