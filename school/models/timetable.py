from school.extensison.db import db


class Timetable(db.Model):
    __tablename__ = "timetable"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    class_id = db.Column(
        db.Integer,
        db.ForeignKey("class_model.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher_profile.id"),
        nullable=False
    )

    day_of_week = db.Column(
        db.String(20),
        nullable=False
    )

    start_time = db.Column(
        db.Time,
        nullable=False
    )

    end_time = db.Column(
        db.Time,
        nullable=False
    )

    room_number = db.Column(
        db.String(20),
        nullable=True
    )

    class_ref = db.relationship(
        "ClassModel",
        backref="timetable_entries"
    )

    subject_ref = db.relationship(
        "Subject",
        backref="timetable_entries"
    )

    teacher_ref = db.relationship(
        "Teacher",
        backref="timetable_entries"
    )

    def __repr__(self):
        return f"<Timetable class={self.class_id} day={self.day_of_week}>"