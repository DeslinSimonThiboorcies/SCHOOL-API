from school.repositories.fee_repository import FeeRepository
from school.repositories.students_repo import StudentRepository
from school.models.fee import Fee


class FeeService:

    ALLOWED_STATUSES = {
        "PENDING",
        "PAID",
        "PARTIAL",
        "OVERDUE"
    }

    @staticmethod
    def create_fee(data):
        student_id = data.get("student_id")
        fee_type = data.get("fee_type")
        amount = data.get("amount")
        due_date = data.get("due_date")
        payment_status = data.get(
            "payment_status",
            "PENDING"
        ).upper()
        paid_date = data.get("paid_date")

        if not StudentRepository.get_by_id(student_id):
            raise ValueError("Student not found")

        if amount <= 0:
            raise ValueError("Fee amount must be greater than zero")

        if payment_status not in FeeService.ALLOWED_STATUSES:
            raise ValueError("Invalid payment status")

        if payment_status == "PAID" and not paid_date:
            raise ValueError(
                "Paid date is required when payment status is PAID"
            )

        fee = Fee(
            student_id=student_id,
            fee_type=fee_type,
            amount=amount,
            due_date=due_date,
            payment_status=payment_status,
            paid_date=paid_date
        )

        try:
            FeeRepository.create(fee)
            FeeRepository.commit()
            return fee

        except Exception:
            FeeRepository.rollback()
            raise

    @staticmethod
    def get_fee_by_id(fee_id):
        fee = FeeRepository.get_by_id(fee_id)

        if not fee:
            raise ValueError("Fee record not found")

        return fee

    @staticmethod
    def get_all_fees():
        return FeeRepository.get_all()

    @staticmethod
    def get_student_fees(student_id):
        if not StudentRepository.get_by_id(student_id):
            raise ValueError("Student not found")

        return FeeRepository.get_by_student_id(student_id)

    @staticmethod
    def update_fee(fee_id, data):
        fee = FeeService.get_fee_by_id(fee_id)

        if "fee_type" in data:
            fee.fee_type = data["fee_type"]

        if "amount" in data:
            if data["amount"] <= 0:
                raise ValueError(
                    "Fee amount must be greater than zero"
                )

            fee.amount = data["amount"]

        if "due_date" in data:
            fee.due_date = data["due_date"]

        if "payment_status" in data:
            payment_status = data["payment_status"].upper()

            if payment_status not in FeeService.ALLOWED_STATUSES:
                raise ValueError("Invalid payment status")

            fee.payment_status = payment_status

        if "paid_date" in data:
            fee.paid_date = data["paid_date"]

        if fee.payment_status == "PAID" and not fee.paid_date:
            raise ValueError(
                "Paid date is required when payment status is PAID"
            )

        try:
            FeeRepository.update()
            return fee

        except Exception:
            FeeRepository.rollback()
            raise

    @staticmethod
    def delete_fee(fee_id):
        fee = FeeService.get_fee_by_id(fee_id)

        try:
            FeeRepository.delete(fee)
            return fee

        except Exception:
            FeeRepository.rollback()
            raise