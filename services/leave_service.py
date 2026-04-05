from models.base import SessionLocal
from models.leave import Leave
from datetime import datetime


class LeaveService:
    @staticmethod
    def create(data: dict):
        session = SessionLocal()
        try:
            leave = Leave(
                employee_id=data["employee_id"],
                type_conge=data.get("type_conge", "annuel"),
                date_debut=data["date_debut"],
                date_fin=data["date_fin"],
                motif=data.get("motif", ""),
                statut="en_attente"
            )
            session.add(leave)
            session.commit()
            session.refresh(leave)
            return leave
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def approve(leave_id, commentaire=""):
        session = SessionLocal()
        try:
            leave = session.query(Leave).filter(Leave.id == leave_id).first()
            if leave:
                leave.statut = "approuve"
                leave.commentaire = commentaire
                leave.updated_at = datetime.now()
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def reject(leave_id, commentaire=""):
        session = SessionLocal()
        try:
            leave = session.query(Leave).filter(Leave.id == leave_id).first()
            if leave:
                leave.statut = "refuse"
                leave.commentaire = commentaire
                leave.updated_at = datetime.now()
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all(employee_id=None, statut=None):
        session = SessionLocal()
        try:
            q = session.query(Leave)
            if employee_id:
                q = q.filter(Leave.employee_id == employee_id)
            if statut:
                q = q.filter(Leave.statut == statut)
            return q.order_by(Leave.created_at.desc()).all()
        finally:
            session.close()

    @staticmethod
    def get_pending():
        return LeaveService.get_all(statut="en_attente")

    @staticmethod
    def count_pending():
        session = SessionLocal()
        try:
            return session.query(Leave).filter(Leave.statut == "en_attente").count()
        finally:
            session.close()
