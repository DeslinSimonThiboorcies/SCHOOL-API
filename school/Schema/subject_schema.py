from marshmallow import Schema, fields, validate


class SubjectCreateSchema(Schema):
    subject_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    subject_code = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=20)
    )

    description = fields.Str(
        allow_none=True
    )


class SubjectUpdateSchema(Schema):
    subject_name = fields.Str(
        validate=validate.Length(min=2, max=100)
    )

    subject_code = fields.Str(
        validate=validate.Length(min=2, max=20)
    )

    description = fields.Str(
        allow_none=True
    )


class SubjectResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    subject_name = fields.Str(
        dump_only=True
    )

    subject_code = fields.Str(
        dump_only=True
    )

    description = fields.Str(
        allow_none=True,
        dump_only=True
    )