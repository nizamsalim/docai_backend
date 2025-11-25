from pydantic import BaseModel, Field


class RefineSectionSchema(BaseModel):
    user_instruction: str = Field(alias="userInstruction")
    model_name: str = Field(default="gemini")


class UpdateSectionSchema(BaseModel):
    title: str | None = None
    content: str | None = None
