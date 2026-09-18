from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class FeeCreateSchema(Schema):
    student_id = fields.Int(
        required=True
    )

    fee_type = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=50)
    )

    amount = fields.Decimal(
        required=True,
        as_string=False,
        validate=validate.Range(min=0.01)
    )

    due_date = fields.Date(
        required=True
    )

    payment_status = fields.Str(
        load_default="PENDING",
        validate=validate.OneOf([
            "PENDING",
            "PAID",
            "PARTIAL",
            "OVERDUE"
        ])
    )

    paid_date = fields.Date(
        allow_none=True
    )

    @validates_schema
    def validate_paid_date(self, data, **kwargs):
        payment_status = data.get("payment_status")
        paid_date = data.get("paid_date")

        if payment_status == "PAID" and not paid_date:
            raise ValidationError(
                "Paid date is required when payment status is PAID"
            )


class FeeUpdateSchema(Schema):
    fee_type = fields.Str(
        validate=validate.Length(min=2, max=50)
    )

    amount = fields.Decimal(
        as_string=False,
        validate=validate.Range(min=0.01)
    )

    due_date = fields.Date()

    payment_status = fields.Str(
        validate=validate.OneOf([
            "PENDING",
            "PAID",
            "PARTIAL",
            "OVERDUE"
        ])
    )

    paid_date = fields.Date(
        allow_none=True
    )


class FeeResponseSchema(Schema):
    id = fields.Int(
        dump_only=True
    )

    student_id = fields.Int(
        dump_only=True
    )

    fee_type = fields.Str(
        dump_only=True
    )

    amount = fields.Decimal(
        as_string=False,
        dump_only=True
    )

    due_date = fields.Date(
        dump_only=True
    )

    payment_status = fields.Str(
        dump_only=True
    )

    paid_date = fields.Date(
        allow_none=True,
        dump_only=True
    )

    created_at = fields.DateTime(
        dump_only=True
    )