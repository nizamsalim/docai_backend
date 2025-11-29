from datetime import datetime
from uuid import uuid4
from ..utils.db import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(4), nullable=False)
    section_count = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    accessed_at = db.Column(db.DateTime, default=datetime.now)

    sections = db.relationship(
        "Section",
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="Section.order",
    )
