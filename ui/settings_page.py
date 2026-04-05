from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QCheckBox, QSpinBox,
                             QDoubleSpinBox, QGroupBox, QFormLayout, QTabWidget,
                             QMessageBox, QComboBox, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from config import load_config, save_config


class SettingsPage(QWidget):
    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.config = load_config()
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        header = QHBoxLayout()
        title = QLabel("⚙️ Paramètres")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()

        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._save_all)
        header.addWidget(save_btn)
        main_layout.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        layout.setSpacing(15)

        tabs = QTabWidget()

        general_tab = QWidget()
        gl = QVBoxLayout(general_tab)
        gl.setSpacing(15)

        theme_group = QGroupBox("Apparence")
        tgl = QFormLayout(theme_group)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Sombre", "Clair"])
        if self.config.get("theme") == "light":
            self.theme_combo.setCurrentIndex(1)
        tgl.addRow("Thème", self.theme_combo)
        gl.addWidget(theme_group)

        company_group = QGroupBox("Entreprise")
        cgl = QFormLayout(company_group)
        company = self.config.get("company", {})
        self.company_name = QLineEdit(company.get("name", ""))
        self.company_name.setPlaceholderText("Nom de l'entreprise")
        cgl.addRow("Nom", self.company_name)
        self.company_address = QLineEdit(company.get("address", ""))
        cgl.addRow("Adresse", self.company_address)
        self.company_phone = QLineEdit(company.get("phone", ""))
        cgl.addRow("Téléphone", self.company_phone)
        gl.addWidget(company_group)

        work_group = QGroupBox("Horaires de travail")
        wgl = QFormLayout(work_group)
        self.work_start_h = QSpinBox()
        self.work_start_h.setRange(0, 23)
        self.work_start_h.setValue(self.config.get("work_start_hour", 8))
        wgl.addRow("Heure début", self.work_start_h)
        self.work_start_m = QSpinBox()
        self.work_start_m.setRange(0, 59)
        self.work_start_m.setValue(self.config.get("work_start_minute", 0))
        wgl.addRow("Minute début", self.work_start_m)
        self.work_hours = QSpinBox()
        self.work_hours.setRange(1, 24)
        self.work_hours.setValue(self.config.get("work_hours_per_day", 8))
        wgl.addRow("Heures/jour", self.work_hours)
        gl.addWidget(work_group)
        gl.addStretch()
        tabs.addTab(general_tab, "🏠 Général")

        kpi_tab = QWidget()
        kl = QVBoxLayout(kpi_tab)
        kpi_config = self.config.get("kpi", {})

        weights_group = QGroupBox("Pondération KPI (total = 100%)")
        wfl = QFormLayout(weights_group)
        self.weight_tasks = QSpinBox()
        self.weight_tasks.setRange(0, 100)
        self.weight_tasks.setValue(kpi_config.get("weight_tasks", 40))
        self.weight_tasks.setSuffix("%")
        wfl.addRow("Tâches", self.weight_tasks)
        self.weight_attendance = QSpinBox()
        self.weight_attendance.setRange(0, 100)
        self.weight_attendance.setValue(kpi_config.get("weight_attendance", 30))
        self.weight_attendance.setSuffix("%")
        wfl.addRow("Présence", self.weight_attendance)
        self.weight_punctuality = QSpinBox()
        self.weight_punctuality.setRange(0, 100)
        self.weight_punctuality.setValue(kpi_config.get("weight_punctuality", 30))
        self.weight_punctuality.setSuffix("%")
        wfl.addRow("Ponctualité", self.weight_punctuality)
        kl.addWidget(weights_group)

        prime_group = QGroupBox("Prime")
        pfl = QFormLayout(prime_group)
        self.prime_threshold = QSpinBox()
        self.prime_threshold.setRange(0, 100)
        self.prime_threshold.setValue(kpi_config.get("prime_threshold", 70))
        self.prime_threshold.setSuffix("/100")
        pfl.addRow("Seuil KPI minimum", self.prime_threshold)
        self.prime_percentage = QDoubleSpinBox()
        self.prime_percentage.setRange(0, 100)
        self.prime_percentage.setValue(kpi_config.get("prime_percentage", 10))
        self.prime_percentage.setSuffix(" %")
        pfl.addRow("% du salaire de base", self.prime_percentage)
        kl.addWidget(prime_group)
        kl.addStretch()
        tabs.addTab(kpi_tab, "📊 KPI & Primes")

        sms_tab = QWidget()
        sl = QVBoxLayout(sms_tab)

        sms_group = QGroupBox("Configuration API SMS (Onbuka)")
        sfl = QFormLayout(sms_group)
        sms_config = self.config.get("sms_api", {})

        self.sms_enabled = QCheckBox("Activer les notifications SMS")
        self.sms_enabled.setChecked(sms_config.get("enabled", False))
        sfl.addRow(self.sms_enabled)

        self.sms_base_url = QLineEdit(sms_config.get("base_url", "https://api.onbuka.com/v3"))
        sfl.addRow("URL de base", self.sms_base_url)
        self.sms_api_key = QLineEdit(sms_config.get("api_key", ""))
        self.sms_api_key.setPlaceholderText("Clé API")
        sfl.addRow("API Key", self.sms_api_key)
        self.sms_api_pwd = QLineEdit(sms_config.get("api_pwd", ""))
        self.sms_api_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.sms_api_pwd.setPlaceholderText("Mot de passe API")
        sfl.addRow("API Password", self.sms_api_pwd)
        self.sms_app_id = QLineEdit(sms_config.get("app_id", ""))
        self.sms_app_id.setPlaceholderText("ID Application")
        sfl.addRow("App ID", self.sms_app_id)
        self.sms_sender = QLineEdit(sms_config.get("sender_id", "HRFlow"))
        sfl.addRow("Sender ID", self.sms_sender)
        sl.addWidget(sms_group)

        test_btn = QPushButton("📱 Tester l'envoi SMS")
        test_btn.setProperty("class", "accent")
        test_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        test_btn.clicked.connect(self._test_sms)
        sl.addWidget(test_btn)
        sl.addStretch()
        tabs.addTab(sms_tab, "📱 SMS")

        db_tab = QWidget()
        dl = QVBoxLayout(db_tab)
        db_group = QGroupBox("PostgreSQL")
        dfl = QFormLayout(db_group)
        db_config = self.config.get("database", {})
        self.db_host = QLineEdit(db_config.get("host", "localhost"))
        dfl.addRow("Hôte", self.db_host)
        self.db_port = QSpinBox()
        self.db_port.setRange(1, 65535)
        self.db_port.setValue(db_config.get("port", 5432))
        dfl.addRow("Port", self.db_port)
        self.db_name = QLineEdit(db_config.get("name", "hrflow"))
        dfl.addRow("Base de données", self.db_name)
        self.db_user = QLineEdit(db_config.get("user", "postgres"))
        dfl.addRow("Utilisateur", self.db_user)
        self.db_password = QLineEdit(db_config.get("password", ""))
        self.db_password.setEchoMode(QLineEdit.EchoMode.Password)
        dfl.addRow("Mot de passe", self.db_password)
        dl.addWidget(db_group)

        warn = QLabel("⚠️ Les modifications de la base de données nécessitent un redémarrage.")
        warn.setStyleSheet("color: #d29922;")
        dl.addWidget(warn)
        dl.addStretch()
        tabs.addTab(db_tab, "🗄️ Base de données")

        layout.addWidget(tabs)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

    def _save_all(self):
        total_weights = self.weight_tasks.value() + self.weight_attendance.value() + self.weight_punctuality.value()
        if total_weights != 100:
            QMessageBox.warning(self, "Erreur", f"La pondération KPI doit totaliser 100% (actuellement {total_weights}%)")
            return

        self.config["theme"] = "light" if self.theme_combo.currentIndex() == 1 else "dark"
        self.config["company"] = {
            "name": self.company_name.text(),
            "address": self.company_address.text(),
            "phone": self.company_phone.text(),
            "logo_path": self.config.get("company", {}).get("logo_path", "")
        }
        self.config["work_start_hour"] = self.work_start_h.value()
        self.config["work_start_minute"] = self.work_start_m.value()
        self.config["work_hours_per_day"] = self.work_hours.value()
        self.config["kpi"] = {
            "weight_tasks": self.weight_tasks.value(),
            "weight_attendance": self.weight_attendance.value(),
            "weight_punctuality": self.weight_punctuality.value(),
            "prime_threshold": self.prime_threshold.value(),
            "prime_percentage": self.prime_percentage.value()
        }
        self.config["sms_api"] = {
            "enabled": self.sms_enabled.isChecked(),
            "base_url": self.sms_base_url.text(),
            "api_key": self.sms_api_key.text(),
            "api_pwd": self.sms_api_pwd.text(),
            "app_id": self.sms_app_id.text(),
            "sender_id": self.sms_sender.text()
        }
        self.config["database"] = {
            "host": self.db_host.text(),
            "port": self.db_port.value(),
            "name": self.db_name.text(),
            "user": self.db_user.text(),
            "password": self.db_password.text()
        }

        save_config(self.config)
        self.theme_changed.emit(self.config["theme"])
        QMessageBox.information(self, "Succès", "Paramètres enregistrés avec succès !")

    def _test_sms(self):
        self._save_all()
        from services.sms_service import SMSService
        phone = self.company_phone.text() or "237697624219"
        success, result = SMSService.send_sms(phone, "Test HRFlow: SMS de vérification")
        if success:
            QMessageBox.information(self, "Succès", f"SMS envoyé avec succès !\n{result}")
        else:
            QMessageBox.warning(self, "Erreur", f"Échec de l'envoi : {result}")

    def refresh_data(self):
        pass
