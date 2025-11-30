from pydantic import BaseModel, Field


class SectionSchema(BaseModel):
    order: int
    title: str


class GenerateSectionsSchema(BaseModel):
    title: str
    type: str


class CreateProjectSchema(BaseModel):
    title: str
    type: str
    sections: list[SectionSchema]


class UpdateProjectSchema(BaseModel):
    title: str
