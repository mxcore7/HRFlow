from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QGridLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime, date
from services.employee_service import EmployeeService
from services.attendance_service import AttendanceService
from services.task_service import TaskService
from services.leave_service import LeaveService


class StatCard(QFrame):
    def __init__(self, title, value, icon, color="#58a6ff"):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(22, 27, 34, 0.8);
                border: 1px solid #21262d;
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(120)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        left = QVBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Segoe UI", 11))
        title_lbl.setStyleSheet("color: #8b949e; border: none; background: transparent;")
        left.addWidget(title_lbl)

        self.value_lbl = QLabel(str(value))
        self.value_lbl.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.value_lbl.setStyleSheet(f"color: {color}; border: none; background: transparent;")
        left.addWidget(self.value_lbl)
        layout.addLayout(left)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont("Segoe UI Emoji", 32))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_lbl)

    def update_value(self, value):
        self.value_lbl.setText(str(value))


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        header = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()

        now = datetime.now()
        date_lbl = QLabel(now.strftime("%A %d %B %Y"))
        date_lbl.setFont(QFont("Segoe UI", 12))
        date_lbl.setStyleSheet("color: #8b949e;")
        header.addWidget(date_lbl)
        layout.addLayout(header)

        self.cards_grid = QGridLayout()
        self.cards_grid.setSpacing(15)

        self.card_employees = StatCard("Employés actifs", "0", "👥", "#58a6ff")
        self.card_present = StatCard("Présents aujourd'hui", "0", "✅", "#238636")
        self.card_tasks = StatCard("Tâches en cours", "0", "📋", "#d29922")
        self.card_leaves = StatCard("Congés en attente", "0", "📅", "#e94560")

        self.cards_grid.addWidget(self.card_employees, 0, 0)
        self.cards_grid.addWidget(self.card_present, 0, 1)
        self.cards_grid.addWidget(self.card_tasks, 1, 0)
        self.cards_grid.addWidget(self.card_leaves, 1, 1)
        layout.addLayout(self.cards_grid)

        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)

        self.chart_frame_1 = QFrame()
        self.chart_frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.chart_frame_1.setStyleSheet("""
            QFrame {
                background-color: rgba(22, 27, 34, 0.8);
                border: 1px solid #21262d;
                border-radius: 12px;
            }
        """)
        self.chart_layout_1 = QVBoxLayout(self.chart_frame_1)
        self.chart_layout_1.setContentsMargins(15, 15, 15, 15)
        chart_title_1 = QLabel("📊 Répartition des tâches")
        chart_title_1.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        chart_title_1.setStyleSheet("border: none; background: transparent;")
        self.chart_layout_1.addWidget(chart_title_1)
        charts_layout.addWidget(self.chart_frame_1)

        self.chart_frame_2 = QFrame()
        self.chart_frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.chart_frame_2.setStyleSheet("""
            QFrame {
                background-color: rgba(22, 27, 34, 0.8);
                border: 1px solid #21262d;
                border-radius: 12px;
            }
        """)
        self.chart_layout_2 = QVBoxLayout(self.chart_frame_2)
        self.chart_layout_2.setContentsMargins(15, 15, 15, 15)
        chart_title_2 = QLabel("📈 Présence cette semaine")
        chart_title_2.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        chart_title_2.setStyleSheet("border: none; background: transparent;")
        self.chart_layout_2.addWidget(chart_title_2)
        charts_layout.addWidget(self.chart_frame_2)

        layout.addLayout(charts_layout)

        try:
            self._load_charts()
        except Exception:
            pass

        layout.addStretch()

    def _load_charts(self):
        try:
            import matplotlib
            matplotlib.use('Agg')
            from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
            from matplotlib.figure import Figure

            fig1 = Figure(figsize=(4, 3), facecolor='#161b22')
            ax1 = fig1.add_subplot(111)
            try:
                from models.base import SessionLocal
                from models.task import Task as TaskModel
                session = SessionLocal()
                statuts = ["assigne", "en_cours", "termine", "livre", "annule"]
                counts = []
                for s in statuts:
                    counts.append(session.query(TaskModel).filter(TaskModel.statut == s).count())
                session.close()
                labels_map = {"assigne": "Assigné", "en_cours": "En cours", "termine": "Terminé", "livre": "Livré", "annule": "Annulé"}
                non_zero = [(labels_map[s], c) for s, c in zip(statuts, counts) if c > 0]
                if non_zero:
                    labels, values = zip(*non_zero)
                    colors = ["#58a6ff", "#d29922", "#238636", "#1f6feb", "#da3633"]
                    ax1.pie(values, labels=labels, colors=colors[:len(values)], autopct='%1.0f%%',
                            textprops={'color': '#e6edf3', 'fontsize': 8})
                else:
                    ax1.text(0.5, 0.5, "Aucune tâche", ha='center', va='center', color='#8b949e', fontsize=10, transform=ax1.transAxes)
            except Exception:
                ax1.text(0.5, 0.5, "Aucune donnée", ha='center', va='center', color='#8b949e', fontsize=10, transform=ax1.transAxes)
            ax1.set_facecolor('#161b22')
            canvas1 = FigureCanvasQTAgg(fig1)
            canvas1.setStyleSheet("border: none; background: transparent;")
            self.chart_layout_1.addWidget(canvas1)

            fig2 = Figure(figsize=(4, 3), facecolor='#161b22')
            ax2 = fig2.add_subplot(111)
            try:
                from models.base import SessionLocal
                from models.attendance import Attendance
                from datetime import timedelta
                session = SessionLocal()
                today = date.today()
                days = []
                counts = []
                for i in range(6, -1, -1):
                    d = today - timedelta(days=i)
                    c = session.query(Attendance).filter(Attendance.date == d).count()
                    days.append(d.strftime("%a"))
                    counts.append(c)
                session.close()
                ax2.bar(days, counts, color='#238636', width=0.6, edgecolor='none')
                ax2.set_facecolor('#161b22')
                ax2.tick_params(colors='#8b949e', labelsize=8)
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['bottom'].set_color('#30363d')
                ax2.spines['left'].set_color('#30363d')
            except Exception:
                ax2.text(0.5, 0.5, "Aucune donnée", ha='center', va='center', color='#8b949e', fontsize=10, transform=ax2.transAxes)
            canvas2 = FigureCanvasQTAgg(fig2)
            canvas2.setStyleSheet("border: none; background: transparent;")
            self.chart_layout_2.addWidget(canvas2)
        except ImportError:
            pass

    def refresh_data(self):
        try:
            self.card_employees.update_value(EmployeeService.count())
            self.card_present.update_value(AttendanceService.count_today())
            self.card_tasks.update_value(TaskService.count_active())
            self.card_leaves.update_value(LeaveService.count_pending())
        except Exception:
            pass
