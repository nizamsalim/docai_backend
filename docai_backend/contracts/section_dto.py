from dataclasses import dataclass as d


@d
class SectionDTO:
    id: str
    title: str
    content: str
    order: int
    project_id: str

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "order": self.order,
            "projectId": self.project_id,
        }
