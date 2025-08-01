"""
Job matching API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.match import Match
from app.models.resume import Resume
from app.models.job import Job

logger = structlog.get_logger()
router = APIRouter()

# Pydantic models
class MatchResponse(BaseModel):
    id: str
    resume_id: str
    job_id: str
    overall_score: float
    skills_score: Optional[float]
    experience_score: Optional[float]
    education_score: Optional[float]
    culture_score: Optional[float]
    created_at: str

@router.post("/resume/{resume_id}/job/{job_id}")
async def create_match(
    resume_id: str,
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a match between resume and job"""
    try:
        # Check if resume and job exist and belong to user
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        ).first()
        
        job = db.query(Job).filter(
            Job.id == job_id,
            Job.user_id == current_user.id
        ).first()

        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )

        # Check if match already exists
        existing_match = db.query(Match).filter(
            Match.resume_id == resume_id,
            Match.job_id == job_id,
            Match.user_id == current_user.id
        ).first()

        if existing_match:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Match already exists"
            )

        # Create match (simplified scoring for now)
        match = Match(
            user_id=current_user.id,
            resume_id=resume_id,
            job_id=job_id,
            overall_score=0.75,  # Placeholder score
            skills_score=0.8,
            experience_score=0.7,
            education_score=0.8,
            culture_score=0.6
        )

        db.add(match)
        db.commit()
        db.refresh(match)

        logger.info(f"Match created: {match.id} by user {current_user.id}")

        return {
            "id": match.id,
            "resume_id": match.resume_id,
            "job_id": match.job_id,
            "overall_score": match.overall_score,
            "status": "created"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create match error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create match"
        )

@router.get("/")
async def get_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """Get user's matches"""
    try:
        matches = db.query(Match).filter(
            Match.user_id == current_user.id
        ).offset(skip).limit(limit).all()

        return {
            "matches": [
                {
                    "id": match.id,
                    "resume_id": match.resume_id,
                    "job_id": match.job_id,
                    "overall_score": match.overall_score,
                    "skills_score": match.skills_score,
                    "experience_score": match.experience_score,
                    "education_score": match.education_score,
                    "culture_score": match.culture_score,
                    "created_at": match.created_at.isoformat() if match.created_at else None
                }
                for match in matches
            ],
            "total": len(matches)
        }

    except Exception as e:
        logger.error(f"Get matches error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get matches"
        )

@router.get("/{match_id}")
async def get_match(
    match_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific match details"""
    try:
        match = db.query(Match).filter(
            Match.id == match_id,
            Match.user_id == current_user.id
        ).first()

        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match not found"
            )

        return {
            "id": match.id,
            "resume_id": match.resume_id,
            "job_id": match.job_id,
            "overall_score": match.overall_score,
            "skills_score": match.skills_score,
            "experience_score": match.experience_score,
            "education_score": match.education_score,
            "culture_score": match.culture_score,
            "skill_matches": match.skill_matches,
            "missing_skills": match.missing_skills,
            "experience_gap": match.experience_gap,
            "match_explanation": match.match_explanation,
            "strengths": match.strengths,
            "weaknesses": match.weaknesses,
            "recommendations": match.recommendations,
            "bias_score": match.bias_score,
            "fairness_adjustment": match.fairness_adjustment,
            "created_at": match.created_at.isoformat() if match.created_at else None
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get match error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get match"
        ) 