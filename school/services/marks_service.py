from school.repositories.marks_repository import MarksRepository
from school.repositories.students_repo import StudentRepository
from school.repositories.subject_repository import SubjectRepository
from school.models.marks import Mark


class MarksService:

    @staticmethod
    def create_mark(data):
        student_id = data.get("student_id")
        subject_id = data.get("subject_id")
        exam_name = data.get("exam_name")
        marks_obtained = data.get("marks_obtained")
        maximum_marks = data.get("maximum_marks")
        exam_date = data.get("exam_date")

        if not StudentRepository.get_by_id(student_id):
            raise ValueError("Student not found")

        if not SubjectRepository.get_by_id(subject_id):
            raise ValueError("Subject not found")

        if marks_obtained < 0:
            raise ValueError("Obtained marks cannot be negative")

        if maximum_marks <= 0:
            raise ValueError("Maximum marks must be greater than zero")

        if marks_obtained > maximum_marks:
            raise ValueError(
                "Obtained marks cannot be greater than maximum marks"
            )

        mark = Mark(
            student_id=student_id,
            subject_id=subject_id,
            exam_name=exam_name,
            marks_obtained=marks_obtained,
            maximum_marks=maximum_marks,
            exam_date=exam_date
        )

        try:
            MarksRepository.create(mark)
            MarksRepository.commit()
            return mark

        except Exception:
            MarksRepository.rollback()
            raise

    @staticmethod
    def get_mark_by_id(mark_id):
        mark = MarksRepository.get_by_id(mark_id)

        if not mark:
            raise ValueError("Mark record not found")

        return mark

    @staticmethod
    def get_all_marks():
        return MarksRepository.get_all()

    @staticmethod
    def get_student_marks(student_id):
        if not StudentRepository.get_by_id(student_id):
            raise ValueError("Student not found")

        return MarksRepository.get_by_student_id(student_id)

    @staticmethod
    def update_mark(mark_id, data):
        mark = MarksService.get_mark_by_id(mark_id)

        if "marks_obtained" in data:
            if data["marks_obtained"] < 0:
                raise ValueError("Obtained marks cannot be negative")

            mark.marks_obtained = data["marks_obtained"]

        if "maximum_marks" in data:
            if data["maximum_marks"] <= 0:
                raise ValueError(
                    "Maximum marks must be greater than zero"
                )

            mark.maximum_marks = data["maximum_marks"]

        if mark.marks_obtained > mark.maximum_marks:
            raise ValueError(
                "Obtained marks cannot be greater than maximum marks"
            )

        if "exam_name" in data:
            mark.exam_name = data["exam_name"]

        if "exam_date" in data:
            mark.exam_date = data["exam_date"]

        try:
            MarksRepository.update()
            return mark

        except Exception:
            MarksRepository.rollback()
            raise

    @staticmethod
    def delete_mark(mark_id):
        mark = MarksService.get_mark_by_id(mark_id)

        try:
            MarksRepository.delete(mark)
            return mark

        except Exception:
            MarksRepository.rollback()
            raise