"""Main application entry point."""
from database import init_db, SessionLocal
from models import User, Organization, Plugin


def main():
    """Initialize database and demonstrate basic usage."""
    print("Initializing LLMObs database...")
    
    # Initialize database tables
    init_db()
    print("✓ Database tables created successfully!")
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Example: Create a test user
        test_user = User(
            email="admin@llmobs.com",
            username="admin",
            hashed_password="hashed_password_here",  # In production, use proper password hashing
            is_superuser=True
        )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == test_user.email).first()
        if not existing_user:
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"✓ Created test user: {test_user}")
        else:
            print(f"✓ User already exists: {existing_user}")
        
        # Query example
        user_count = db.query(User).count()
        print(f"✓ Total users in database: {user_count}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n" + "="*50)
    print("Database setup complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure your database")
    print("2. Run migrations: alembic revision --autogenerate -m 'Initial migration'")
    print("3. Apply migrations: alembic upgrade head")


if __name__ == "__main__":
    main()
