import os
from dotenv import load_dotenv
from database import SessionLocal
from models.user import User, UserRole
from core.security import hash_password

load_dotenv()

def seed_users():
    """Seed database with doctor and receptionist users."""
    db = SessionLocal()
    
    try:
        existing_doctor = db.query(User).filter(User.email == os.getenv("SEED_DOCTOR_EMAIL")).first()
        existing_receptionist = db.query(User).filter(User.email == os.getenv("SEED_RECEPTIONIST_EMAIL")).first()
        
        if existing_doctor and existing_receptionist:
            print("Seed users already exist in database.")
            return
        
        if not existing_doctor:
            doctor = User(
                name=os.getenv("SEED_DOCTOR_NAME"),
                email=os.getenv("SEED_DOCTOR_EMAIL"),
                phone=os.getenv("SEED_DOCTOR_PHONE"),
                role=UserRole.DOCTOR,
                password_hash=hash_password(os.getenv("SEED_DOCTOR_PASSWORD"))
            )
            db.add(doctor)
            print(f"Created doctor: {doctor.name}")
        
        if not existing_receptionist:
            receptionist = User(
                name=os.getenv("SEED_RECEPTIONIST_NAME"),
                email=os.getenv("SEED_RECEPTIONIST_EMAIL"),
                phone=os.getenv("SEED_RECEPTIONIST_PHONE"),
                role=UserRole.RECEPTIONIST,
                password_hash=hash_password(os.getenv("SEED_RECEPTIONIST_PASSWORD"))
            )
            db.add(receptionist)
            print(f"Created receptionist: {receptionist.name}")
        
        db.commit()
        print("Seed data inserted successfully.")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()