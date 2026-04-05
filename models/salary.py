from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class Salary(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    mois = Column(Integer, nullable=False)
    annee = Column(Integer, nullable=False)
    salaire_base = Column(Float, default=0.0)
    prime_kpi = Column(Float, default=0.0)
    bonus = Column(Float, default=0.0)
    deductions = Column(Float, default=0.0)
    salaire_net = Column(Float, default=0.0)
    kpi_score = Column(Float, default=0.0)
    statut = Column(String(20), default="brouillon")  # brouillon, valide, paye
    created_at = Column(DateTime, default=datetime.now)

    employee = relationship("Employee", back_populates="salaries")

    def __repr__(self):
        return f"<Salary {self.employee_id} - {self.mois}/{self.annee}>"
