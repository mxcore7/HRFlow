from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QFormLayout, QComboBox, QDateEdit,
                             QTextEdit, QLineEdit, QHeaderView, QAbstractItemView,
                             QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from services.task_service import TaskService
from services.employee_service import EmployeeService
from services.sms_service import SMSService


class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle("Modifier la tâche" if task else "Nouvelle tâche")
        self.setMinimumWidth(500)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("Modifier la tâche" if self.task else "📋 Nouvelle tâche")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.employee_combo = QComboBox()
        for emp in EmployeeService.get_all():
            self.employee_combo.addItem(f"{emp.matricule} - {emp.full_name}", emp.id)
        form.addRow("Employé *", self.employee_combo)

        self.titre_input = QLineEdit()
        self.titre_input.setPlaceholderText("Titre de la tâche")
        form.addRow("Titre *", self.titre_input)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Description de la tâche...")
        self.desc_input.setMaximumHeight(80)
        form.addRow("Description", self.desc_input)

        self.priorite_combo = QComboBox()
        self.priorite_combo.addItems(["Basse", "Normale", "Haute", "Urgente"])
        self.priorite_combo.setCurrentIndex(1)
        form.addRow("Priorité", self.priorite_combo)

        self.echeance_input = QDateEdit()
        self.echeance_input.setDate(QDate.currentDate().addDays(7))
        self.echeance_input.setCalendarPopup(True)
        form.addRow("Échéance", self.echeance_input)

        if self.task:
            for i in range(self.employee_combo.count()):
                if self.employee_combo.itemData(i) == self.task.employee_id:
                    self.employee_combo.setCurrentIndex(i)
                    break
            self.titre_input.setText(self.task.titre)
            self.desc_input.setPlainText(self.task.description or "")
            prio_map = {"basse": 0, "normale": 1, "haute": 2, "urgente": 3}
            self.priorite_combo.setCurrentIndex(prio_map.get(self.task.priorite, 1))

        layout.addLayout(form)

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

    def _save(self):
        if not self.titre_input.text().strip():
            QMessageBox.warning(self, "Erreur", "Le titre est obligatoire.")
            return

        from datetime import date
        prio_map = {0: "basse", 1: "normale", 2: "haute", 3: "urgente"}
        emp_id = self.employee_combo.currentData()

        data = {
            "employee_id": emp_id,
            "titre": self.titre_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "priorite": prio_map.get(self.priorite_combo.currentIndex(), "normale"),
            "date_echeance": date(
                self.echeance_input.date().year(),
                self.echeance_input.date().month(),
                self.echeance_input.date().day()
            )
        }

        try:
            if self.task:
                from models.base import SessionLocal
                from models.task import Task
                session = SessionLocal()
                t = session.query(Task).filter(Task.id == self.task.id).first()
                if t:
                    t.employee_id = data["employee_id"]
                    t.titre = data["titre"]
                    t.description = data["description"]
                    t.priorite = data["priorite"]
                    t.date_echeance = data["date_echeance"]
                    session.commit()
                session.close()
            else:
                TaskService.create(data)
                emp = EmployeeService.get_by_id(emp_id)
                if emp and emp.telephone:
                    try:
                        SMSService.notify_task_assigned(emp.full_name, emp.telephone, data["titre"])
                    except Exception:
                        pass
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))


class TaskPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("📋 Gestion des tâches")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()

        self.filter_status = QComboBox()
        self.filter_status.addItems(["Toutes", "Assigné", "En cours", "Terminé", "Livré", "Annulé"])
        self.filter_status.currentIndexChanged.connect(self._apply_filter)
        header.addWidget(self.filter_status)

        self.filter_employee = QComboBox()
        self.filter_employee.addItem("Tous les employés", None)
        self.filter_employee.currentIndexChanged.connect(self._apply_filter)
        header.addWidget(self.filter_employee)

        add_btn = QPushButton("+ Nouvelle tâche")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self._add_task)
        header.addWidget(add_btn)
        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Employé", "Titre", "Priorité", "Statut", "Échéance", "Début", "Fin", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def refresh_data(self):
        self.filter_employee.blockSignals(True)
        current_data = self.filter_employee.currentData()
        self.filter_employee.clear()
        self.filter_employee.addItem("Tous les employés", None)
        for emp in EmployeeService.get_all():
            self.filter_employee.addItem(f"{emp.matricule} - {emp.full_name}", emp.id)
        for i in range(self.filter_employee.count()):
            if self.filter_employee.itemData(i) == current_data:
                self.filter_employee.setCurrentIndex(i)
                break
        self.filter_employee.blockSignals(False)
        self._apply_filter()

    def _apply_filter(self):
        statut_map = {"Toutes": None, "Assigné": "assigne", "En cours": "en_cours",
                      "Terminé": "termine", "Livré": "livre", "Annulé": "annule"}
        statut = statut_map.get(self.filter_status.currentText())
        emp_id = self.filter_employee.currentData()
        tasks = TaskService.get_all(employee_id=emp_id, statut=statut)
        self._fill_table(tasks)

    def _fill_table(self, tasks):
        self.table.setRowCount(len(tasks))
        statut_labels = {"assigne": "📌 Assigné", "en_cours": "🔄 En cours",
                         "termine": "✅ Terminé", "livre": "📦 Livré", "annule": "❌ Annulé"}
        prio_labels = {"basse": "🟢 Basse", "normale": "🔵 Normale",
                       "haute": "🟠 Haute", "urgente": "🔴 Urgente"}

        for row, task in enumerate(tasks):
            emp = EmployeeService.get_by_id(task.employee_id)
            self.table.setItem(row, 0, QTableWidgetItem(emp.full_name if emp else ""))
            self.table.setItem(row, 1, QTableWidgetItem(task.titre))
            self.table.setItem(row, 2, QTableWidgetItem(prio_labels.get(task.priorite, task.priorite)))
            self.table.setItem(row, 3, QTableWidgetItem(statut_labels.get(task.statut, task.statut)))
            self.table.setItem(row, 4, QTableWidgetItem(str(task.date_echeance) if task.date_echeance else "-"))
            self.table.setItem(row, 5, QTableWidgetItem(
                task.date_debut.strftime("%Y-%m-%d %H:%M") if task.date_debut else "-"))
            self.table.setItem(row, 6, QTableWidgetItem(
                task.date_fin.strftime("%Y-%m-%d %H:%M") if task.date_fin else "-"))

            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(3)

            if task.statut == "assigne":
                start_btn = QPushButton("▶")
                start_btn.setFixedSize(28, 28)
                start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                start_btn.setToolTip("Démarrer")
                start_btn.setProperty("class", "accent")
                start_btn.clicked.connect(lambda _, tid=task.id: self._update_status(tid, "en_cours"))
                actions_layout.addWidget(start_btn)

            if task.statut == "en_cours":
                done_btn = QPushButton("✔")
                done_btn.setFixedSize(28, 28)
                done_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                done_btn.setToolTip("Terminer")
                done_btn.clicked.connect(lambda _, tid=task.id: self._update_status(tid, "termine"))
                actions_layout.addWidget(done_btn)

            if task.statut == "termine":
                deliver_btn = QPushButton("📦")
                deliver_btn.setFixedSize(28, 28)
                deliver_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                deliver_btn.setToolTip("Livrer")
                deliver_btn.setProperty("class", "accent")
                deliver_btn.clicked.connect(lambda _, tid=task.id: self._update_status(tid, "livre"))
                actions_layout.addWidget(deliver_btn)

            if task.statut not in ("annule", "livre"):
                cancel_btn = QPushButton("✕")
                cancel_btn.setFixedSize(28, 28)
                cancel_btn.setProperty("class", "danger")
                cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                cancel_btn.setToolTip("Annuler")
                cancel_btn.clicked.connect(lambda _, tid=task.id: self._update_status(tid, "annule"))
                actions_layout.addWidget(cancel_btn)

            del_btn = QPushButton("🗑")
            del_btn.setFixedSize(28, 28)
            del_btn.setProperty("class", "danger")
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.setToolTip("Supprimer")
            del_btn.clicked.connect(lambda _, tid=task.id: self._delete_task(tid))
            actions_layout.addWidget(del_btn)

            self.table.setCellWidget(row, 7, actions_widget)

    def _add_task(self):
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def _update_status(self, task_id, new_status):
        TaskService.update_status(task_id, new_status)
        self.refresh_data()

    def _delete_task(self, task_id):
        reply = QMessageBox.question(
            self, "Confirmer", "Supprimer cette tâche ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            TaskService.delete(task_id)
            self.refresh_data()
