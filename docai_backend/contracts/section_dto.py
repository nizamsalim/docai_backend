from dataclasses import dataclass as d


@d
class RefinementDTO:
    id: str
    prompt: str
    rating: str | None
    section_id: str
    before_content: str
    after_content: str

    def to_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "rating": self.rating,
            "sectionId": self.section_id,
            "beforeContent": self.before_content,
            "afterContent": self.after_content,
        }


@d
class CommentDTO:
    id: str
    section_id: str
    content: str

    def to_dict(self):
        return {"id": self.id, "sectionId": self.section_id, "content": self.content}


@d
class SectionDTO:
    id: str
    title: str
    content: str
    order: int
    project_id: str
    refinements: list[RefinementDTO] | None = None
    comments: list[CommentDTO] | None = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "order": self.order,
            "projectId": self.project_id,
            "refinements": (
                [r.to_dict() for r in self.refinements] if self.refinements else []
            ),
            "comments": [c.to_dict() for c in self.comments] if self.comments else [],
        }
