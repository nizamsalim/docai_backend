from pydantic import BaseModel,field_validator

class SectionSchema(BaseModel):
    order:int
    title:str

class CreateProjectSchema(BaseModel):
    title:str
    type:str
    sections:list[SectionSchema]
