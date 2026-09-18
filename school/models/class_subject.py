from school.extensison.db import db


class ClassSubject(db.Model):
    __tablename__ = "class_subjects"

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
        nullable=True
    )

    class_ref = db.relationship(
        "ClassModel",
        backref="class_subjects"
    )

    subject_ref = db.relationship(
        "Subject",
        backref="class_subjects"
    )

    teacher_ref = db.relationship(
        "Teacher",
        backref="class_subjects"
    )

    def __repr__(self):
        return f"<ClassSubject class={self.class_id} subject={self.subject_id}>"