# 🗂️ Cloud Task Manager

A simple full-stack task management application built with **Flask**, **PostgreSQL**, and **Docker**, deployed on an **AWS EC2 instance**. The project is designed with a focus on **cloud engineering** and **DevOps practices**.

### 🌐 Live Demo

Access the live version at:  
👉 [http://18.225.235.157:8080](http://18.225.235.157:8080)

---

## 🛠️ Features

- 🧠 Flask REST API for managing tasks
- 🗄️ PostgreSQL as a database service
- 📦 Docker containers for API, DB, and frontend
- 📁 HTML frontend served with Nginx or directly from a mounted volume
- ⚙️ CI pipeline with GitHub Actions
- ☁️ Deployed on AWS EC2 with security groups and `.env` management

---

## 📁 Project Structure
cloud-task-manager/
├── backend/ # Flask app and Dockerfile
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
├── frontend/ # Static frontend
│ ├── index.html
│ └── config.js
├── .env # Environment variables
├── docker-compose.yml # Multi-service container config
└── .github/workflows/ci.yml # GitHub Actions CI workflow
