"""
Resume management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.resume import Resume

logger = structlog.get_logger()
router = APIRouter()

# Pydantic models
class ResumeResponse(BaseModel):
    id: str
    original_filename: str
    candidate_name: Optional[str]
    candidate_email: Optional[str]
    status: str
    created_at: str

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a resume file"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF, DOCX, and DOC files are allowed"
            )

        # Create resume record
        resume = Resume(
            user_id=current_user.id,
            original_filename=file.filename,
            file_path=f"uploads/{file.filename}",
            file_size=0,  # Will be updated after processing
            file_type=file.filename.split('.')[-1].lower(),
            status="pending"
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        logger.info(f"Resume uploaded: {resume.id} by user {current_user.id}")

        return {
            "id": resume.id,
            "filename": resume.original_filename,
            "status": resume.status
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload resume error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload resume"
        )

@router.get("/")
async def get_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """Get user's resumes"""
    try:
        resumes = db.query(Resume).filter(
            Resume.user_id == current_user.id
        ).offset(skip).limit(limit).all()

        return {
            "resumes": [
                {
                    "id": resume.id,
                    "original_filename": resume.original_filename,
                    "candidate_name": resume.candidate_name,
                    "candidate_email": resume.candidate_email,
                    "status": resume.status,
                    "created_at": resume.created_at.isoformat() if resume.created_at else None
                }
                for resume in resumes
            ],
            "total": len(resumes)
        }

    except Exception as e:
        logger.error(f"Get resumes error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get resumes"
        )

@router.get("/{resume_id}")
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific resume details"""
    try:
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        ).first()

        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        return {
            "id": resume.id,
            "original_filename": resume.original_filename,
            "candidate_name": resume.candidate_name,
            "candidate_email": resume.candidate_email,
            "candidate_phone": resume.candidate_phone,
            "candidate_location": resume.candidate_location,
            "summary": resume.summary,
            "skills": resume.skills,
            "experience_years": resume.experience_years,
            "education": resume.education,
            "work_experience": resume.work_experience,
            "certifications": resume.certifications,
            "status": resume.status,
            "confidence_score": resume.confidence_score,
            "created_at": resume.created_at.isoformat() if resume.created_at else None
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get resume error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get resume"
        ) 