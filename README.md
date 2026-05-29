# MedCare App

A full-stack Healthcare Management Application deployed using DevOps tools and practices.

## Project Overview

MedCare App is a healthcare web application that allows users to:

* Book medical appointments
* View available medical services
* Download prescriptions
* Check doctor availability
* Manage healthcare-related information

The project demonstrates a complete DevOps workflow using:

* Docker
* Jenkins
* Kubernetes
* AWS EC2 VM

---

# Tech Stack

## Frontend

* HTML
* CSS
* JavaScript

## Backend

* Python
* Flask

## DevOps Tools

* Docker
* Jenkins
* Kubernetes
* AWS EC2
* GitHub

---

# Project Architecture

```text
User → Browser → Kubernetes Service → Flask Application → Database
```

---

# Project Structure

```text
medcare-app/
│
├── backend/
│   ├── app.py
│   ├── app_with_db.py
│   ├── healthcare.db
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── Dockerfile
├── Jenkinsfile
├── deployment.yaml
├── service.yaml
└── README.md
```

---

# Features

* Appointment Booking
* Medical Services Display
* Prescription Download
* Responsive Frontend UI
* Flask REST Backend
* Docker Containerization
* Jenkins CI/CD Pipeline
* Kubernetes Deployment
* AWS VM Hosting

---

# Docker Setup

## Build Docker Image

```bash
docker build -t medcare-app .
```

## Run Docker Container

```bash
docker run -d -p 5000:5000 medcare-app
```

## Access Application

```text
http://localhost:5000
```

---

# Jenkins CI/CD Pipeline

The Jenkins pipeline performs:

1. Clone GitHub Repository
2. Build Docker Image
3. Push Docker Image to DockerHub
4. Deploy Application to Kubernetes
5. Verify Deployment

---

# Kubernetes Deployment

## Apply Deployment

```bash
kubectl apply -f deployment.yaml
```

## Apply Service

```bash
kubectl apply -f service.yaml
```

## Check Pods

```bash
kubectl get pods
```

## Check Services

```bash
kubectl get svc
```

---

# Access Application on AWS EC2

```text
http://EC2_PUBLIC_IP:30007
```

Example:

```text
http://13.232.10.55:30007
```

---

# Jenkins Setup

## Install Jenkins

```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
sudo apt install jenkins -y
```

## Start Jenkins

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
```

## Access Jenkins

```text
http://EC2_PUBLIC_IP:8080
```

---

# Docker Installation

```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

---

# Kubernetes Installation

## Install Minikube

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

## Start Minikube

```bash
minikube start --driver=docker
```

---

# Health Check Endpoint

```python
@app.route('/health')
def health():
    return {"status": "healthy"}, 200
```

---

# Future Enhancements

* User Authentication
* Role-Based Access Control
* Database Integration
* Monitoring using Prometheus & Grafana
* HTTPS with Ingress
* Helm Charts
* Terraform Infrastructure Automation

---

# Author

Samuel 

---

# License

This project is developed for educational and DevOps learning purposes.
