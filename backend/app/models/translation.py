from datetime import datetime, timezone

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class TranslationJob(BaseModel):
    """Model for storing translation job information."""

    __tablename__ = "translation_jobs"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)  # in bytes
    target_language: Mapped[str] = mapped_column(String, nullable=False)
    translation_options: Mapped[dict] = mapped_column(
        JSON, nullable=False
    )  # Store selected options
    status: Mapped[str] = mapped_column(
        String, nullable=False, default="pending"
    )  # pending, processing, completed, failed
    temp_file_path: Mapped[str | None] = mapped_column(
        String, nullable=True
    )  # For temporary storage reference

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)
        if not self.updated_at:
            self.updated_at = datetime.now(timezone.utc)

    # Relationships
    user = relationship("User", back_populates="translation_jobs")
