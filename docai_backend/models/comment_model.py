from ..utils.db import db
from uuid import uuid4


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))

    content = db.Column(db.Text, nullable=False)

    section_id = db.Column(
        db.String(36), db.ForeignKey("sections.id", ondelete="CASCADE"), nullable=False
    )

    section = db.relationship("Section", back_populates="comments")
