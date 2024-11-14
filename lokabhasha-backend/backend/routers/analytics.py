from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from backend.utils.database import get_db
from backend.schemas.analytics import (
    AdminAnalytics,
    UserAnalytics,
    UserProgress,
    ModuleProgress,
    OverallProgress,
)

router = APIRouter()


@router.get("/admin-analytics", response_model=AdminAnalytics)
def admin_analytics_endpoint(db: Session = Depends(get_db)):
    """Get admin analytics including daily responses, most active language, etc."""
    try:
        results = {}

        results["daily_responses"] = db.execute(
            text("SELECT GetDailyResponseCount(CURDATE())")
        ).scalar()

        results["most_active_language"] = db.execute(
            text("SELECT GetMostActiveLanguage()")
        ).scalar()

        results["active_language_responses"] = db.execute(
            text("SELECT GetMostActiveLanguageCount()")
        ).scalar()

        results["today_signups"] = db.execute(text("SELECT GetTodaySignups()")).scalar()

        results["overall_avg_latency"] = float(
            db.execute(text("SELECT GetOverallAverageLatency()")).scalar() or 0
        )

        return AdminAnalytics(**results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user-analytics/{u_id}", response_model=UserAnalytics)
def user_analytics_endpoint(
    u_id: int, target_date: date = None, db: Session = Depends(get_db)
):
    """Get user analytics for responses submitted on a specific date."""
    try:
        if target_date is None:
            target_date = date.today()

        result = db.execute(
            text("SELECT GetUserDailyAnalytics(:user_id, :target_date)"),
            {"user_id": u_id, "target_date": target_date},
        ).scalar()

        parts = result.split(", ")
        analytics = {
            "total_responses": int(parts[0].split(": ")[1]),
            "correct_responses": int(parts[1].split(": ")[1]),
            "wrong_responses": int(parts[2].split(": ")[1]),
        }

        return UserAnalytics(**analytics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Modify the SQL query in user_progress_endpoint to handle NULL cases
@router.get("/user-progress/{u_id}", response_model=UserProgress)
def user_progress_endpoint(u_id: int, db: Session = Depends(get_db)):
    try:
        # Update the percentage calculation to handle zero questions
        module_results = db.execute(
            text(
                "SELECT m.m_id, m.lang_id, l.name AS language_name, m.name AS module_name, "
                "COUNT(DISTINCT q.q_id) AS total_questions, "
                "COUNT(DISTINCT a.q_id) AS answered_questions, "
                "CASE WHEN COUNT(DISTINCT a.q_id) = COUNT(DISTINCT q.q_id) THEN 'Completed' "
                "WHEN COUNT(DISTINCT a.q_id) > 0 THEN 'In Progress' "
                "ELSE 'Not Started' END AS module_status, "
                "CASE WHEN COUNT(DISTINCT q.q_id) = 0 THEN 0 "
                "ELSE ROUND((COUNT(DISTINCT a.q_id) / NULLIF(COUNT(DISTINCT q.q_id), 0)) * 100, 2) "
                "END AS completion_percentage "
                "FROM Modules m "
                "JOIN Languages l ON m.lang_id = l.lang_id "
                "LEFT JOIN Questions q ON m.m_id = q.m_id "
                "LEFT JOIN Answers a ON q.q_id = a.q_id AND a.u_id = :user_id "
                "GROUP BY m.m_id, m.lang_id, l.name, m.name "
                "ORDER BY l.name, m.name"
            ),
            {"user_id": u_id},
        ).all()

        # Add null checks when creating ModuleProgress objects
        module_progress = [
            ModuleProgress(
                module_id=row.m_id,
                lang_id=row.lang_id,
                language_name=row.language_name,
                module_name=row.module_name,
                total_questions=row.total_questions or 0,
                answered_questions=row.answered_questions or 0,
                module_status=row.module_status,
                completion_percentage=float(row.completion_percentage or 0),
            )
            for row in module_results
        ]

        # Add null checks for overall progress
        overall = db.execute(
            text(
                "SELECT COUNT(DISTINCT q.q_id) AS total_questions, "
                "COUNT(DISTINCT a.q_id) AS completed_questions, "
                "CASE WHEN COUNT(DISTINCT q.q_id) = 0 THEN 0 "
                "ELSE ROUND((COUNT(DISTINCT a.q_id) / NULLIF(COUNT(DISTINCT q.q_id), 0)) * 100, 2) "
                "END AS overall_completion_percentage "
                "FROM Questions q "
                "LEFT JOIN Answers a ON q.q_id = a.q_id AND a.u_id = :user_id"
            ),
            {"user_id": u_id},
        ).first()

        overall_progress = OverallProgress(
            total_questions=overall.total_questions or 0,
            completed_questions=overall.completed_questions or 0,
            overall_completion_percentage=float(
                overall.overall_completion_percentage or 0
            ),
        )

        return UserProgress(
            module_progress=module_progress, overall_progress=overall_progress
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
