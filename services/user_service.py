from models.base import SessionLocal
from models.user import User


class UserService:
    @staticmethod
    def create(username, password, role="manager"):
        session = SessionLocal()
        try:
            user = User(username=username, role=role)
            user.set_password(password)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def authenticate(username, password):
        session = SessionLocal()
        try:
            user = session.query(User).filter(
                User.username == username,
                User.actif == True
            ).first()
            if user and user.check_password(password):
                return user
            return None
        finally:
            session.close()

    @staticmethod
    def get_all():
        session = SessionLocal()
        try:
            return session.query(User).order_by(User.username).all()
        finally:
            session.close()

    @staticmethod
    def exists():
        session = SessionLocal()
        try:
            return session.query(User).count() > 0
        finally:
            session.close()

    @staticmethod
    def create_default_admin():
        session = SessionLocal()
        try:
            admin = session.query(User).filter(User.username == "admin").first()
            if not admin:
                admin = User(username="admin", role="admin")
                admin.set_password("admin123")
                session.add(admin)
                session.commit()
                return True
            return False
        finally:
            session.close()
