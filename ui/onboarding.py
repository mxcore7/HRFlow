from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QComboBox, QStackedWidget)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient


class OnboardingScreen(QWidget):
    finished = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.current_step = 0
        self.config_data = {}
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self._build_welcome_page()
        self._build_db_page()
        self._build_company_page()
        self._build_ready_page()

    def _build_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        icon_label = QLabel("🏢")
        icon_label.setFont(QFont("Segoe UI Emoji", 60))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        title = QLabel("Bienvenue dans HRFlow")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #58a6ff;")
        layout.addWidget(title)

        subtitle = QLabel("Votre solution complète de gestion des ressources humaines")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #8b949e;")
        layout.addWidget(subtitle)

        features = [
            "👥  Gestion des employés et badges",
            "⏰  Suivi de présence intelligent",
            "📊  KPI et performance automatisés",
            "💰  Calcul de salaires et fiches de paie",
        ]
        for feat in features:
            fl = QLabel(feat)
            fl.setFont(QFont("Segoe UI", 12))
            fl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fl.setStyleSheet("color: #c9d1d9; padding: 4px;")
            layout.addWidget(fl)

        layout.addSpacing(30)
        btn = QPushButton("Commencer la configuration  →")
        btn.setFixedWidth(300)
        btn.setFixedHeight(45)
        btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stack.addWidget(page)

    def _build_db_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("🗄️  Configuration de la base de données")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(10)

        form = QWidget()
        form.setFixedWidth(400)
        fl = QVBoxLayout(form)
        fl.setSpacing(12)

        self.db_host = QLineEdit()
        self.db_host.setPlaceholderText("Hôte (ex: localhost)")
        self.db_host.setText("localhost")
        fl.addWidget(QLabel("Hôte"))
        fl.addWidget(self.db_host)

        self.db_port = QLineEdit()
        self.db_port.setPlaceholderText("Port (ex: 5432)")
        self.db_port.setText("5432")
        fl.addWidget(QLabel("Port"))
        fl.addWidget(self.db_port)

        self.db_name = QLineEdit()
        self.db_name.setPlaceholderText("Nom de la base")
        self.db_name.setText("hrflow")
        fl.addWidget(QLabel("Base de données"))
        fl.addWidget(self.db_name)

        self.db_user = QLineEdit()
        self.db_user.setPlaceholderText("Utilisateur")
        self.db_user.setText("postgres")
        fl.addWidget(QLabel("Utilisateur"))
        fl.addWidget(self.db_user)

        self.db_password = QLineEdit()
        self.db_password.setPlaceholderText("Mot de passe")
        self.db_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.db_password.setText("postgres")
        fl.addWidget(QLabel("Mot de passe"))
        fl.addWidget(self.db_password)

        layout.addWidget(form, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_layout = QHBoxLayout()
        back_btn = QPushButton("← Retour")
        back_btn.setProperty("class", "secondary")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_layout.addWidget(back_btn)

        next_btn = QPushButton("Suivant →")
        next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_btn.clicked.connect(self._save_db_and_next)
        btn_layout.addWidget(next_btn)
        layout.addLayout(btn_layout)

        self.stack.addWidget(page)

    def _build_company_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("🏢  Informations de l'entreprise")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(10)

        form = QWidget()
        form.setFixedWidth(400)
        fl = QVBoxLayout(form)
        fl.setSpacing(12)

        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Nom de l'entreprise")
        fl.addWidget(QLabel("Nom de l'entreprise"))
        fl.addWidget(self.company_name)

        self.company_address = QLineEdit()
        self.company_address.setPlaceholderText("Adresse")
        fl.addWidget(QLabel("Adresse"))
        fl.addWidget(self.company_address)

        self.company_phone = QLineEdit()
        self.company_phone.setPlaceholderText("Téléphone")
        fl.addWidget(QLabel("Téléphone"))
        fl.addWidget(self.company_phone)

        fl.addWidget(QLabel("Thème"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Sombre", "Clair"])
        fl.addWidget(self.theme_combo)

        layout.addWidget(form, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_layout = QHBoxLayout()
        back_btn = QPushButton("← Retour")
        back_btn.setProperty("class", "secondary")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_layout.addWidget(back_btn)

        next_btn = QPushButton("Suivant →")
        next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_btn.clicked.connect(self._save_company_and_next)
        btn_layout.addWidget(next_btn)
        layout.addLayout(btn_layout)

        self.stack.addWidget(page)

    def _build_ready_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        icon_label = QLabel("🚀")
        icon_label.setFont(QFont("Segoe UI Emoji", 60))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        title = QLabel("Tout est prêt !")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #238636;")
        layout.addWidget(title)

        subtitle = QLabel("HRFlow est configuré et prêt à être utilisé.\nUn compte admin par défaut a été créé : admin / admin123")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #8b949e;")
        layout.addWidget(subtitle)

        layout.addSpacing(30)
        btn = QPushButton("Lancer HRFlow  🎉")
        btn.setFixedWidth(300)
        btn.setFixedHeight(45)
        btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._finish)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stack.addWidget(page)

    def _save_db_and_next(self):
        self.config_data["database"] = {
            "host": self.db_host.text(),
            "port": int(self.db_port.text() or 5432),
            "name": self.db_name.text(),
            "user": self.db_user.text(),
            "password": self.db_password.text()
        }
        self.stack.setCurrentIndex(2)

    def _save_company_and_next(self):
        self.config_data["company"] = {
            "name": self.company_name.text(),
            "address": self.company_address.text(),
            "phone": self.company_phone.text()
        }
        self.config_data["theme"] = "light" if self.theme_combo.currentIndex() == 1 else "dark"
        self.stack.setCurrentIndex(3)

    def _finish(self):
        self.config_data["onboarding_done"] = True
        self.finished.emit(self.config_data)
