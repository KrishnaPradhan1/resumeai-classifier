"""
User management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import structlog

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

logger = structlog.get_logger()
router = APIRouter()

# Pydantic models
class UserProfile(BaseModel):
    id: str
    email: str
    full_name: str
    company: str
    role: str
    is_active: bool
    created_at: str

@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    try:
        return {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "company": current_user.company,
            "role": current_user.role,
            "phone": current_user.phone,
            "location": current_user.location,
            "bio": current_user.bio,
            "is_active": current_user.is_active,
            "is_verified": current_user.is_verified,
            "subscription_plan": current_user.subscription_plan,
            "monthly_uploads": current_user.monthly_uploads,
            "current_month_uploads": current_user.current_month_uploads,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "last_login_at": current_user.last_login_at.isoformat() if current_user.last_login_at else None
        }

    except Exception as e:
        logger.error(f"Get user profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )

@router.put("/profile")
async def update_user_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    try:
        # Update allowed fields
        allowed_fields = ["full_name", "company", "phone", "location", "bio"]
        update_data = {k: v for k, v in profile_data.items() if k in allowed_fields}
        
        for field, value in update_data.items():
            setattr(current_user, field, value)

        db.commit()
        db.refresh(current_user)

        logger.info(f"User profile updated: {current_user.id}")

        return {
            "message": "Profile updated successfully",
            "user": {
                "id": current_user.id,
                "full_name": current_user.full_name,
                "company": current_user.company,
                "phone": current_user.phone,
                "location": current_user.location,
                "bio": current_user.bio
            }
        }

    except Exception as e:
        logger.error(f"Update user profile error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        ) 