from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# SQLite Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.String(50), unique=True)
    patient_name = db.Column(db.String(100))
    doctor = db.Column(db.String(100))
    date = db.Column(db.String(20))
    medicines = db.Column(db.Text)
    instructions = db.Column(db.Text)

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# API Routes
@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    try:
        data = request.json
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
        
        # Sample prescription
        prescriptions = {
            "Dr. Smith": {"medicines": "Aspirin 100mg, Atorvastatin 20mg", "instructions": "Take after meals, twice daily"},
            "Dr. Johnson": {"medicines": "Paracetamol 500mg, Ibuprofen 400mg", "instructions": "Take when needed"},
            "Dr. Williams": {"medicines": "Amoxicillin 250mg, Vitamin D drops", "instructions": "Complete full course"}
        }
        
        prescription = Prescription(
            appointment_id=data['id'],
            patient_name=data['patientName'],
            doctor=data['doctor'],
            date=data['date'],
            medicines=prescriptions.get(data['doctor'], {}).get('medicines', 'Regular checkup'),
            instructions=prescriptions.get(data['doctor'], {}).get('instructions', 'As directed')
        )
        db.session.add(prescription)
        db.session.commit()
        
        return jsonify({"message": "Appointment booked successfully!", "id": appointment.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/prescription/<appointment_id>', methods=['GET'])
def get_prescription(appointment_id):
    prescription = Prescription.query.filter_by(appointment_id=appointment_id).first()
    if prescription:
        return jsonify({
            'appointmentId': prescription.appointment_id,
            'patientName': prescription.patient_name,
            'doctor': prescription.doctor,
            'date': prescription.date,
            'medicines': prescription.medicines,
            'instructions': prescription.instructions
        })
    return jsonify({"error": "Prescription not found"}), 404

@app.route('/api/doctors/timings', methods=['GET'])
def get_timings():
    timings = {
        "Dr. Smith": {"Monday": "9-5", "Tuesday": "9-5", "Wednesday": "9-5", "Thursday": "9-5", "Friday": "9-5", "Saturday": "10-2"},
        "Dr. Johnson": {"Monday": "10-6", "Tuesday": "10-6", "Wednesday": "10-6", "Thursday": "10-6", "Friday": "10-6", "Saturday": "Closed"},
        "Dr. Williams": {"Monday": "8-4", "Tuesday": "8-4", "Wednesday": "8-4", "Thursday": "8-4", "Friday": "8-4", "Saturday": "9-1"}
    }
    return jsonify(timings)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "database": "SQLite", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏥 MediCare Healthcare App")
    print("📍 Running on: http://localhost:5000")
    print("💾 Database: SQLite (healthcare.db)")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)