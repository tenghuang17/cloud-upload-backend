# Cloud Upload Backend

A backend service for secure file uploads and asynchronous processing using cloud-native components.

This project demonstrates practical backend and cloud engineering experience, focusing on real-world system design, deployment, and integration with cloud services.

---

## Features

- Secure client-side file uploads using AWS S3 pre-signed URLs
- Asynchronous processing workflow using AWS SQS
- RESTful API built with Flask
- Containerized backend service deployed on a cloud platform
- Continuous integration validation using GitHub Actions

---

## Tech Stack

- Python
- Flask
- AWS S3 (Pre-signed URL)
- AWS SQS
- Docker
- GitHub Actions
- Linux
- Gunicorn

---

## System Flow

1. Client requests a pre-signed upload URL from the backend API
2. Backend generates an AWS S3 pre-signed URL
3. Client uploads the file directly to S3
4. Backend sends a message to AWS SQS
5. A worker service consumes the message and processes the uploaded file asynchronously

---

## Development & Deployment

The backend can be run locally by installing dependencies from the requirements file and starting the Flask application.  
For deployment, the service is containerized using Docker and deployed to a cloud hosting platform (Render).  
A minimal CI workflow is configured with GitHub Actions to validate builds on every code push.

---

## Purpose

This backend project is part of a cloud upload system and focuses on backend API design, cloud service integration, asynchronous processing, and deployment workflows in a real-world environment.

---

## 中文說明

此後端專案使用 Flask 建立 RESTful API，透過 AWS S3 Pre-signed URL 讓前端可直接將檔案上傳至雲端，降低後端負載，並搭配 AWS SQS 實作非同步處理流程。整個服務以 Docker 容器化並部署至雲端平台（Render），用於展示實際後端與雲端工程的系統設計與實務能力。
