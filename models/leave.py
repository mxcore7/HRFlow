from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    type_conge = Column(String(50), default="annuel")
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    motif = Column(Text, nullable=True)
    statut = Column(String(20), default="en_attente")  # en_attente, approuve, refuse
    commentaire = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    employee = relationship("Employee", back_populates="leaves")

    @property
    def duree_jours(self):
        if self.date_debut and self.date_fin:
            return (self.date_fin - self.date_debut).days + 1
        return 0

    def __repr__(self):
        return f"<Leave {self.employee_id} - {self.statut}>"
