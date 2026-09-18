from marshmallow import Schema, fields, validate


class StudentCreateSchema(Schema):
    user_id = fields.Int(
        required=True
    )

    admission_number = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=20)
    )

    joining_date = fields.DateTime(
        allow_none=True
    )

    class_id = fields.Int(
        required=True
    )

    parent_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    parent_phone = fields.Str(
        required=True,
        validate=validate.Length(min=7, max=15)
    )


class StudentUpdateSchema(Schema):
    admission_number = fields.Str(
        validate=validate.Length(min=2, max=20)
    )

    class_id = fields.Int()

    parent_name = fields.Str(
        validate=validate.Length(min=2, max=100)
    )

    parent_phone = fields.Str(
        validate=validate.Length(min=7, max=15)
    )


class StudentResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    user_id = fields.Int(
        dump_only=True
    )

    admission_number = fields.Str(
        dump_only=True
    )

    joining_date = fields.DateTime(
        dump_only=True
    )

    class_id = fields.Int(
        dump_only=True
    )

    parent_name = fields.Str(
        dump_only=True
    )

    parent_phone = fields.Str(
        dump_only=True
    )