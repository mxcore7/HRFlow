from models.base import SessionLocal
from models.attendance import Attendance
from config import load_config
from datetime import datetime, date, timedelta


class AttendanceService:
    @staticmethod
    def check_in(employee_id):
        session = SessionLocal()
        try:
            today = date.today()
            existing = session.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.date == today,
                Attendance.heure_depart == None
            ).first()

            if existing:
                return None, "already_checked_in"

            config = load_config()
            now = datetime.now()
            work_start = now.replace(
                hour=config.get("work_start_hour", 8),
                minute=config.get("work_start_minute", 0),
                second=0, microsecond=0
            )

            retard = 0.0
            if now > work_start:
                retard = (now - work_start).total_seconds() / 60.0

            att = Attendance(
                employee_id=employee_id,
                date=today,
                heure_arrivee=now,
                retard_minutes=max(0, retard),
                statut="present"
            )
            session.add(att)
            session.commit()
            session.refresh(att)
            return att, "checked_in"
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def check_out(employee_id):
        session = SessionLocal()
        try:
            today = date.today()
            att = session.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.date == today,
                Attendance.heure_depart == None
            ).first()

            if not att:
                return None, "not_checked_in"

            now = datetime.now()
            att.heure_depart = now
            if att.heure_arrivee:
                delta = (now - att.heure_arrivee).total_seconds() / 3600.0
                att.duree_travail = round(delta, 2)

            session.commit()
            session.refresh(att)
            return att, "checked_out"
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def smart_pointage(employee_id):
        session = SessionLocal()
        try:
            today = date.today()
            open_att = session.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.date == today,
                Attendance.heure_depart == None
            ).first()

            if open_att:
                session.close()
                return AttendanceService.check_out(employee_id)
            else:
                session.close()
                return AttendanceService.check_in(employee_id)
        except Exception:
            session.close()
            return AttendanceService.check_in(employee_id)

    @staticmethod
    def get_history(employee_id=None, start_date=None, end_date=None):
        session = SessionLocal()
        try:
            q = session.query(Attendance)
            if employee_id:
                q = q.filter(Attendance.employee_id == employee_id)
            if start_date:
                q = q.filter(Attendance.date >= start_date)
            if end_date:
                q = q.filter(Attendance.date <= end_date)
            return q.order_by(Attendance.date.desc()).all()
        finally:
            session.close()

    @staticmethod
    def get_today(employee_id=None):
        session = SessionLocal()
        try:
            q = session.query(Attendance).filter(Attendance.date == date.today())
            if employee_id:
                q = q.filter(Attendance.employee_id == employee_id)
            return q.all()
        finally:
            session.close()

    @staticmethod
    def get_monthly_stats(employee_id, month, year):
        session = SessionLocal()
        try:
            start = date(year, month, 1)
            if month == 12:
                end = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end = date(year, month + 1, 1) - timedelta(days=1)

            records = session.query(Attendance).filter(
                Attendance.employee_id == employee_id,
                Attendance.date >= start,
                Attendance.date <= end
            ).all()

            total_days = len(records)
            total_hours = sum(r.duree_travail or 0 for r in records)
            total_retard = sum(r.retard_minutes or 0 for r in records)
            days_late = sum(1 for r in records if (r.retard_minutes or 0) > 0)

            return {
                "total_days": total_days,
                "total_hours": round(total_hours, 2),
                "total_retard": round(total_retard, 2),
                "days_late": days_late
            }
        finally:
            session.close()

    @staticmethod
    def count_today():
        session = SessionLocal()
        try:
            return session.query(Attendance).filter(Attendance.date == date.today()).count()
        finally:
            session.close()
