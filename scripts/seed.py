import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from app.db.session import engine, init_db
from app.models.domain import User, UserRole, Weakness
from app.core.security import get_password_hash
from sqlmodel import Session, select

def seed():
    init_db()
    with Session(engine) as db:
        admin_email = "admin@kessel.local"
        if not db.exec(select(User).where(User.email == admin_email)).first():
            # Injected with 1987 password logic
            admin = User(email=admin_email, password_hash=get_password_hash("1987"), role=UserRole.ADMIN)
            db.add(admin)
            db.commit()
            print("✅ 1987 Admin Seeded successfully.")
if __name__ == "__main__":
    seed()
