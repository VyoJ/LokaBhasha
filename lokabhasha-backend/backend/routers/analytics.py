# from typing import List
# from backend.utils.models import Answer
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from backend.utils.database import get_db

# router = APIRouter()


# @router.get("/admin-analytics", response_model=something)
# def admin_analytics_endpoint(
#     skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
# ):
#     # Call all SQL functions to get analytics data
#     pass


# @router.get("/user-analytics/{u_id}", response_model=something)
# def user_analytics_endpoint(q_id: int, resp_id: int, db: Session = Depends(get_db)):
#     # Call the user analytics SQL function here for the given user_id
#     pass


# @router.get("/user-progress/{u_id}", response_model=something)
# def user_progress_endpoint(q_id: int, resp_id: int, db: Session = Depends(get_db)):
#     # Call the user progress SQL procedure here for the given user_id
#     pass




from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from backend.utils.database import get_db
from backend.schemas.analytics import AdminAnalytics, UserAnalytics, UserProgress, ModuleProgress, OverallProgress

router = APIRouter()

@router.get("/admin-analytics", response_model=AdminAnalytics)
def admin_analytics_endpoint(db: Session = Depends(get_db)):
    """Get admin analytics including daily responses, most active language, etc."""
    try:
        results = {}
        
        # Execute all analytics functions
        results["daily_responses"] = db.execute(
            text("SELECT GetDailyResponseCount(CURDATE())")
        ).scalar()
        
        results["most_active_language"] = db.execute(
            text("SELECT GetMostActiveLanguage()")
        ).scalar()
        
        results["active_language_responses"] = db.execute(
            text("SELECT GetMostActiveLanguageCount()")
        ).scalar()
        
        results["today_signups"] = db.execute(
            text("SELECT GetTodaySignups()")
        ).scalar()
        
        results["overall_avg_latency"] = float(db.execute(
            text("SELECT GetOverallAverageLatency()")
        ).scalar() or 0)
        
        return AdminAnalytics(**results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-analytics/{u_id}", response_model=UserAnalytics)
def user_analytics_endpoint(
    u_id: int,
    target_date: date = None,
    db: Session = Depends(get_db)
):
    """Get user analytics for responses submitted on a specific date."""
    try:
        if target_date is None:
            target_date = date.today()
            
        result = db.execute(
            text("SELECT GetUserDailyAnalytics(:user_id, :target_date)"),
            {"user_id": u_id, "target_date": target_date}
        ).scalar()
        
        # Parse "Total: X, Correct: Y, Wrong: Z"
        parts = result.split(", ")
        analytics = {
            "total_responses": int(parts[0].split(": ")[1]),
            "correct_responses": int(parts[1].split(": ")[1]),
            "wrong_responses": int(parts[2].split(": ")[1])
        }
        
        return UserAnalytics(**analytics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-progress/{u_id}", response_model=UserProgress)
def user_progress_endpoint(u_id: int, db: Session = Depends(get_db)):
    """Get user's progress across all modules."""
    try:
        # Execute GetUserProgress procedure
        result = db.execute(text("CALL GetUserProgress(:user_id)"), {"user_id": u_id})
        
        # First result set: module progress
        module_results = result.fetchall()
        module_progress = []
        
        for row in module_results:
            module_progress.append(ModuleProgress(
                lang_id=row.lang_id,
                language_name=row.language_name,
                module_name=row.module_name,
                total_questions=row.total_questions,
                answered_questions=row.answered_questions,
                module_status=row.module_status,
                completion_percentage=float(row.completion_percentage)
            ))
            
        # Second result set: overall progress
        result = result.nextset()
        if result:
            overall = result.fetchone()
            overall_progress = OverallProgress(
                total_questions=overall.total_questions,
                completed_questions=overall.completed_questions,
                overall_completion_percentage=float(overall.overall_completion_percentage)
            )
        
        return UserProgress(
            module_progress=module_progress,
            overall_progress=overall_progress
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))