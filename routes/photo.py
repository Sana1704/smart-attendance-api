# routes/photo.py
import os
from flask import Blueprint, request, jsonify, current_app
from utils.db import get_db_connection

photo_bp = Blueprint('photo_bp', __name__)

@photo_bp.route('/upload-photo', methods=['POST'])
def upload_photo():
    emp_id = request.form.get('emp_id')
    photo = request.files.get('photo')
    if not emp_id or not photo:
        return jsonify({'error': 'Missing emp_id or photo'}), 400

    path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{emp_id}_{photo.filename}")
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    photo.save(path)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for i in range(1, 21):
            col = f"photo_path_{i}"
            cursor.execute(f"SELECT {col} FROM employees WHERE emp_id = %s", (emp_id,))
            val = cursor.fetchone()
            if val is None or not val[0]:
                cursor.execute(f"UPDATE employees SET {col} = %s WHERE emp_id = %s", (path, emp_id))
                conn.commit()
                return jsonify({'message': f'Stored in {col}'})
        return jsonify({'error': 'All photo columns used'}), 400
    finally:
        cursor.close()
        conn.close()
