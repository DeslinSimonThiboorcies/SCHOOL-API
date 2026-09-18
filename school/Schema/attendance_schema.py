from marshmallow import Schema, fields, validate


class AttendanceCreateSchema(Schema):
    student_id = fields.Int(
        required=True
    )

    class_id = fields.Int(
        required=True
    )

    attendance_date = fields.Date(
        required=True
    )

    status = fields.Str(
        load_default="PRESENT",
        validate=validate.OneOf([
            "PRESENT",
            "ABSENT",
            "LATE",
            "LEAVE"
        ])
    )


class AttendanceUpdateSchema(Schema):
    attendance_date = fields.Date()

    status = fields.Str(
        validate=validate.OneOf([
            "PRESENT",
            "ABSENT",
            "LATE",
            "LEAVE"
        ])
    )


class AttendanceResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    student_id = fields.Int(
        dump_only=True
    )

    class_id = fields.Int(
        dump_only=True
    )

    attendance_date = fields.Date(
        dump_only=True
    )

    status = fields.Str(
        dump_only=True
    )

    marked_at = fields.DateTime(
        dump_only=True
    )