from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QFrame,
                             QSizePolicy, QSpacerItem, QApplication)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

from ui.themes import get_theme
from ui.dashboard_page import DashboardPage
from ui.employee_page import EmployeePage
from ui.attendance_page import AttendancePage
from ui.leave_page import LeavePage
from ui.task_page import TaskPage
from ui.salary_page import SalaryPage
from ui.settings_page import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.current_theme = config.get("theme", "dark")
        self.nav_buttons = []
        self.setWindowTitle("HRFlow - Gestion des Ressources Humaines")
        self.setMinimumSize(1200, 750)
        self._build_ui()
        self._apply_theme(self.current_theme)
        self._navigate(0)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(4)

        logo_layout = QHBoxLayout()
        logo_icon = QLabel("🏢")
        logo_icon.setFont(QFont("Segoe UI Emoji", 20))
        logo_icon.setStyleSheet("background: transparent; border: none;")
        logo_layout.addWidget(logo_icon)

        logo_text = QLabel("HRFlow")
        logo_text.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        logo_text.setStyleSheet("color: #58a6ff; background: transparent; border: none;")
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        sidebar_layout.addLayout(logo_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #21262d; max-height: 1px; border: none;")
        sidebar_layout.addWidget(separator)
        sidebar_layout.addSpacing(10)

        nav_items = [
            ("📊", "Dashboard"),
            ("👥", "Employés"),
            ("⏰", "Présences"),
            ("📅", "Congés"),
            ("📋", "Tâches"),
            ("💰", "Salaires"),
            ("⚙️", "Paramètres"),
        ]

        for idx, (icon, label) in enumerate(nav_items):
            btn = QPushButton(f"  {icon}   {label}")
            btn.setFont(QFont("Segoe UI", 12))
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("class", "nav-btn")
            btn.clicked.connect(lambda checked, i=idx: self._navigate(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        version_label = QLabel("v1.0.0")
        version_label.setFont(QFont("Segoe UI", 9))
        version_label.setStyleSheet("color: #484f58; background: transparent; border: none;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(self.sidebar)

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.employee_page = EmployeePage()
        self.attendance_page = AttendancePage()
        self.leave_page = LeavePage()
        self.task_page = TaskPage()
        self.salary_page = SalaryPage()
        self.settings_page = SettingsPage()
        self.settings_page.theme_changed.connect(self._apply_theme)

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.employee_page)
        self.pages.addWidget(self.attendance_page)
        self.pages.addWidget(self.leave_page)
        self.pages.addWidget(self.task_page)
        self.pages.addWidget(self.salary_page)
        self.pages.addWidget(self.settings_page)

        main_layout.addWidget(self.pages)

    def _navigate(self, index):
        self.pages.setCurrentIndex(index)

        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        current_page = self.pages.currentWidget()
        if hasattr(current_page, "refresh_data"):
            try:
                current_page.refresh_data()
            except Exception:
                pass

    def _apply_theme(self, theme_name):
        self.current_theme = theme_name
        stylesheet = get_theme(theme_name)
        QApplication.instance().setStyleSheet(stylesheet)
