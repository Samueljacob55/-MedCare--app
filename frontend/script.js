// API Configuration
const API_URL = 'http://localhost:5000/api';

// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ MediCare Frontend Loaded');
    testBackendConnection();
    
    // Setup form submission
    const appointmentForm = document.getElementById('appointmentForm');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', bookAppointment);
    }
    
    const prescriptionForm = document.getElementById('prescriptionForm');
    if (prescriptionForm) {
        prescriptionForm.addEventListener('submit', getPrescription);
    }
});

// Test backend connection
async function testBackendConnection() {
    try {
        const response = await fetch(`http://localhost:5000/health`);
        if (response.ok) {
            console.log('✅ Backend connected');
            showNotification('Connected to server', 'success');
        } else {
            showNotification('Server connection failed', 'error');
        }
    } catch (error) {
        console.error('Backend not reachable');
    }
}

// Book Appointment
async function bookAppointment(event) {
    event.preventDefault();
    
    const appointment = {
        id: Date.now().toString(),
        patientName: document.getElementById('patientName').value,
        patientEmail: document.getElementById('patientEmail').value,
        patientPhone: document.getElementById('patientPhone').value,
        doctor: document.getElementById('doctor').value,
        date: document.getElementById('appointmentDate').value,
        time: document.getElementById('appointmentTime').value
    };
    
    const submitBtn = event.target.querySelector('.btn-primary');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Booking...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/appointments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(appointment)
        });
        
        if (response.ok) {
            showNotification(
                `✅ Appointment booked successfully!\nID: ${appointment.id}\nDoctor: ${appointment.doctor}`,
                'success'
            );
            document.getElementById('appointmentForm').reset();
        } else {
            throw new Error('Booking failed');
        }
    } catch (error) {
        showNotification('Failed to book appointment', 'error');
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

// Get Prescription
async function getPrescription(event) {
    event.preventDefault();
    const appointmentId = document.getElementById('prescriptionId').value;
    
    try {
        const response = await fetch(`${API_URL}/prescription/${appointmentId}`);
        if (response.ok) {
            const prescription = await response.json();
            displayPrescription(prescription);
            showNotification('Prescription found!', 'success');
        } else {
            throw new Error('Not found');
        }
    } catch (error) {
        showNotification('No prescription found for this ID', 'error');
    }
}

function displayPrescription(prescription) {
    const detailsDiv = document.getElementById('prescriptionDetails');
    detailsDiv.innerHTML = `
        <div style="background: white; border-radius: 20px; padding: 2rem; margin-top: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <h3 style="color: #667eea; margin-bottom: 1rem;">📋 Prescription Details</h3>
            <p><strong>Patient:</strong> ${prescription.patientName}</p>
            <p><strong>Doctor:</strong> ${prescription.doctor}</p>
            <p><strong>Medicines:</strong> ${prescription.medicines}</p>
            <p><strong>Instructions:</strong> ${prescription.instructions}</p>
        </div>
    `;
}

function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active-section');
        section.style.display = 'none';
    });
    
    const selectedSection = document.getElementById(sectionId);
    selectedSection.style.display = 'block';
    setTimeout(() => selectedSection.classList.add('active-section'), 10);
    
    // Update active nav button
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i> ${message}`;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 4000);
}