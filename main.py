import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QFont
from config import load_config, save_config


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setApplicationName("HRFlow")

    config = load_config()

    if not config.get("onboarding_done", False):
        from ui.onboarding import OnboardingScreen
        from ui.themes import get_theme

        app.setStyleSheet(get_theme("dark"))

        onboarding = OnboardingScreen()
        onboarding.setWindowTitle("HRFlow - Configuration initiale")
        onboarding.setMinimumSize(700, 550)

        def on_onboarding_finished(data):
            for key, val in data.items():
                if isinstance(val, dict) and key in config and isinstance(config[key], dict):
                    config[key].update(val)
                else:
                    config[key] = val
            save_config(config)

            try:
                from sqlalchemy import create_engine
                from config import get_db_url
                engine = create_engine(get_db_url(config))
                conn = engine.connect()
                conn.close()
            except Exception as e:
                QMessageBox.critical(
                    None, "Erreur de connexion",
                    f"Impossible de se connecter à PostgreSQL:\n{str(e)}\n\n"
                    "Vérifiez que PostgreSQL est en cours d'exécution et que la base de données existe."
                )
                return

            try:
                from models.base import Base, engine as db_engine
                from models import Employee, Attendance, Leave, Task, Salary, KPI, User
                Base.metadata.create_all(bind=db_engine)

                from services.user_service import UserService
                UserService.create_default_admin()
            except Exception as e:
                QMessageBox.critical(None, "Erreur", f"Erreur d'initialisation:\n{str(e)}")
                return

            onboarding.close()
            launch_main(app, config)

        onboarding.finished.connect(on_onboarding_finished)
        onboarding.show()
    else:
        try:
            from models.base import init_db
            init_db()
            from services.user_service import UserService
            UserService.create_default_admin()
        except Exception as e:
            QMessageBox.critical(
                None, "Erreur de connexion",
                f"Impossible de se connecter à la base de données:\n{str(e)}\n\n"
                "Vérifiez PostgreSQL et la configuration dans les paramètres."
            )
            config["onboarding_done"] = False
            save_config(config)
            from ui.onboarding import OnboardingScreen
            from ui.themes import get_theme
            app.setStyleSheet(get_theme("dark"))
            onboarding = OnboardingScreen()
            onboarding.setWindowTitle("HRFlow - Reconfiguration")
            onboarding.setMinimumSize(700, 550)

            def on_reconfig(data):
                for key, val in data.items():
                    if isinstance(val, dict) and key in config and isinstance(config[key], dict):
                        config[key].update(val)
                    else:
                        config[key] = val
                save_config(config)
                onboarding.close()
                os.execl(sys.executable, sys.executable, *sys.argv)

            onboarding.finished.connect(on_reconfig)
            onboarding.show()
            sys.exit(app.exec())
            return

        launch_main(app, config)

    sys.exit(app.exec())


def launch_main(app, config):
    from ui.main_window import MainWindow
    from ui.themes import get_theme

    window = MainWindow(config)
    window.show()


if __name__ == "__main__":
    main()
