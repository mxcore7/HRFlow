from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QMessageBox, QDateEdit,
                             QComboBox, QFrame)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from services.attendance_service import AttendanceService
from services.employee_service import EmployeeService
from datetime import date


class AttendancePage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("⏰ Gestion des présences")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        pointage_frame = QFrame()
        pointage_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(22, 27, 34, 0.8);
                border: 1px solid #21262d;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        pl = QHBoxLayout(pointage_frame)
        pl.setSpacing(15)

        pl.addWidget(QLabel("Matricule:"))
        self.matricule_input = QLineEdit()
        self.matricule_input.setPlaceholderText("Entrez le matricule de l'employé")
        self.matricule_input.setFixedWidth(250)
        self.matricule_input.returnPressed.connect(self._do_pointage)
        pl.addWidget(self.matricule_input)

        pointage_btn = QPushButton("⏱️ Pointer")
        pointage_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pointage_btn.setFixedWidth(140)
        pointage_btn.clicked.connect(self._do_pointage)
        pl.addWidget(pointage_btn)

        self.pointage_status = QLabel("")
        self.pointage_status.setFont(QFont("Segoe UI", 11))
        pl.addWidget(self.pointage_status)
        pl.addStretch()
        layout.addWidget(pointage_frame)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtre :"))

        self.filter_employee = QComboBox()
        self.filter_employee.addItem("Tous les employés", None)
        self.filter_employee.setFixedWidth(200)
        filter_layout.addWidget(self.filter_employee)

        self.date_start = QDateEdit()
        self.date_start.setDate(QDate.currentDate())
        self.date_start.setCalendarPopup(True)
        filter_layout.addWidget(QLabel("Du:"))
        filter_layout.addWidget(self.date_start)

        self.date_end = QDateEdit()
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setCalendarPopup(True)
        filter_layout.addWidget(QLabel("Au:"))
        filter_layout.addWidget(self.date_end)

        filter_btn = QPushButton("🔍 Filtrer")
        filter_btn.setProperty("class", "accent")
        filter_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        filter_btn.clicked.connect(self._apply_filter)
        filter_layout.addWidget(filter_btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Date", "Matricule", "Nom", "Arrivée", "Départ", "Durée (h)", "Retard (min)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def refresh_data(self):
        self.filter_employee.clear()
        self.filter_employee.addItem("Tous les employés", None)
        for emp in EmployeeService.get_all():
            self.filter_employee.addItem(f"{emp.matricule} - {emp.full_name}", emp.id)
        self._load_today()

    def _load_today(self):
        records = AttendanceService.get_today()
        self._fill_table(records)

    def _apply_filter(self):
        emp_id = self.filter_employee.currentData()
        start = date(
            self.date_start.date().year(),
            self.date_start.date().month(),
            self.date_start.date().day()
        )
        end = date(
            self.date_end.date().year(),
            self.date_end.date().month(),
            self.date_end.date().day()
        )
        records = AttendanceService.get_history(emp_id, start, end)
        self._fill_table(records)

    def _fill_table(self, records):
        self.table.setRowCount(len(records))
        for row, rec in enumerate(records):
            emp = EmployeeService.get_by_id(rec.employee_id)
            self.table.setItem(row, 0, QTableWidgetItem(str(rec.date)))
            self.table.setItem(row, 1, QTableWidgetItem(emp.matricule if emp else ""))
            self.table.setItem(row, 2, QTableWidgetItem(emp.full_name if emp else ""))
            self.table.setItem(row, 3, QTableWidgetItem(
                rec.heure_arrivee.strftime("%H:%M") if rec.heure_arrivee else "-"))
            self.table.setItem(row, 4, QTableWidgetItem(
                rec.heure_depart.strftime("%H:%M") if rec.heure_depart else "-"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{rec.duree_travail:.1f}" if rec.duree_travail else "-"))

            retard_item = QTableWidgetItem(f"{rec.retard_minutes:.0f}" if rec.retard_minutes else "0")
            if rec.retard_minutes and rec.retard_minutes > 0:
                retard_item.setForeground(Qt.GlobalColor.red)
            self.table.setItem(row, 6, retard_item)

    def _do_pointage(self):
        matricule = self.matricule_input.text().strip()
        if not matricule:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un matricule.")
            return

        emp = EmployeeService.get_by_matricule(matricule)
        if not emp:
            QMessageBox.warning(self, "Erreur", f"Aucun employé trouvé avec le matricule : {matricule}")
            return

        att, status = AttendanceService.smart_pointage(emp.id)
        if status == "checked_in":
            self.pointage_status.setText(f"✅ {emp.full_name} - Entrée enregistrée à {att.heure_arrivee.strftime('%H:%M')}")
            self.pointage_status.setStyleSheet("color: #238636;")
        elif status == "checked_out":
            self.pointage_status.setText(f"🏠 {emp.full_name} - Sortie enregistrée à {att.heure_depart.strftime('%H:%M')}")
            self.pointage_status.setStyleSheet("color: #58a6ff;")
        elif status == "already_checked_in":
            self.pointage_status.setText(f"⚠️ {emp.full_name} - Déjà pointé aujourd'hui")
            self.pointage_status.setStyleSheet("color: #d29922;")

        self.matricule_input.clear()
        self._load_today()
