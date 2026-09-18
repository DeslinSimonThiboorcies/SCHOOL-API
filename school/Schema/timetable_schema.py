from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class TimetableCreateSchema(Schema):
    class_id = fields.Int(
        required=True
    )

    subject_id = fields.Int(
        required=True
    )

    teacher_id = fields.Int(
        required=True
    )

    day_of_week = fields.Str(
        required=True,
        validate=validate.OneOf([
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY"
        ])
    )

    start_time = fields.Time(
        required=True
    )

    end_time = fields.Time(
        required=True
    )

    room_number = fields.Str(
        allow_none=True,
        validate=validate.Length(max=20)
    )

    @validates_schema
    def validate_time(self, data, **kwargs):
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if (
            start_time is not None
            and end_time is not None
            and start_time >= end_time
        ):
            raise ValidationError(
                "Start time must be earlier than end time"
            )


class TimetableUpdateSchema(Schema):
    class_id = fields.Int()

    subject_id = fields.Int()

    teacher_id = fields.Int()

    day_of_week = fields.Str(
        validate=validate.OneOf([
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY"
        ])
    )

    start_time = fields.Time()

    end_time = fields.Time()

    room_number = fields.Str(
        allow_none=True,
        validate=validate.Length(max=20)
    )

    @validates_schema
    def validate_time(self, data, **kwargs):
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if (
            start_time is not None
            and end_time is not None
            and start_time >= end_time
        ):
            raise ValidationError(
                "Start time must be earlier than end time"
            )


class TimetableResponseSchema(Schema):
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
        dump_only=True
    )

    day_of_week = fields.Str(
        dump_only=True
    )

    start_time = fields.Time(
        dump_only=True
    )

    end_time = fields.Time(
        dump_only=True
    )

    room_number = fields.Str(
        allow_none=True,
        dump_only=True
    )