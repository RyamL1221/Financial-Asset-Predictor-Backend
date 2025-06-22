import os
import bcrypt
import pymysql
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

register_bp = Blueprint('register', __name__, url_prefix='/api/register')

def get_db_connection():
    """Create and return a MySQL database connection"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'financial_predictor'),
            port=int(os.getenv('DB_PORT', 3306)),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def create_users_table(connection):
    """Create the users table if it doesn't exist"""
    try:
        with connection.cursor() as cursor:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_sql)
            connection.commit()
            return True
    except Exception as e:
        print(f"Error creating users table: {e}")
        return False

@register_bp.route('/', methods=['POST'])
def register():
    """Register a new user"""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if not isinstance(email, str) or not isinstance(password, str):
            return jsonify({'error': 'Email and password must be strings'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Connect to database
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Create users table if it doesn't exist
        if not create_users_table(connection):
            connection.close()
            return jsonify({'error': 'Failed to create users table'}), 500
        
        # Check if user already exists
        with connection.cursor() as cursor:
            check_user_sql = "SELECT id FROM users WHERE email = %s"
            cursor.execute(check_user_sql, (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                connection.close()
                return jsonify({'error': 'User with this email already exists'}), 409
        
        # Hash the password
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt)
        
        # Insert new user
        with connection.cursor() as cursor:
            insert_user_sql = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
            cursor.execute(insert_user_sql, (email, password_hash.decode('utf-8')))
            connection.commit()
            
            user_id = cursor.lastrowid
        
        connection.close()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'email': email
        }), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@register_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the register service"""
    return jsonify({'status': 'healthy', 'service': 'register'}), 200 