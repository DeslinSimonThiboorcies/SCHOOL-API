from school.repositories.subject_repository import SubjectRepository
from school.models.subject import Subject


class SubjectService:

    @staticmethod
    def create_subject(data):
        subject_name = data.get("subject_name")
        subject_code = data.get("subject_code")
        description = data.get("description")

        if SubjectRepository.get_by_name(subject_name):
            raise ValueError("Subject name already exists")

        if SubjectRepository.get_by_code(subject_code):
            raise ValueError("Subject code already exists")

        subject = Subject(
            subject_name=subject_name,
            subject_code=subject_code,
            description=description
        )

        try:
            SubjectRepository.create(subject)
            SubjectRepository.commit()
            return subject

        except Exception:
            SubjectRepository.rollback()
            raise

    @staticmethod
    def get_subject_by_id(subject_id):
        subject = SubjectRepository.get_by_id(subject_id)

        if not subject:
            raise ValueError("Subject not found")

        return subject

    @staticmethod
    def get_all_subjects():
        return SubjectRepository.get_all()

    @staticmethod
    def update_subject(subject_id, data):
        subject = SubjectService.get_subject_by_id(subject_id)

        if "subject_name" in data:
            existing_subject = SubjectRepository.get_by_name(
                data["subject_name"]
            )

            if existing_subject and existing_subject.id != subject.id:
                raise ValueError("Subject name already exists")

            subject.subject_name = data["subject_name"]

        if "subject_code" in data:
            existing_subject = SubjectRepository.get_by_code(
                data["subject_code"]
            )

            if existing_subject and existing_subject.id != subject.id:
                raise ValueError("Subject code already exists")

            subject.subject_code = data["subject_code"]

        if "description" in data:
            subject.description = data["description"]

        try:
            SubjectRepository.update()
            return subject

        except Exception:
            SubjectRepository.rollback()
            raise

    @staticmethod
    def delete_subject(subject_id):
        subject = SubjectService.get_subject_by_id(subject_id)

        try:
            SubjectRepository.delete(subject)
            return subject

        except Exception:
            SubjectRepository.rollback()
            raise