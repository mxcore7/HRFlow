from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
                             QDialog, QFormLayout, QFileDialog, QMessageBox,
                             QHeaderView, QComboBox, QDoubleSpinBox, QDateEdit,
                             QAbstractItemView)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPixmap, QImage
from services.employee_service import EmployeeService
from utils.pdf_utils import generate_badge_pdf
import os
import tempfile


class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.employee = employee
        self.photo_data = None
        self.setWindowTitle("Modifier l'employé" if employee else "Nouvel employé")
        self.setMinimumWidth(500)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("Modifier l'employé" if self.employee else "Nouvel employé")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom de famille")
        form.addRow("Nom *", self.nom_input)

        self.prenom_input = QLineEdit()
        self.prenom_input.setPlaceholderText("Prénom")
        form.addRow("Prénom *", self.prenom_input)

        self.matricule_input = QLineEdit()
        self.matricule_input.setPlaceholderText("Auto-généré si vide")
        form.addRow("Matricule", self.matricule_input)

        self.poste_input = QLineEdit()
        self.poste_input.setPlaceholderText("Ex: Développeur, Manager...")
        form.addRow("Poste", self.poste_input)

        self.dept_input = QLineEdit()
        self.dept_input.setPlaceholderText("Ex: IT, RH, Finance...")
        form.addRow("Département", self.dept_input)

        self.tel_input = QLineEdit()
        self.tel_input.setPlaceholderText("Ex: 237697624219")
        form.addRow("Téléphone", self.tel_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@exemple.com")
        form.addRow("Email", self.email_input)

        self.salaire_input = QDoubleSpinBox()
        self.salaire_input.setRange(0, 99999999)
        self.salaire_input.setDecimals(0)
        self.salaire_input.setSuffix(" FCFA")
        form.addRow("Salaire de base", self.salaire_input)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form.addRow("Date d'embauche", self.date_input)

        photo_layout = QHBoxLayout()
        self.photo_label = QLabel("Aucune photo")
        self.photo_label.setFixedSize(80, 80)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet("border: 2px dashed #30363d; border-radius: 8px;")
        photo_layout.addWidget(self.photo_label)

        photo_btn = QPushButton("📷 Choisir")
        photo_btn.setProperty("class", "secondary")
        photo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        photo_btn.clicked.connect(self._choose_photo)
        photo_layout.addWidget(photo_btn)
        photo_layout.addStretch()
        form.addRow("Photo", photo_layout)

        layout.addLayout(form)

        if self.employee:
            self.nom_input.setText(self.employee.nom)
            self.prenom_input.setText(self.employee.prenom)
            self.matricule_input.setText(self.employee.matricule)
            self.matricule_input.setReadOnly(True)
            self.poste_input.setText(self.employee.poste or "")
            self.dept_input.setText(self.employee.departement or "")
            self.tel_input.setText(self.employee.telephone or "")
            self.email_input.setText(self.employee.email or "")
            self.salaire_input.setValue(self.employee.salaire_base or 0)
            if self.employee.date_embauche:
                self.date_input.setDate(QDate(
                    self.employee.date_embauche.year,
                    self.employee.date_embauche.month,
                    self.employee.date_embauche.day
                ))
            if self.employee.photo:
                self.photo_data = self.employee.photo
                self._display_photo(self.employee.photo)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _choose_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir une photo", "",
                                               "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            with open(path, "rb") as f:
                self.photo_data = f.read()
            self._display_photo(self.photo_data)

    def _display_photo(self, data):
        img = QImage()
        img.loadFromData(data)
        pixmap = QPixmap.fromImage(img).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation)
        self.photo_label.setPixmap(pixmap)

    def _save(self):
        if not self.nom_input.text().strip() or not self.prenom_input.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom et le prénom sont obligatoires.")
            return

        from datetime import datetime
        data = {
            "nom": self.nom_input.text().strip(),
            "prenom": self.prenom_input.text().strip(),
            "poste": self.poste_input.text().strip(),
            "departement": self.dept_input.text().strip(),
            "telephone": self.tel_input.text().strip(),
            "email": self.email_input.text().strip(),
            "salaire_base": self.salaire_input.value(),
            "date_embauche": datetime(
                self.date_input.date().year(),
                self.date_input.date().month(),
                self.date_input.date().day()
            ),
            "photo": self.photo_data,
        }

        if not self.employee:
            mat = self.matricule_input.text().strip()
            if mat:
                data["matricule"] = mat

        try:
            if self.employee:
                EmployeeService.update(self.employee.id, data)
            else:
                EmployeeService.create(data)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))


class EmployeePage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("👥 Gestion des employés")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self._filter_table)
        header.addWidget(self.search_input)

        add_btn = QPushButton("+ Ajouter")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self._add_employee)
        header.addWidget(add_btn)
        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Matricule", "Nom", "Prénom", "Poste", "Département", "Téléphone", "Salaire", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def refresh_data(self):
        employees = EmployeeService.get_all()
        self.table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(emp.matricule))
            self.table.setItem(row, 1, QTableWidgetItem(emp.nom))
            self.table.setItem(row, 2, QTableWidgetItem(emp.prenom))
            self.table.setItem(row, 3, QTableWidgetItem(emp.poste or ""))
            self.table.setItem(row, 4, QTableWidgetItem(emp.departement or ""))
            self.table.setItem(row, 5, QTableWidgetItem(emp.telephone or ""))
            self.table.setItem(row, 6, QTableWidgetItem(f"{emp.salaire_base:,.0f}"))

            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)
            actions_layout.setSpacing(4)

            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(32, 32)
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.setProperty("class", "accent")
            edit_btn.setToolTip("Modifier")
            edit_btn.clicked.connect(lambda _, eid=emp.id: self._edit_employee(eid))
            actions_layout.addWidget(edit_btn)

            badge_btn = QPushButton("🪪")
            badge_btn.setFixedSize(32, 32)
            badge_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            badge_btn.setProperty("class", "secondary")
            badge_btn.setToolTip("Générer badge PDF")
            badge_btn.clicked.connect(lambda _, eid=emp.id: self._generate_badge(eid))
            actions_layout.addWidget(badge_btn)

            del_btn = QPushButton("🗑️")
            del_btn.setFixedSize(32, 32)
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.setProperty("class", "danger")
            del_btn.setToolTip("Supprimer")
            del_btn.clicked.connect(lambda _, eid=emp.id: self._delete_employee(eid))
            actions_layout.addWidget(del_btn)

            self.table.setCellWidget(row, 7, actions_widget)

    def _filter_table(self, text):
        text = text.lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount() - 1):
                item = self.table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def _add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def _edit_employee(self, employee_id):
        emp = EmployeeService.get_by_id(employee_id)
        if emp:
            dialog = EmployeeDialog(self, emp)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.refresh_data()

    def _generate_badge(self, employee_id):
        emp = EmployeeService.get_by_id(employee_id)
        if emp:
            path, _ = QFileDialog.getSaveFileName(
                self, "Enregistrer le badge", f"badge_{emp.matricule}.pdf",
                "PDF (*.pdf)"
            )
            if path:
                try:
                    generate_badge_pdf(emp, path)
                    QMessageBox.information(self, "Succès", f"Badge généré : {path}")
                    os.startfile(path)
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", str(e))

    def _delete_employee(self, employee_id):
        reply = QMessageBox.question(
            self, "Confirmer", "Voulez-vous vraiment désactiver cet employé ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            EmployeeService.delete(employee_id)
            self.refresh_data()
