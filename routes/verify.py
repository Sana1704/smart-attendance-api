# routes/verify.py
import cv2
import os
import numpy as np
from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from skimage.metrics import structural_similarity as ssim
from datetime import datetime

verify_bp = Blueprint('verify_bp', __name__)

@verify_bp.route('/verify', methods=['GET'])
def run_verification():
    emp_id = request.args.get('emp_id')
    if not emp_id:
        return jsonify({'error': 'Missing emp_id'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    stored_images = []
    try:
        for i in range(1, 21):
            col = f"photo_path_{i}"
            cursor.execute(f"SELECT {col} FROM employees WHERE emp_id = %s", (emp_id,))
            row = cursor.fetchone()
            if row and row[0]:
                img = cv2.imread(row[0], cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    stored_images.append(cv2.resize(img, (200, 200)))
    finally:
        cursor.close()
        conn.close()

    if not stored_images:
        return jsonify({'error': 'No stored images'}), 404

    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if not ret:
        return jsonify({'error': 'Webcam failed'}), 500

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (200, 200))

    for img in stored_images:
        score, _ = ssim(resized, img, full=True)
        if score > 0.15:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE employees SET last_verified = %s WHERE emp_id = %s", (datetime.now(), emp_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'verified': True, 'score': score})

    return jsonify({'verified': False})
