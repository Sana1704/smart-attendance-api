# app.py
from flask import Flask
from routes.employee import employee_bp
from routes.photo import photo_bp
from routes.verify import verify_bp
from flasgger import Swagger
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SWAGGER'] = {
    'title': 'Smart Attendance API',
    'uiversion': 3
}
Swagger(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register API Blueprints
app.register_blueprint(employee_bp, url_prefix='/api')
app.register_blueprint(photo_bp, url_prefix='/api')
app.register_blueprint(verify_bp, url_prefix='/api')

@app.route('/')
def index():
    return {
        'message': 'Welcome to Smart Attendance API',
        'routes': [
            '/api/register',
            '/api/employees',
            '/api/upload-photo',
            '/api/verify?emp_id=123'
        ]
    }

if __name__ == '__main__':
    app.run(debug=True, port=5001)

