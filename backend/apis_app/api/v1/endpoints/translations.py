import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apis_app.database.session import get_async_session
from apis_app.models.translation import TranslationJob
from apis_app.models.user import User
from apis_app.schemas.translation import TranslationJob as TranslationJobSchema
from apis_app.schemas.translation import TranslationOptionsBase
from apis_app.services.auth import get_current_user

router = APIRouter()

@router.post("/upload", response_model=TranslationJobSchema)
async def upload_rom(
    file: UploadFile = File(...),
    target_language: str = Form(...),
    translation_options: str = Form(...),  # JSON string
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
) -> TranslationJobSchema:
    """
    Upload a ROM file for translation.

    The file will be temporarily stored and a translation job will be created.
    The actual translation process will be handled asynchronously.

    Args:
        file: The ROM file to translate
        target_language: The target language for translation
        translation_options: JSON string of translation options
        db: Database session
        current_user: Current authenticated user

    Returns:
        TranslationJobSchema: Created translation job information

    Raises:
        HTTPException: If file upload fails or file type is not supported
    """
    # Validate file size (e.g., max 100MB)
    max_size = 100 * 1024 * 1024  # 100MB
    if file.size > max_size:
        raise HTTPException(status_code=400, detail="File too large")

    # Validate file extension
    allowed_extensions = {".gba", ".gbc", ".gb"}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not supported")

    try:
        # Parse and validate translation options
        try:
            options_dict = json.loads(translation_options)
            validated_options = TranslationOptionsBase(**options_dict)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid translation options format: {e!s}"
            ) from e

        # Create temporary file
        with NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            # Copy uploaded file to temporary location
            shutil.copyfileobj(file.file, temp_file)

            # Get current timestamp
            now = datetime.now(timezone.utc)

            # Create translation job
            translation_job = TranslationJob(
                user_id=current_user.id,
                original_filename=file.filename,
                file_size=file.size,
                target_language=target_language,
                translation_options=validated_options.model_dump(),  # Convert to dict
                status="pending",
                temp_file_path=temp_file.name,
                created_at=now,
                updated_at=now
            )

            db.add(translation_job)
            await db.commit()
            await db.refresh(translation_job)

            return translation_job
    except Exception as e:
        # Clean up temporary file if it exists
        if "temp_file" in locals():
            os.unlink(temp_file.name)
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/jobs", response_model=List[TranslationJobSchema])
async def get_translation_jobs(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> List[TranslationJobSchema]:
    """
    Get all translation jobs for the current user.

    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List[TranslationJobSchema]: List of translation jobs
    """
    query = (
        select(TranslationJob)
        .filter(TranslationJob.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()
