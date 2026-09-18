from marshmallow import Schema, fields, validate


class TeacherCreateSchema(Schema):
    user_id = fields.Int(
        required=True
    )

    employee_number = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=20)
    )

    department = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=50)
    )

    qualification = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=50)
    )


class TeacherUpdateSchema(Schema):
    employee_number = fields.Str(
        validate=validate.Length(min=2, max=20)
    )

    department = fields.Str(
        validate=validate.Length(min=2, max=50)
    )

    qualification = fields.Str(
        validate=validate.Length(min=2, max=50)
    )


class TeacherResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    user_id = fields.Int(
        dump_only=True
    )

    employee_number = fields.Str(
        dump_only=True
    )

    department = fields.Str(
        dump_only=True
    )

    qualification = fields.Str(
        dump_only=True
    )

    joining_date = fields.DateTime(
        dump_only=True
    )