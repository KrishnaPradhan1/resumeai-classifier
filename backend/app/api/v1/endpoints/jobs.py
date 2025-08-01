"""
Job management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.job import Job

logger = structlog.get_logger()
router = APIRouter()

# Pydantic models
class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    requirements: List[str]
    location: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = "full-time"  # full-time, part-time, contract, etc.
    experience_level: Optional[str] = None  # entry, mid, senior, etc.

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    is_active: Optional[bool] = None

@router.post("/")
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job posting"""
    try:
        job = Job(
            user_id=current_user.id,
            title=job_data.title,
            company=job_data.company,
            description=job_data.description,
            requirements=job_data.requirements,
            location=job_data.location,
            salary_range=job_data.salary_range,
            job_type=job_data.job_type,
            experience_level=job_data.experience_level
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        logger.info(f"Job created: {job.id} by user {current_user.id}")
        
        return {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "status": "created"
        }
        
    except Exception as e:
        logger.error(f"Create job error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create job"
        )

@router.get("/")
async def get_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    active_only: bool = True
):
    """Get user's job postings"""
    try:
        query = db.query(Job).filter(Job.user_id == current_user.id)
        
        if active_only:
            query = query.filter(Job.is_active == True)
        
        jobs = query.offset(skip).limit(limit).all()
        
        return {
            "jobs": [
                {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "job_type": job.job_type,
                    "experience_level": job.experience_level,
                    "is_active": job.is_active,
                    "created_at": job.created_at,
                    "updated_at": job.updated_at
                }
                for job in jobs
            ],
            "total": len(jobs)
        }
        
    except Exception as e:
        logger.error(f"Get jobs error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get jobs"
        )

@router.get("/{job_id}")
async def get_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific job details"""
    try:
        job = db.query(Job).filter(
            Job.id == job_id,
            Job.user_id == current_user.id
        ).first()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        return {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "requirements": job.requirements,
            "location": job.location,
            "salary_range": job.salary_range,
            "job_type": job.job_type,
            "experience_level": job.experience_level,
            "is_active": job.is_active,
            "created_at": job.created_at,
            "updated_at": job.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get job error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job"
        )

@router.put("/{job_id}")
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a job posting"""
    try:
        job = db.query(Job).filter(
            Job.id == job_id,
            Job.user_id == current_user.id
        ).first()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Update fields
        update_data = job_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        db.commit()
        db.refresh(job)
        
        logger.info(f"Job updated: {job_id} by user {current_user.id}")
        
        return {
            "id": job.id,
            "title": job.title,
            "status": "updated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update job error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update job"
        )

@router.delete("/{job_id}")
async def delete_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a job posting"""
    try:
        job = db.query(Job).filter(
            Job.id == job_id,
            Job.user_id == current_user.id
        ).first()
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        db.delete(job)
        db.commit()
        
        logger.info(f"Job deleted: {job_id} by user {current_user.id}")
        
        return {"message": "Job deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete job error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job"
        ) 