from datetime import date


def require_fields(data, required_fields):
    missing_fields = [
        field
        for field in required_fields
        if data.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )


def validate_positive_number(value, field_name):
    if value is None:
        raise ValueError(f"{field_name} is required")

    if value <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero"
        )


def validate_non_negative_number(value, field_name):
    if value is None:
        raise ValueError(f"{field_name} is required")

    if value < 0:
        raise ValueError(
            f"{field_name} cannot be negative"
        )


def validate_date_not_in_future(value, field_name):
    if value is None:
        raise ValueError(f"{field_name} is required")

    if value > date.today():
        raise ValueError(
            f"{field_name} cannot be in the future"
        )