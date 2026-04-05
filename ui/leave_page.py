from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QFormLayout, QComboBox, QDateEdit,
                             QTextEdit, QHeaderView, QAbstractItemView, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from services.leave_service import LeaveService
from services.employee_service import EmployeeService


class LeaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouvelle demande de congé")
        self.setMinimumWidth(450)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("📅 Demande de congé")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.employee_combo = QComboBox()
        for emp in EmployeeService.get_all():
            self.employee_combo.addItem(f"{emp.matricule} - {emp.full_name}", emp.id)
        form.addRow("Employé *", self.employee_combo)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Annuel", "Maladie", "Maternité", "Sans solde", "Autre"])
        form.addRow("Type", self.type_combo)

        self.date_debut = QDateEdit()
        self.date_debut.setDate(QDate.currentDate())
        self.date_debut.setCalendarPopup(True)
        form.addRow("Date début *", self.date_debut)

        self.date_fin = QDateEdit()
        self.date_fin.setDate(QDate.currentDate().addDays(1))
        self.date_fin.setCalendarPopup(True)
        form.addRow("Date fin *", self.date_fin)

        self.motif_input = QTextEdit()
        self.motif_input.setPlaceholderText("Motif de la demande...")
        self.motif_input.setMaximumHeight(80)
        form.addRow("Motif", self.motif_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("📨 Soumettre")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _save(self):
        from datetime import date
        d_start = date(
            self.date_debut.date().year(),
            self.date_debut.date().month(),
            self.date_debut.date().day()
        )
        d_end = date(
            self.date_fin.date().year(),
            self.date_fin.date().month(),
            self.date_fin.date().day()
        )
        if d_end < d_start:
            QMessageBox.warning(self, "Erreur", "La date de fin doit être après la date de début.")
            return

        types_map = {"Annuel": "annuel", "Maladie": "maladie", "Maternité": "maternite",
                     "Sans solde": "sans_solde", "Autre": "autre"}
        data = {
            "employee_id": self.employee_combo.currentData(),
            "type_conge": types_map.get(self.type_combo.currentText(), "annuel"),
            "date_debut": d_start,
            "date_fin": d_end,
            "motif": self.motif_input.toPlainText().strip()
        }
        try:
            LeaveService.create(data)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))


class LeavePage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("📅 Gestion des congés")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tous", "En attente", "Approuvés", "Refusés"])
        self.filter_combo.currentIndexChanged.connect(self._apply_filter)
        header.addWidget(self.filter_combo)

        add_btn = QPushButton("+ Nouvelle demande")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self._add_leave)
        header.addWidget(add_btn)
        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Employé", "Type", "Début", "Fin", "Jours", "Motif", "Statut", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def refresh_data(self):
        self._apply_filter()

    def _apply_filter(self):
        statut_map = {"Tous": None, "En attente": "en_attente", "Approuvés": "approuve", "Refusés": "refuse"}
        statut = statut_map.get(self.filter_combo.currentText())
        leaves = LeaveService.get_all(statut=statut)
        self._fill_table(leaves)

    def _fill_table(self, leaves):
        self.table.setRowCount(len(leaves))
        type_labels = {"annuel": "Annuel", "maladie": "Maladie", "maternite": "Maternité",
                       "sans_solde": "Sans solde", "autre": "Autre"}
        statut_labels = {"en_attente": "⏳ En attente", "approuve": "✅ Approuvé", "refuse": "❌ Refusé"}

        for row, leave in enumerate(leaves):
            emp = EmployeeService.get_by_id(leave.employee_id)
            self.table.setItem(row, 0, QTableWidgetItem(emp.full_name if emp else ""))
            self.table.setItem(row, 1, QTableWidgetItem(type_labels.get(leave.type_conge, leave.type_conge)))
            self.table.setItem(row, 2, QTableWidgetItem(str(leave.date_debut)))
            self.table.setItem(row, 3, QTableWidgetItem(str(leave.date_fin)))
            self.table.setItem(row, 4, QTableWidgetItem(str(leave.duree_jours)))
            self.table.setItem(row, 5, QTableWidgetItem(leave.motif or ""))
            self.table.setItem(row, 6, QTableWidgetItem(statut_labels.get(leave.statut, leave.statut)))

            if leave.statut == "en_attente":
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(4, 2, 4, 2)
                actions_layout.setSpacing(4)

                approve_btn = QPushButton("✅")
                approve_btn.setFixedSize(32, 32)
                approve_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                approve_btn.setToolTip("Approuver")
                approve_btn.clicked.connect(lambda _, lid=leave.id: self._approve(lid))
                actions_layout.addWidget(approve_btn)

                reject_btn = QPushButton("❌")
                reject_btn.setFixedSize(32, 32)
                reject_btn.setProperty("class", "danger")
                reject_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                reject_btn.setToolTip("Refuser")
                reject_btn.clicked.connect(lambda _, lid=leave.id: self._reject(lid))
                actions_layout.addWidget(reject_btn)

                self.table.setCellWidget(row, 7, actions_widget)

    def _add_leave(self):
        dialog = LeaveDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def _approve(self, leave_id):
        LeaveService.approve(leave_id, "Approuvé par le manager")
        self.refresh_data()

    def _reject(self, leave_id):
        LeaveService.reject(leave_id, "Refusé par le manager")
        self.refresh_data()
