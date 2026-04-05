from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from models.base import Base


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, default=date.today)
    heure_arrivee = Column(DateTime, nullable=True)
    heure_depart = Column(DateTime, nullable=True)
    duree_travail = Column(Float, default=0.0)
    retard_minutes = Column(Float, default=0.0)
    statut = Column(String(20), default="present")
    created_at = Column(DateTime, default=datetime.now)

    employee = relationship("Employee", back_populates="attendances")

    def __repr__(self):
        return f"<Attendance {self.employee_id} - {self.date}>"
