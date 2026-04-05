from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class KPI(Base):
    __tablename__ = "kpis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    mois = Column(Integer, nullable=False)
    annee = Column(Integer, nullable=False)
    score_taches = Column(Float, default=0.0)
    score_presence = Column(Float, default=0.0)
    score_ponctualite = Column(Float, default=0.0)
    score_global = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)

    employee = relationship("Employee", back_populates="kpis")

    def __repr__(self):
        return f"<KPI {self.employee_id} - {self.score_global}/100>"
