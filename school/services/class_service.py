from school.repositories.class_repository import ClassRepository
from school.models.class_model import ClassModel


class ClassService:

    @staticmethod
    def create_class(data):
        class_name = data.get("class_name")
        section = data.get("section")
        academic_year = data.get("academic_year")

        existing_class = ClassRepository.get_by_name_and_section(
            class_name,
            section,
            academic_year
        )

        if existing_class:
            raise ValueError(
                "This class and section already exist for the academic year"
            )

        class_obj = ClassModel(
            class_name=class_name,
            section=section,
            academic_year=academic_year
        )

        try:
            ClassRepository.create(class_obj)
            ClassRepository.commit()
            return class_obj

        except Exception:
            ClassRepository.rollback()
            raise

    @staticmethod
    def get_class_by_id(class_id):
        class_obj = ClassRepository.get_by_id(class_id)

        if not class_obj:
            raise ValueError("Class not found")

        return class_obj

    @staticmethod
    def get_all_classes():
        return ClassRepository.get_all()

    @staticmethod
    def update_class(class_id, data):
        class_obj = ClassService.get_class_by_id(class_id)

        if "class_name" in data:
            class_obj.class_name = data["class_name"]

        if "section" in data:
            class_obj.section = data["section"]

        if "academic_year" in data:
            class_obj.academic_year = data["academic_year"]

        try:
            ClassRepository.update()
            return class_obj

        except Exception:
            ClassRepository.rollback()
            raise

    @staticmethod
    def delete_class(class_id):
        class_obj = ClassService.get_class_by_id(class_id)

        try:
            ClassRepository.delete(class_obj)
            return class_obj

        except Exception:
            ClassRepository.rollback()
            raise