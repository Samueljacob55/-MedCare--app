from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Fix for Python 3.14 compatibility
import pkgutil
import importlib

if not hasattr(pkgutil, 'get_loader'):
    def get_loader(module_name):
        spec = importlib.util.find_spec(module_name)
        return spec.loader if spec else None
    pkgutil.get_loader = get_loader

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "healthcare.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)

# Database Models
class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.String(50), primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_email = db.Column(db.String(100), nullable=False)
    patient_phone = db.Column(db.String(20), nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patientName': self.patient_name,
            'patientEmail': self.patient_email,
            'patientPhone': self.patient_phone,
            'doctor': self.doctor,
            'date': self.date,
            'time': self.time,
            'status': self.status,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.String(50), db.ForeignKey('appointments.id'), unique=True)
    patient_name = db.Column(db.String(100))
    doctor = db.Column(db.String(100))
    date = db.Column(db.String(20))
    medicines = db.Column(db.Text)
    instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'appointmentId': self.appointment_id,
            'patientName': self.patient_name,
            'doctor': self.doctor,
            'date': self.date,
            'medicines': self.medicines,
            'instructions': self.instructions
        }

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    specialization = db.Column(db.String(100))
    timings = db.Column(db.Text)  # JSON string of timings
    
    def to_dict(self):
        return {
            'name': self.name,
            'specialization': self.specialization,
            'timings': json.loads(self.timings) if self.timings else {}
        }

# Create tables
with app.app_context():
    db.create_all()
    
    # Seed doctors if not exists
    if Doctor.query.count() == 0:
        doctors_data = [
            {
                "name": "Dr. Smith",
                "specialization": "Cardiologist",
                "timings": json.dumps({
                    "Monday": "9-5", "Tuesday": "9-5", "Wednesday": "9-5",
                    "Thursday": "9-5", "Friday": "9-5", "Saturday": "10-2"
                })
            },
            {
                "name": "Dr. Johnson",
                "specialization": "Neurologist",
                "timings": json.dumps({
                    "Monday": "10-6", "Tuesday": "10-6", "Wednesday": "10-6",
                    "Thursday": "10-6", "Friday": "10-6", "Saturday": "Closed"
                })
            },
            {
                "name": "Dr. Williams",
                "specialization": "Pediatrician",
                "timings": json.dumps({
                    "Monday": "8-4", "Tuesday": "8-4", "Wednesday": "8-4",
                    "Thursday": "8-4", "Friday": "8-4", "Saturday": "9-1"
                })
            }
        ]
        for doctor_data in doctors_data:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
        db.session.commit()
        print("✅ Sample doctors added to database")

# Serve frontend
@app.route('/')
def serve_index():
    return send_file('../frontend/index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_file(f'../frontend/{path}')

# API Routes
@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
    return jsonify([app.to_dict() for app in appointments])

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    try:
        data = request.json
        
        # Create new appointment
        appointment = Appointment(
            id=data['id'],
            patient_name=data['patientName'],
            patient_email=data['patientEmail'],
            patient_phone=data['patientPhone'],
            doctor=data['doctor'],
            date=data['date'],
            time=data['time']
        )
        db.session.add(appointment)
        
        # Generate prescription
        sample_prescriptions = {
            "Dr. Smith": {
                "medicines": "Aspirin 100mg, Atorvastatin 20mg",
                "instructions": "Take after meals, twice daily"
            },
            "Dr. Johnson": {
                "medicines": "Paracetamol 500mg, Ibuprofen 400mg",
                "instructions": "Take when needed, not exceed 3 times daily"
            },
            "Dr. Williams": {
                "medicines": "Amoxicillin 250mg, Vitamin D drops",
                "instructions": "Complete full course of antibiotics"
            }
        }
        
        doc_prescription = sample_prescriptions.get(data['doctor'], sample_prescriptions["Dr. Smith"])
        
        prescription = Prescription(
            appointment_id=data['id'],
            patient_name=data['patientName'],
            doctor=data['doctor'],
            date=data['date'],
            medicines=doc_prescription['medicines'],
            instructions=doc_prescription['instructions']
        )
        db.session.add(prescription)
        
        db.session.commit()
        
        return jsonify({
            "message": "Appointment booked successfully",
            "id": appointment.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/prescription/<appointment_id>', methods=['GET'])
def get_prescription(appointment_id):
    prescription = Prescription.query.filter_by(appointment_id=appointment_id).first()
    if prescription:
        return jsonify(prescription.to_dict())
    return jsonify({"error": "Prescription not found"}), 404

@app.route('/api/prescription/<appointment_id>/download', methods=['GET'])
def download_prescription(appointment_id):
    prescription = Prescription.query.filter_by(appointment_id=appointment_id).first()
    if not prescription:
        return jsonify({"error": "Prescription not found"}), 404
    
    filename = f"prescription_{appointment_id}.pdf"
    filepath = os.path.join('/tmp', filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    c.drawString(100, 750, "Healthcare Appointment System")
    c.drawString(100, 730, "=" * 40)
    c.drawString(100, 700, f"Prescription for: {prescription.patient_name}")
    c.drawString(100, 680, f"Doctor: {prescription.doctor}")
    c.drawString(100, 660, f"Date: {prescription.date}")
    c.drawString(100, 630, "Medicines:")
    c.drawString(120, 610, prescription.medicines)
    c.drawString(100, 580, "Instructions:")
    c.drawString(120, 560, prescription.instructions)
    c.save()
    
    return send_file(filepath, as_attachment=True)

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([doc.to_dict() for doc in doctors])

@app.route('/api/doctors/timings', methods=['GET'])
def get_doctor_timings():
    doctors = Doctor.query.all()
    timings = {}
    for doctor in doctors:
        timings[doctor.name] = json.loads(doctor.timings) if doctor.timings else {}
    return jsonify(timings)

@app.route('/api/appointments/doctor/<doctor_name>', methods=['GET'])
def get_appointments_by_doctor(doctor_name):
    appointments = Appointment.query.filter_by(doctor=doctor_name).order_by(Appointment.date).all()
    return jsonify([app.to_dict() for app in appointments])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_appointments = Appointment.query.count()
    unique_patients = db.session.query(Appointment.patient_email).distinct().count()
    
    return jsonify({
        'total_appointments': total_appointments,
        'unique_patients': unique_patients,
        'doctors': Doctor.query.count()
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n{'='*50}")
    print(f"🏥 Healthcare App with Database")
    print(f"📍 Running on http://localhost:{port}")
    print(f"💾 Database: SQLite (healthcare.db)")
    print(f"{'='*50}\n")
    app.run(host='0.0.0.0', port=port, debug=True)