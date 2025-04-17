# routes/employee.py
from flask import Blueprint, request, jsonify
from utils.db import get_db_connection

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/register', methods=['POST'])
def register_employee():
    data = request.json
    required_fields = ['emp_id', 'name', 'desig_id', 'designation', 'loc_id', 'location', 'shift_id', 'shift_name']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM employees WHERE emp_id = %s", (data['emp_id'],))
        if cursor.fetchone():
            return jsonify({'message': 'Employee already registered'})

        cursor.execute("""
            INSERT INTO employees (emp_id, name, desig_id, designation, loc_id, location, shift_id, shift_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(data[field] for field in required_fields))
        conn.commit()
        return jsonify({'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@employee_bp.route('/employees', methods=['GET'])
def list_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return jsonify([dict(zip(columns, row)) for row in rows])
    finally:
        cursor.close()
        conn.close()
