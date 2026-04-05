from sqlalchemy import Column, Integer, String, Float, DateTime, LargeBinary, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    matricule = Column(String(20), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    poste = Column(String(100))
    departement = Column(String(100))
    telephone = Column(String(30))
    email = Column(String(150))
    salaire_base = Column(Float, default=0.0)
    photo = Column(LargeBinary, nullable=True)
    date_embauche = Column(DateTime, default=datetime.now)
    actif = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    attendances = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    leaves = relationship("Leave", back_populates="employee", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="employee", cascade="all, delete-orphan")
    salaries = relationship("Salary", back_populates="employee", cascade="all, delete-orphan")
    kpis = relationship("KPI", back_populates="employee", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.prenom} {self.nom}"

    def __repr__(self):
        return f"<Employee {self.matricule} - {self.full_name}>"
