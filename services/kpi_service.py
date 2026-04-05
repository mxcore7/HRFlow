from models.base import SessionLocal
from models.kpi import KPI
from services.attendance_service import AttendanceService
from services.task_service import TaskService
from config import load_config
from datetime import date


class KPIService:
    @staticmethod
    def calculate(employee_id, month, year):
        config = load_config()
        kpi_config = config.get("kpi", {})
        weight_tasks = kpi_config.get("weight_tasks", 40)
        weight_attendance = kpi_config.get("weight_attendance", 30)
        weight_punctuality = kpi_config.get("weight_punctuality", 30)

        task_stats = TaskService.get_employee_stats(employee_id, month, year)
        att_stats = AttendanceService.get_monthly_stats(employee_id, month, year)

        score_taches = task_stats["completion_rate"]

        import calendar
        work_days = 0
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            d = date(year, month, day)
            if d.weekday() < 5:
                work_days += 1

        score_presence = min(100, (att_stats["total_days"] / max(work_days, 1)) * 100)

        if att_stats["total_days"] > 0:
            days_on_time = att_stats["total_days"] - att_stats["days_late"]
            score_ponctualite = (days_on_time / att_stats["total_days"]) * 100
        else:
            score_ponctualite = 0.0

        score_global = (
            score_taches * (weight_tasks / 100) +
            score_presence * (weight_attendance / 100) +
            score_ponctualite * (weight_punctuality / 100)
        )

        session = SessionLocal()
        try:
            existing = session.query(KPI).filter(
                KPI.employee_id == employee_id,
                KPI.mois == month,
                KPI.annee == year
            ).first()

            if existing:
                existing.score_taches = round(score_taches, 2)
                existing.score_presence = round(score_presence, 2)
                existing.score_ponctualite = round(score_ponctualite, 2)
                existing.score_global = round(score_global, 2)
                session.commit()
                session.refresh(existing)
                return existing
            else:
                kpi = KPI(
                    employee_id=employee_id,
                    mois=month,
                    annee=year,
                    score_taches=round(score_taches, 2),
                    score_presence=round(score_presence, 2),
                    score_ponctualite=round(score_ponctualite, 2),
                    score_global=round(score_global, 2)
                )
                session.add(kpi)
                session.commit()
                session.refresh(kpi)
                return kpi
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_employee_kpi(employee_id, month=None, year=None):
        session = SessionLocal()
        try:
            q = session.query(KPI).filter(KPI.employee_id == employee_id)
            if month:
                q = q.filter(KPI.mois == month)
            if year:
                q = q.filter(KPI.annee == year)
            return q.order_by(KPI.annee.desc(), KPI.mois.desc()).all()
        finally:
            session.close()

    @staticmethod
    def get_latest(employee_id):
        session = SessionLocal()
        try:
            return session.query(KPI).filter(
                KPI.employee_id == employee_id
            ).order_by(KPI.annee.desc(), KPI.mois.desc()).first()
        finally:
            session.close()
