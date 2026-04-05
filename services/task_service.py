from models.base import SessionLocal
from models.task import Task
from datetime import datetime


class TaskService:
    @staticmethod
    def create(data: dict):
        session = SessionLocal()
        try:
            task = Task(
                employee_id=data["employee_id"],
                titre=data["titre"],
                description=data.get("description", ""),
                priorite=data.get("priorite", "normale"),
                date_echeance=data.get("date_echeance"),
                statut="assigne"
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update_status(task_id, new_status):
        session = SessionLocal()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return None
            task.statut = new_status
            task.updated_at = datetime.now()
            if new_status == "en_cours" and not task.date_debut:
                task.date_debut = datetime.now()
            elif new_status in ("termine", "livre"):
                task.date_fin = datetime.now()
            session.commit()
            session.refresh(task)
            return task
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all(employee_id=None, statut=None):
        session = SessionLocal()
        try:
            q = session.query(Task)
            if employee_id:
                q = q.filter(Task.employee_id == employee_id)
            if statut:
                q = q.filter(Task.statut == statut)
            return q.order_by(Task.created_at.desc()).all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(task_id):
        session = SessionLocal()
        try:
            return session.query(Task).filter(Task.id == task_id).first()
        finally:
            session.close()

    @staticmethod
    def delete(task_id):
        session = SessionLocal()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_employee_stats(employee_id, month=None, year=None):
        session = SessionLocal()
        try:
            q = session.query(Task).filter(Task.employee_id == employee_id)
            if month and year:
                from sqlalchemy import extract
                q = q.filter(
                    extract('month', Task.created_at) == month,
                    extract('year', Task.created_at) == year
                )
            tasks = q.all()
            total = len(tasks)
            completed = sum(1 for t in tasks if t.statut in ("termine", "livre"))
            in_progress = sum(1 for t in tasks if t.statut == "en_cours")
            cancelled = sum(1 for t in tasks if t.statut == "annule")
            overdue = sum(1 for t in tasks if t.date_echeance and t.statut not in ("termine", "livre", "annule") and t.date_echeance < datetime.now().date())

            return {
                "total": total,
                "completed": completed,
                "in_progress": in_progress,
                "cancelled": cancelled,
                "overdue": overdue,
                "completion_rate": round((completed / total * 100) if total > 0 else 0, 1)
            }
        finally:
            session.close()

    @staticmethod
    def count_active():
        session = SessionLocal()
        try:
            return session.query(Task).filter(Task.statut.in_(["assigne", "en_cours"])).count()
        finally:
            session.close()
