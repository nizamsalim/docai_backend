from pydantic import BaseModel, Field
from pydantic.alias_generators import to_snake


class RefineSectionSchema(BaseModel):
    user_instruction: str = Field(alias="userInstruction")
    model_name: str = Field(default="gemini")
