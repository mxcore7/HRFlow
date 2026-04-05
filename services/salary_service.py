from models.base import SessionLocal
from models.salary import Salary
from services.kpi_service import KPIService
from config import load_config


class SalaryService:
    @staticmethod
    def generate(employee_id, month, year, salaire_base, bonus=0, deductions=0):
        config = load_config()
        kpi_config = config.get("kpi", {})
        prime_threshold = kpi_config.get("prime_threshold", 70)
        prime_percentage = kpi_config.get("prime_percentage", 10)

        kpi = KPIService.calculate(employee_id, month, year)
        kpi_score = kpi.score_global if kpi else 0

        prime_kpi = 0.0
        if kpi_score >= prime_threshold:
            prime_kpi = salaire_base * (prime_percentage / 100.0) * (kpi_score / 100.0)

        salaire_net = salaire_base + prime_kpi + bonus - deductions

        session = SessionLocal()
        try:
            existing = session.query(Salary).filter(
                Salary.employee_id == employee_id,
                Salary.mois == month,
                Salary.annee == year
            ).first()

            if existing:
                existing.salaire_base = salaire_base
                existing.prime_kpi = round(prime_kpi, 2)
                existing.bonus = bonus
                existing.deductions = deductions
                existing.salaire_net = round(salaire_net, 2)
                existing.kpi_score = round(kpi_score, 2)
                session.commit()
                session.refresh(existing)
                return existing
            else:
                sal = Salary(
                    employee_id=employee_id,
                    mois=month,
                    annee=year,
                    salaire_base=salaire_base,
                    prime_kpi=round(prime_kpi, 2),
                    bonus=bonus,
                    deductions=deductions,
                    salaire_net=round(salaire_net, 2),
                    kpi_score=round(kpi_score, 2),
                    statut="brouillon"
                )
                session.add(sal)
                session.commit()
                session.refresh(sal)
                return sal
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_all(employee_id=None, month=None, year=None):
        session = SessionLocal()
        try:
            q = session.query(Salary)
            if employee_id:
                q = q.filter(Salary.employee_id == employee_id)
            if month:
                q = q.filter(Salary.mois == month)
            if year:
                q = q.filter(Salary.annee == year)
            return q.order_by(Salary.annee.desc(), Salary.mois.desc()).all()
        finally:
            session.close()

    @staticmethod
    def validate(salary_id):
        session = SessionLocal()
        try:
            sal = session.query(Salary).filter(Salary.id == salary_id).first()
            if sal:
                sal.statut = "valide"
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
