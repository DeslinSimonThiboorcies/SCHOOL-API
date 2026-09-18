from school.extensison.db import db
from school.models.class_model import ClassModel


class ClassRepository:

    @staticmethod
    def get_by_id(class_id):
        return db.session.get(ClassModel, class_id)

    @staticmethod
    def get_all():
        return ClassModel.query.all()

    @staticmethod
    def get_by_name_and_section(class_name, section, academic_year):
        return ClassModel.query.filter_by(
            class_name=class_name,
            section=section,
            academic_year=academic_year
        ).first()

    @staticmethod
    def create(class_obj):
        db.session.add(class_obj)
        db.session.flush()
        return class_obj

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(class_obj):
        db.session.delete(class_obj)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()