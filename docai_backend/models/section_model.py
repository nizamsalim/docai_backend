from ..utils.db import db
from uuid import uuid4


class Section(db.Model):
    __tablename__ = "sections"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False)

    project_id = db.Column(
        db.String(36), db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )

    project = db.relationship("Project", back_populates="sections")

    refinements = db.relationship(
        "Refinement",
        back_populates="section",
        cascade="all, delete-orphan",
    )

    comments = db.relationship(
        "Comment", back_populates="section", cascade="all, delete-orphan"
    )
