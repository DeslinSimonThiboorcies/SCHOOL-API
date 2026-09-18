from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class MarkCreateSchema(Schema):
    student_id = fields.Int(
        required=True
    )

    subject_id = fields.Int(
        required=True
    )

    exam_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    marks_obtained = fields.Float(
        required=True,
        validate=validate.Range(min=0)
    )

    maximum_marks = fields.Float(
        required=True,
        validate=validate.Range(min=0.01)
    )

    exam_date = fields.Date(
        required=True
    )

    @validates_schema
    def validate_marks(self, data, **kwargs):
        marks_obtained = data.get("marks_obtained")
        maximum_marks = data.get("maximum_marks")

        if (
            marks_obtained is not None
            and maximum_marks is not None
            and marks_obtained > maximum_marks
        ):
            raise ValidationError(
                "Obtained marks cannot be greater than maximum marks"
            )


class MarkUpdateSchema(Schema):
    exam_name = fields.Str(
        validate=validate.Length(min=2, max=100)
    )

    marks_obtained = fields.Float(
        validate=validate.Range(min=0)
    )

    maximum_marks = fields.Float(
        validate=validate.Range(min=0.01)
    )

    exam_date = fields.Date()

    @validates_schema
    def validate_marks(self, data, **kwargs):
        marks_obtained = data.get("marks_obtained")
        maximum_marks = data.get("maximum_marks")

        if (
            marks_obtained is not None
            and maximum_marks is not None
            and marks_obtained > maximum_marks
        ):
            raise ValidationError(
                "Obtained marks cannot be greater than maximum marks"
            )


class MarkResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    student_id = fields.Int(
        dump_only=True
    )

    subject_id = fields.Int(
        dump_only=True
    )

    exam_name = fields.Str(
        dump_only=True
    )

    marks_obtained = fields.Float(
        dump_only=True
    )

    maximum_marks = fields.Float(
        dump_only=True
    )

    exam_date = fields.Date(
        dump_only=True
    )

    created_at = fields.DateTime(
        dump_only=True
    )