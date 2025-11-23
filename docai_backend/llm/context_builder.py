from ..repositories.project_repository import ProjectRepository
from ..repositories.section_repository import SectionRepository
from ..utils.exception import ResourceNotFoundError


class ContextBuilder:
    def __init__(
        self, project_repo: ProjectRepository, section_repo: SectionRepository
    ):
        self.project_repo = project_repo
        self.section_repo = section_repo

    def build(self, project_id: str, section_id: str | None = None, mode="None") -> str:
        # mode - none, section, full
        if mode == "none":
            return ""

        if mode == "section":
            section = self.section_repo.find_by_id(section_id)
            if section is None:
                raise ResourceNotFoundError(
                    message=f"Section with id: {section_id} not found"
                )
            return section.content

        if mode == "full":
            project = self.project_repo.find_by_id(project_id)
            parts = []
            for sec in project.sections:
                parts.append(f"section: {sec.title}\ncontent: {sec.content}")
            return "\n------------------\n".join(parts)

        return ""
