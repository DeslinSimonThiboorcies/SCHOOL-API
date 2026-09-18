from school.repositories.timetable_repository import TimetableRepository
from school.repositories.class_repository import ClassRepository
from school.repositories.subject_repository import SubjectRepository
from school.repositories.teacher_repo import TeacherRepository
from school.models.timetable import Timetable


class TimetableService:

    ALLOWED_DAYS = {
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY",
        "SUNDAY"
    }

    @staticmethod
    def create_timetable(data):
        class_id = data.get("class_id")
        subject_id = data.get("subject_id")
        teacher_id = data.get("teacher_id")
        day_of_week = data.get("day_of_week", "").upper()
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        room_number = data.get("room_number")

        if not ClassRepository.get_by_id(class_id):
            raise ValueError("Class not found")

        if not SubjectRepository.get_by_id(subject_id):
            raise ValueError("Subject not found")

        if not TeacherRepository.get_by_id(teacher_id):
            raise ValueError("Teacher not found")

        if day_of_week not in TimetableService.ALLOWED_DAYS:
            raise ValueError("Invalid day of week")

        if start_time >= end_time:
            raise ValueError(
                "Start time must be earlier than end time"
            )

        timetable = Timetable(
            class_id=class_id,
            subject_id=subject_id,
            teacher_id=teacher_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            room_number=room_number
        )

        try:
            TimetableRepository.create(timetable)
            TimetableRepository.commit()
            return timetable

        except Exception:
            TimetableRepository.rollback()
            raise

    @staticmethod
    def get_timetable_by_id(timetable_id):
        timetable = TimetableRepository.get_by_id(timetable_id)

        if not timetable:
            raise ValueError("Timetable entry not found")

        return timetable

    @staticmethod
    def get_all_timetable():
        return TimetableRepository.get_all()

    @staticmethod
    def get_all_timetables():
        return TimetableService.get_all_timetable()

    @staticmethod
    def get_by_class_id(class_id):
        return TimetableService.get_class_timetable(class_id)

    @staticmethod
    def get_by_subject_id(subject_id):
        return TimetableRepository.get_by_subject_id(subject_id)

    @staticmethod
    def get_by_teacher_id(teacher_id):
        return TimetableRepository.get_by_teacher_id(teacher_id)

    @staticmethod
    def get_by_day(day_of_week):
        return Timetable.query.filter_by(day_of_week=day_of_week.upper()).all()

    @staticmethod
    def get_class_timetable(class_id):
        if not ClassRepository.get_by_id(class_id):
            raise ValueError("Class not found")

        return TimetableRepository.get_by_class_id(class_id)

    @staticmethod
    def update_timetable(timetable_id, data):
        timetable = TimetableService.get_timetable_by_id(
            timetable_id
        )

        if "class_id" in data:
            if not ClassRepository.get_by_id(data["class_id"]):
                raise ValueError("Class not found")

            timetable.class_id = data["class_id"]

        if "subject_id" in data:
            if not SubjectRepository.get_by_id(data["subject_id"]):
                raise ValueError("Subject not found")

            timetable.subject_id = data["subject_id"]

        if "teacher_id" in data:
            if not TeacherRepository.get_by_id(data["teacher_id"]):
                raise ValueError("Teacher not found")

            timetable.teacher_id = data["teacher_id"]

        if "day_of_week" in data:
            day_of_week = data["day_of_week"].upper()

            if day_of_week not in TimetableService.ALLOWED_DAYS:
                raise ValueError("Invalid day of week")

            timetable.day_of_week = day_of_week

        if "start_time" in data:
            timetable.start_time = data["start_time"]

        if "end_time" in data:
            timetable.end_time = data["end_time"]

        if timetable.start_time >= timetable.end_time:
            raise ValueError(
                "Start time must be earlier than end time"
            )

        if "room_number" in data:
            timetable.room_number = data["room_number"]

        try:
            TimetableRepository.update()
            return timetable

        except Exception:
            TimetableRepository.rollback()
            raise

    @staticmethod
    def delete_timetable(timetable_id):
        timetable = TimetableService.get_timetable_by_id(
            timetable_id
        )

        try:
            TimetableRepository.delete(timetable)
            return timetable

        except Exception:
            TimetableRepository.rollback()
            raise