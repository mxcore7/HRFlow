from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QSpinBox, QHeaderView, QAbstractItemView,
                             QMessageBox, QFileDialog, QDoubleSpinBox, QDialog,
                             QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from services.salary_service import SalaryService
from services.employee_service import EmployeeService
from services.kpi_service import KPIService
from utils.pdf_utils import generate_payslip_pdf
from config import load_config
from datetime import datetime
import os


class SalaryPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("💰 Gestion des salaires")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()

        header.addWidget(QLabel("Mois:"))
        self.month_spin = QSpinBox()
        self.month_spin.setRange(1, 12)
        self.month_spin.setValue(datetime.now().month)
        header.addWidget(self.month_spin)

        header.addWidget(QLabel("Année:"))
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2020, 2050)
        self.year_spin.setValue(datetime.now().year)
        header.addWidget(self.year_spin)

        gen_btn = QPushButton("⚙️ Générer fiches")
        gen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        gen_btn.clicked.connect(self._generate_all)
        header.addWidget(gen_btn)

        gen_one_btn = QPushButton("+ Fiche individuelle")
        gen_one_btn.setProperty("class", "accent")
        gen_one_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        gen_one_btn.clicked.connect(self._generate_individual)
        header.addWidget(gen_one_btn)
        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Employé", "Mois/An", "Base", "Prime KPI", "Bonus", "Déductions",
            "Net", "KPI Score", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(8, 80)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(42)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def refresh_data(self):
        month = self.month_spin.value()
        year = self.year_spin.value()
        salaries = SalaryService.get_all(month=month, year=year)
        self._fill_table(salaries)

    def _fill_table(self, salaries):
        self.table.setRowCount(len(salaries))
        for row, sal in enumerate(salaries):
            emp = EmployeeService.get_by_id(sal.employee_id)
            self.table.setItem(row, 0, QTableWidgetItem(emp.full_name if emp else ""))
            self.table.setItem(row, 1, QTableWidgetItem(f"{sal.mois:02d}/{sal.annee}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{sal.salaire_base:,.0f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{sal.prime_kpi:,.0f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{sal.bonus:,.0f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{sal.deductions:,.0f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{sal.salaire_net:,.0f}"))
            self.table.setItem(row, 7, QTableWidgetItem(f"{sal.kpi_score:.1f}/100"))

            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)

            pdf_btn = QPushButton("📄")
            pdf_btn.setFixedSize(32, 32)
            pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            pdf_btn.setProperty("class", "accent")
            pdf_btn.setToolTip("Exporter PDF")
            pdf_btn.clicked.connect(lambda _, sid=sal.id, eid=sal.employee_id: self._export_pdf(eid, sid))
            actions_layout.addWidget(pdf_btn)

            self.table.setCellWidget(row, 8, actions_widget)

    def _generate_all(self):
        month = self.month_spin.value()
        year = self.year_spin.value()
        employees = EmployeeService.get_all()
        count = 0
        for emp in employees:
            try:
                SalaryService.generate(emp.id, month, year, emp.salaire_base)
                count += 1
            except Exception:
                pass
        QMessageBox.information(self, "Succès", f"{count} fiches de paie générées pour {month:02d}/{year}")
        self.refresh_data()

    def _generate_individual(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Fiche de paie individuelle")
        dialog.setMinimumWidth(400)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        form = QFormLayout()
        emp_combo = QComboBox()
        for emp in EmployeeService.get_all():
            emp_combo.addItem(f"{emp.matricule} - {emp.full_name}", emp.id)
        form.addRow("Employé", emp_combo)

        bonus_spin = QDoubleSpinBox()
        bonus_spin.setRange(0, 99999999)
        bonus_spin.setDecimals(0)
        bonus_spin.setSuffix(" FCFA")
        form.addRow("Bonus", bonus_spin)

        ded_spin = QDoubleSpinBox()
        ded_spin.setRange(0, 99999999)
        ded_spin.setDecimals(0)
        ded_spin.setSuffix(" FCFA")
        form.addRow("Déductions", ded_spin)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Générer")
        save_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            emp_id = emp_combo.currentData()
            emp = EmployeeService.get_by_id(emp_id)
            if emp:
                month = self.month_spin.value()
                year = self.year_spin.value()
                SalaryService.generate(emp_id, month, year, emp.salaire_base,
                                       bonus=bonus_spin.value(), deductions=ded_spin.value())
                self.refresh_data()

    def _export_pdf(self, employee_id, salary_id):
        emp = EmployeeService.get_by_id(employee_id)
        salaries = SalaryService.get_all(employee_id=employee_id)
        sal = next((s for s in salaries if s.id == salary_id), None)
        if not emp or not sal:
            return

        kpis = KPIService.get_employee_kpi(employee_id, sal.mois, sal.annee)
        kpi = kpis[0] if kpis else None
        config = load_config()

        paie_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "documents", "fiches_de_paie")
        os.makedirs(paie_dir, exist_ok=True)
        path = os.path.join(paie_dir, f"fiche_paie_{emp.matricule}_{sal.mois:02d}_{sal.annee}.pdf")
        try:
            generate_payslip_pdf(emp, sal, kpi, path, config.get("company", {}))
            QMessageBox.information(self, "Succès", f"Fiche de paie exportée : {path}")
            os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))
