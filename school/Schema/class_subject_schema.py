from marshmallow import Schema, fields


class ClassSubjectCreateSchema(Schema):
    class_id = fields.Int(
        required=True
    )

    subject_id = fields.Int(
        required=True
    )

    teacher_id = fields.Int(
        allow_none=True
    )


class ClassSubjectUpdateSchema(Schema):
    class_id = fields.Int()

    subject_id = fields.Int()

    teacher_id = fields.Int(
        allow_none=True
    )


class ClassSubjectResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    class_id = fields.Int(
        dump_only=True
    )

    subject_id = fields.Int(
        dump_only=True
    )

    teacher_id = fields.Int(
        allow_none=True,
        dump_only=True
    )