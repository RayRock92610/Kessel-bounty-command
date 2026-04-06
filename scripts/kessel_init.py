import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from app.db.session import engine, Session, init_db
from app.models.domain import Role, Weakness, User
from app.core.security import get_password_hash
from sqlmodel import select

def run():
    # Ensure the tables exist first
    init_db()
    
    with Session(engine) as db:
        # 1. Create the Admin Role first (Foundation)
        admin_role = db.exec(select(Role).where(Role.name == 'Admin')).first()
        if not admin_role:
            print("🛡️ Creating Admin Role...")
            admin_role = Role(name='Admin', permissions={'all': True})
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        # 2. Create the 1987 Admin User
        admin_email = 'admin@kessel.local'
        # Query specifically for the email now that the schema is fresh
        admin_user = db.exec(select(User).where(User.email == admin_email)).first()
        
        if not admin_user:
            print(f"👤 Creating Admin User: {admin_email}")
            new_admin = User(
                email=admin_email,
                password_hash=get_password_hash('1987'),
                role_id=admin_role.id
            )
            db.add(new_admin)
        
        # 3. Seed Hunting Targets
        targets = [('Injection', 'sqli', 'SQLi', 89), ('Injection', 'xss', 'XSS', 79)]
        for f, s, n, cwe in targets:
            if not db.exec(select(Weakness).where(Weakness.slug == s)).first():
                db.add(Weakness(name=n, slug=s, family=f, cwe_id=cwe))
        
        db.commit()
        print('✅ Kessel initialized successfully with 17-entity logic.')

if __name__ == '__main__':
    run()
