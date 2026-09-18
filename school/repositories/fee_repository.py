from school.extensison.db import db
from school.models.fee import Fee


class FeeRepository:

    @staticmethod
    def get_by_id(fee_id):
        return db.session.get(Fee, fee_id)

    @staticmethod
    def get_all():
        return Fee.query.all()

    @staticmethod
    def get_by_student_id(student_id):
        return Fee.query.filter_by(
            student_id=student_id
        ).all()

    @staticmethod
    def get_by_payment_status(payment_status):
        return Fee.query.filter_by(
            payment_status=payment_status
        ).all()

    @staticmethod
    def get_pending_fees():
        return Fee.query.filter_by(
            payment_status="PENDING"
        ).all()

    @staticmethod
    def get_by_student_and_fee_type(student_id, fee_type):
        return Fee.query.filter_by(
            student_id=student_id,
            fee_type=fee_type
        ).all()

    @staticmethod
    def create(fee):
        db.session.add(fee)
        db.session.flush()
        return fee

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(fee):
        db.session.delete(fee)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()