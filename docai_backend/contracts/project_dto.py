from dataclasses import dataclass as d
from datetime import datetime
from .section_dto import SectionDTO


@d
class ProjectDTO:
    title: str
    type: str
    section_count: int
    id: str
    created_at: datetime
    updated_at: datetime
    accessed_at: datetime
    sections: list[SectionDTO] | None = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "sectionCount": self.section_count,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "accessedAt": self.accessed_at.isoformat(),
            "sections": (
                [s.to_dict() for s in self.sections]
                if self.sections is not None
                else None
            ),
        }
