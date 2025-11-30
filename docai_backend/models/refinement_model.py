from ..utils.db import db
from uuid import uuid4


class Refinement(db.Model):
    __tablename__ = "refinements"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))

    prompt = db.Column(db.Text, nullable=False)
    rating = db.Column(db.String(8), nullable=True)

    model = db.Column(db.String(16), nullable=True)

    before_content = db.Column(db.Text, nullable=False)
    after_content = db.Column(db.Text, nullable=False)

    section_id = db.Column(
        db.String(36), db.ForeignKey("sections.id", ondelete="CASCADE"), nullable=False
    )

    section = db.relationship("Section", back_populates="refinements")
