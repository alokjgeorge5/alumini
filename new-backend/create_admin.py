import bcrypt
from app.models import get_engine
from sqlalchemy import text

def create_admin_user(email, password, name="Admin User"):
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    engine = get_engine()
    try:
        with engine.connect() as conn:
            # Check if admin already exists
            result = conn.execute(
                text("SELECT id FROM users WHERE email = :email"), 
                {"email": email}
            )
            if result.fetchone():
                print(f"Admin user with email {email} already exists")
                return
            
            # Create admin user
            conn.execute(
                text("""
                    INSERT INTO users (email, password_hash, name, role) 
                    VALUES (:email, :password_hash, :name, 'admin')
                """),
                {
                    "email": email,
                    "password_hash": password_hash,
                    "name": name
                }
            )
            conn.commit()
            print(f"Admin user created successfully with email: {email}")
            
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")

if __name__ == "__main__":
    import getpass
    
    print("Create Admin User")
    print("================")
    email = input("Admin email: ")
    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if password != confirm_password:
        print("Error: Passwords do not match")
    else:
        create_admin_user(email, password)
