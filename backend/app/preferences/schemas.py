from pydantic import BaseModel, ConfigDict


class PreferencesBase(BaseModel):
    favorite_topics: list[str] = []
    blocked_topics: list[str] = []
    preferred_sources: list[str] = []


class PreferencesUpdate(PreferencesBase):
    pass


class PreferencesResponse(PreferencesBase):
    model_config = ConfigDict(from_attributes=True)