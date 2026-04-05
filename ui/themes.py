DARK_THEME = """
QMainWindow, QWidget {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: 'Segoe UI', sans-serif;
}

QLabel {
    color: #e6edf3;
    background: transparent;
    border: none;
}

QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e6edf3;
    font-size: 13px;
    selection-background-color: #58a6ff;
}

QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {
    border: 1px solid #58a6ff;
}

QComboBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e6edf3;
    font-size: 13px;
    min-width: 120px;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #8b949e;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #161b22;
    border: 1px solid #30363d;
    color: #e6edf3;
    selection-background-color: #1f6feb;
}

QPushButton {
    background-color: #238636;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
    min-height: 18px;
}

QPushButton:hover {
    background-color: #2ea043;
}

QPushButton:pressed {
    background-color: #1a7f37;
}

QPushButton[class="danger"] {
    background-color: #f85149;
}

QPushButton[class="danger"]:hover {
    background-color: #f85149;
}

QPushButton[class="secondary"] {
    background-color: #484f58;
    color: #e6edf3;
}

QPushButton[class="secondary"]:hover {
    background-color: #3d444d;
}

QPushButton[class="accent"] {
    background-color: #1f6feb;
}

QPushButton[class="accent"]:hover {
    background-color: #388bfd;
}

QTableWidget, QTableView {
    background-color: #0d1117;
    alternate-background-color: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    gridline-color: #21262d;
    color: #e6edf3;
    font-size: 12px;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
}

QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #21262d;
}

QTableWidget QPushButton {
    padding: 2px;
    min-height: 0px;
    min-width: 0px;
    font-size: 12px;
    border-radius: 6px;
}

QHeaderView::section {
    background-color: #161b22;
    color: #8b949e;
    font-weight: bold;
    font-size: 11px;
    padding: 8px 10px;
    border: none;
    border-bottom: 2px solid #30363d;
    text-transform: uppercase;
}

QScrollBar:vertical {
    background-color: #0d1117;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #30363d;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #484f58;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #0d1117;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #30363d;
    border-radius: 4px;
    min-width: 30px;
}

QDialog {
    background-color: #161b22;
    border-radius: 12px;
}

QGroupBox {
    border: 1px solid #30363d;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #8b949e;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

QTabWidget::pane {
    border: 1px solid #30363d;
    border-radius: 8px;
    background-color: #0d1117;
}

QTabBar::tab {
    background-color: #161b22;
    color: #8b949e;
    padding: 8px 20px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
}

QTabBar::tab:selected {
    color: #e6edf3;
    border-bottom: 2px solid #58a6ff;
}

QTabBar::tab:hover {
    color: #e6edf3;
}

QMessageBox {
    background-color: #161b22;
}

QMessageBox QLabel {
    color: #e6edf3;
}

QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #21262d;
    text-align: center;
    color: #e6edf3;
    font-size: 11px;
    height: 12px;
}

QProgressBar::chunk {
    border-radius: 6px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #238636, stop:1 #58a6ff);
}

QToolTip {
    background-color: #1c2128;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
}
"""

LIGHT_THEME = """
QMainWindow, QWidget {
    background-color: #f6f8fa;
    color: #24292f;
    font-family: 'Segoe UI', sans-serif;
}

QLabel {
    color: #24292f;
    background: transparent;
    border: none;
}

QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    padding: 8px 12px;
    color: #24292f;
    font-size: 13px;
    selection-background-color: #0969da;
}

QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {
    border: 1px solid #0969da;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    padding: 8px 12px;
    color: #24292f;
    font-size: 13px;
    min-width: 120px;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #57606a;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    color: #24292f;
    selection-background-color: #0969da;
    selection-color: #ffffff;
}

QPushButton {
    background-color: #2da44e;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
    min-height: 18px;
}

QPushButton:hover {
    background-color: #218838;
}

QPushButton:pressed {
    background-color: #1a7f37;
}

QPushButton[class="danger"] {
    background-color: #cf222e;
}

QPushButton[class="danger"]:hover {
    background-color: #a40e26;
}

QPushButton[class="secondary"] {
    background-color: #eaeef2;
    color: #24292f;
    border: 1px solid #d0d7de;
}

QPushButton[class="secondary"]:hover {
    background-color: #d0d7de;
}

QPushButton[class="accent"] {
    background-color: #0969da;
}

QPushButton[class="accent"]:hover {
    background-color: #0550ae;
}

QTableWidget, QTableView {
    background-color: #ffffff;
    alternate-background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    gridline-color: #d8dee4;
    color: #24292f;
    font-size: 12px;
    selection-background-color: #0969da;
    selection-color: #ffffff;
}

QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #d8dee4;
}

QTableWidget QPushButton {
    padding: 2px;
    min-height: 0px;
    min-width: 0px;
    font-size: 12px;
    border-radius: 6px;
}

QHeaderView::section {
    background-color: #f6f8fa;
    color: #57606a;
    font-weight: bold;
    font-size: 11px;
    padding: 8px 10px;
    border: none;
    border-bottom: 2px solid #d0d7de;
    text-transform: uppercase;
}

QScrollBar:vertical {
    background-color: #f6f8fa;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #d0d7de;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #afb8c1;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #f6f8fa;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #d0d7de;
    border-radius: 4px;
    min-width: 30px;
}

QDialog {
    background-color: #ffffff;
    border-radius: 12px;
}

QGroupBox {
    border: 1px solid #d0d7de;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #57606a;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

QTabWidget::pane {
    border: 1px solid #d0d7de;
    border-radius: 8px;
    background-color: #ffffff;
}

QTabBar::tab {
    background-color: #f6f8fa;
    color: #57606a;
    padding: 8px 20px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
}

QTabBar::tab:selected {
    color: #24292f;
    border-bottom: 2px solid #0969da;
}

QTabBar::tab:hover {
    color: #24292f;
}

QMessageBox {
    background-color: #ffffff;
}

QMessageBox QLabel {
    color: #24292f;
}

QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #eaeef2;
    text-align: center;
    color: #24292f;
    font-size: 11px;
    height: 12px;
}

QProgressBar::chunk {
    border-radius: 6px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2da44e, stop:1 #0969da);
}

QToolTip {
    background-color: #ffffff;
    color: #24292f;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
}
"""

SIDEBAR_DARK = """
QFrame#sidebar {
    background-color: #010409;
    border-right: 1px solid #21262d;
}

QPushButton.nav-btn {
    background-color: transparent;
    color: #8b949e;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: normal;
}

QPushButton.nav-btn:hover {
    background-color: #161b22;
    color: #e6edf3;
}

QPushButton.nav-btn[active="true"] {
    background-color: #1f6feb;
    color: #ffffff;
    font-weight: bold;
}
"""

SIDEBAR_LIGHT = """
QFrame#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #d0d7de;
}

QPushButton.nav-btn {
    background-color: transparent;
    color: #57606a;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: normal;
}

QPushButton.nav-btn:hover {
    background-color: #f6f8fa;
    color: #24292f;
}

QPushButton.nav-btn[active="true"] {
    background-color: #0969da;
    color: #ffffff;
    font-weight: bold;
}
"""


def get_theme(theme_name):
    if theme_name == "light":
        return LIGHT_THEME + SIDEBAR_LIGHT
    return DARK_THEME + SIDEBAR_DARK
