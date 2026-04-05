from models.base import SessionLocal
from models.employee import Employee
from datetime import datetime
import uuid


class EmployeeService:
    @staticmethod
    def generate_matricule():
        return f"EMP-{uuid.uuid4().hex[:6].upper()}"

    @staticmethod
    def create(data: dict):
        session = SessionLocal()
        try:
            emp = Employee(
                matricule=data.get("matricule") or EmployeeService.generate_matricule(),
                nom=data["nom"],
                prenom=data["prenom"],
                poste=data.get("poste", ""),
                departement=data.get("departement", ""),
                telephone=data.get("telephone", ""),
                email=data.get("email", ""),
                salaire_base=data.get("salaire_base", 0.0),
                photo=data.get("photo"),
                date_embauche=data.get("date_embauche", datetime.now()),
            )
            session.add(emp)
            session.commit()
            session.refresh(emp)
            return emp
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all(active_only=True):
        session = SessionLocal()
        try:
            q = session.query(Employee)
            if active_only:
                q = q.filter(Employee.actif == True)
            return q.order_by(Employee.nom).all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(employee_id):
        session = SessionLocal()
        try:
            return session.query(Employee).filter(Employee.id == employee_id).first()
        finally:
            session.close()

    @staticmethod
    def get_by_matricule(matricule):
        session = SessionLocal()
        try:
            return session.query(Employee).filter(Employee.matricule == matricule).first()
        finally:
            session.close()

    @staticmethod
    def update(employee_id, data: dict):
        session = SessionLocal()
        try:
            emp = session.query(Employee).filter(Employee.id == employee_id).first()
            if not emp:
                return None
            for key, val in data.items():
                if hasattr(emp, key) and key != "id":
                    setattr(emp, key, val)
            emp.updated_at = datetime.now()
            session.commit()
            session.refresh(emp)
            return emp
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(employee_id):
        session = SessionLocal()
        try:
            emp = session.query(Employee).filter(Employee.id == employee_id).first()
            if emp:
                emp.actif = False
                emp.updated_at = datetime.now()
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def hard_delete(employee_id):
        session = SessionLocal()
        try:
            emp = session.query(Employee).filter(Employee.id == employee_id).first()
            if emp:
                session.delete(emp)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def count():
        session = SessionLocal()
        try:
            return session.query(Employee).filter(Employee.actif == True).count()
        finally:
            session.close()
