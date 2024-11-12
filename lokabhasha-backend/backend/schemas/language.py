from pydantic import BaseModel


class LanguageBase(BaseModel):
    name: str


class LanguageUpdate(LanguageBase):
    name: str | None = None


class LanguageInDB(LanguageBase):
    lang_id: int

    class Config:
        from_attributes = True
