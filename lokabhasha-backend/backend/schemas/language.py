from pydantic import BaseModel, ConfigDict


class LanguageBase(BaseModel):
    name: str


class LanguageUpdate(LanguageBase):
    name: str | None = None


class LanguageInDB(LanguageBase):
    model_config = ConfigDict(from_attributes=True)
    lang_id: int
