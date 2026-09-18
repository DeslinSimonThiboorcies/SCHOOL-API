from school.repositories.attendance_repository import AttendanceRepository
from school.repositories.students_repo import StudentRepository
from school.repositories.class_repository import ClassRepository
from school.models.attendance import Attendance


class AttendanceService:

    ALLOWED_STATUS = {
        "PRESENT",
        "ABSENT",
        "LATE",
        "LEAVE"
    }

    @staticmethod
    def create_attendance(data):
        student_id = data.get("student_id")
        class_id = data.get("class_id")
        attendance_date = data.get("attendance_date")
        status = data.get("status", "PRESENT").upper()

        student = StudentRepository.get_by_id(student_id)

        if not student:
            raise ValueError("Student not found")

        class_obj = ClassRepository.get_by_id(class_id)

        if not class_obj:
            raise ValueError("Class not found")

        if status not in AttendanceService.ALLOWED_STATUS:
            raise ValueError("Invalid attendance status")

        existing_attendance = (
            AttendanceRepository.get_by_student_and_date(
                student_id,
                attendance_date
            )
        )

        if existing_attendance:
            raise ValueError(
                "Attendance already marked for this student on this date"
            )

        attendance = Attendance(
            student_id=student_id,
            class_id=class_id,
            attendance_date=attendance_date,
            status=status
        )

        try:
            AttendanceRepository.create(attendance)
            AttendanceRepository.commit()
            return attendance

        except Exception:
            AttendanceRepository.rollback()
            raise

    @staticmethod
    def get_attendance_by_id(attendance_id):
        attendance = AttendanceRepository.get_by_id(attendance_id)

        if not attendance:
            raise ValueError("Attendance record not found")

        return attendance

    @staticmethod
    def get_all_attendance():
        return AttendanceRepository.get_all()

    @staticmethod
    def get_student_attendance(student_id):
        if not StudentRepository.get_by_id(student_id):
            raise ValueError("Student not found")

        return AttendanceRepository.get_by_student_id(student_id)

    @staticmethod
    def update_attendance(attendance_id, data):
        attendance = AttendanceService.get_attendance_by_id(
            attendance_id
        )

        if "status" in data:
            status = data["status"].upper()

            if status not in AttendanceService.ALLOWED_STATUS:
                raise ValueError("Invalid attendance status")

            attendance.status = status

        if "attendance_date" in data:
            attendance.attendance_date = data["attendance_date"]

        try:
            AttendanceRepository.update()
            return attendance

        except Exception:
            AttendanceRepository.rollback()
            raise

    @staticmethod
    def delete_attendance(attendance_id):
        attendance = AttendanceService.get_attendance_by_id(
            attendance_id
        )

        try:
            AttendanceRepository.delete(attendance)
            return attendance

        except Exception:
            AttendanceRepository.rollback()
            raise