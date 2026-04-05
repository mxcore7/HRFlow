from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    titre = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    statut = Column(String(20), default="assigne")  # assigne, en_cours, termine, livre, annule
    priorite = Column(String(20), default="normale")  # basse, normale, haute, urgente
    date_echeance = Column(Date, nullable=True)
    date_debut = Column(DateTime, nullable=True)
    date_fin = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    employee = relationship("Employee", back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.titre} - {self.statut}>"
