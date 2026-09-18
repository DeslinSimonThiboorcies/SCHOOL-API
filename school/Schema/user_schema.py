from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    full_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    email = fields.Email(
        required=True
    )

    phone_number = fields.Str(
        allow_none=True,
        validate=validate.Length(max=15)
    )

    date_of_birth = fields.Date(
        required=True,
        allow_none=False
    )

    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128)
    )

    role = fields.Str(
        load_default="STUDENT",
        validate=validate.OneOf([
            "PRINCIPAL",
            "TEACHER",
            "STUDENT"
        ])
    )


class UserLoginSchema(Schema):
    email = fields.Email(
        required=True
    )

    password = fields.Str(
        required=True,
        load_only=True
    )


class UserResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    full_name = fields.Str(
        dump_only=True
    )

    email = fields.Email(
        dump_only=True
    )

    phone_number = fields.Str(
        allow_none=True,
        dump_only=True
    )

    date_of_birth = fields.Date(
        allow_none=True,
        dump_only=True
    )

    role = fields.Str(
        dump_only=True
    )

    login_date = fields.DateTime(
        allow_none=True,
        dump_only=True
    )