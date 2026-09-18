from marshmallow import Schema, fields, validate


class ClassCreateSchema(Schema):
    class_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )

    section = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=10)
    )

    academic_year = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=20)
    )


class ClassUpdateSchema(Schema):
    class_name = fields.Str(
        validate=validate.Length(min=1, max=50)
    )

    section = fields.Str(
        validate=validate.Length(min=1, max=10)
    )

    academic_year = fields.Str(
        validate=validate.Length(min=4, max=20)
    )


class ClassResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    class_name = fields.Str(
        dump_only=True
    )

    section = fields.Str(
        dump_only=True
    )

    academic_year = fields.Str(
        dump_only=True
    )

    created_at = fields.DateTime(
        dump_only=True
    )