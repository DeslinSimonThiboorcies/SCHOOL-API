from school.repositories.class_subject_repository import ClassSubjectRepository
from school.repositories.class_repository import ClassRepository
from school.repositories.subject_repository import SubjectRepository
from school.repositories.teacher_repo import TeacherRepository
from school.models.class_subject import ClassSubject


class ClassSubjectService:

    @staticmethod
    def create_class_subject(data):
        class_id = data.get("class_id")
        subject_id = data.get("subject_id")
        teacher_id = data.get("teacher_id")

        class_obj = ClassRepository.get_by_id(class_id)

        if not class_obj:
            raise ValueError("Class not found")

        subject = SubjectRepository.get_by_id(subject_id)

        if not subject:
            raise ValueError("Subject not found")

        if teacher_id is not None:
            teacher = TeacherRepository.get_by_id(teacher_id)

            if not teacher:
                raise ValueError("Teacher not found")

        existing_assignment = (
            ClassSubjectRepository.get_by_class_and_subject(
                class_id,
                subject_id
            )
        )

        if existing_assignment:
            raise ValueError(
                "This subject is already assigned to this class"
            )

        class_subject = ClassSubject(
            class_id=class_id,
            subject_id=subject_id,
            teacher_id=teacher_id
        )

        try:
            ClassSubjectRepository.create(class_subject)
            ClassSubjectRepository.commit()
            return class_subject

        except Exception:
            ClassSubjectRepository.rollback()
            raise

    @staticmethod
    def get_class_subject_by_id(class_subject_id):
        class_subject = ClassSubjectRepository.get_by_id(
            class_subject_id
        )

        if not class_subject:
            raise ValueError("Class subject assignment not found")

        return class_subject

    @staticmethod
    def get_all_class_subjects():
        return ClassSubjectRepository.get_all()

    @staticmethod
    def get_subjects_by_class(class_id):
        class_obj = ClassRepository.get_by_id(class_id)

        if not class_obj:
            raise ValueError("Class not found")

        return ClassSubjectRepository.get_by_class_id(class_id)

    @staticmethod
    def update_class_subject(class_subject_id, data):
        class_subject = (
            ClassSubjectService.get_class_subject_by_id(
                class_subject_id
            )
        )

        if "class_id" in data:
            if not ClassRepository.get_by_id(data["class_id"]):
                raise ValueError("Class not found")

            class_subject.class_id = data["class_id"]

        if "subject_id" in data:
            if not SubjectRepository.get_by_id(data["subject_id"]):
                raise ValueError("Subject not found")

            class_subject.subject_id = data["subject_id"]

        if "teacher_id" in data:
            if data["teacher_id"] is not None:
                if not TeacherRepository.get_by_id(data["teacher_id"]):
                    raise ValueError("Teacher not found")

            class_subject.teacher_id = data["teacher_id"]

        try:
            ClassSubjectRepository.update()
            return class_subject

        except Exception:
            ClassSubjectRepository.rollback()
            raise

    @staticmethod
    def delete_class_subject(class_subject_id):
        class_subject = (
            ClassSubjectService.get_class_subject_by_id(
                class_subject_id
            )
        )

        try:
            ClassSubjectRepository.delete(class_subject)
            return class_subject

        except Exception:
            ClassSubjectRepository.rollback()
            raise