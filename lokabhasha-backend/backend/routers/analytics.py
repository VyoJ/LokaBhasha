from typing import List
from backend.utils.models import Answer
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.utils.database import get_db

router = APIRouter()


@router.get("/admin-analytics", response_model=something)
def admin_analytics_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    # Call all SQL functions to get analytics data
    pass


@router.get("/user-analytics/{u_id}", response_model=something)
def user_analytics_endpoint(q_id: int, resp_id: int, db: Session = Depends(get_db)):
    # Call the user analytics SQL function here for the given user_id
    pass


@router.get("/user-progress/{u_id}", response_model=something)
def user_progress_endpoint(q_id: int, resp_id: int, db: Session = Depends(get_db)):
    # Call the user progress SQL procedure here for the given user_id
    pass
