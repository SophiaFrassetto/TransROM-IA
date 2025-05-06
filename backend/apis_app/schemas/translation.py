from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TranslationOptionsBase(BaseModel):
    """Base schema for translation options."""

    text: bool = True
    audio: bool = False
    image: bool = False


class TranslationJobBase(BaseModel):
    """Base schema for translation jobs."""

    target_language: str
    translation_options: TranslationOptionsBase


class TranslationJobCreate(TranslationJobBase):
    """Schema for creating a translation job."""

    pass


class TranslationJobUpdate(BaseModel):
    """Schema for updating a translation job."""

    status: Optional[str] = None
    temp_file_path: Optional[str] = None


class TranslationJob(TranslationJobBase):
    """Schema for a complete translation job."""

    id: int
    user_id: int
    original_filename: str
    file_size: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
