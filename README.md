<h2 align="center">Image Compression Service Overview</h2>

### Overview:

This document describes the architecture, components, and usage of an image compression service built with FastAPI, MongoDB, Celery, Docker, and MinIO.

This document outlines the design and functionality of an image compression service built using FastAPI, MongoDB, Celery, Docker, and MinIO. The service offers a robust platform for uploading CSV files containing image data, initiating asynchronous image compression tasks, checking task statuses, and downloading compressed images.

### Architecture Diagram:

<image src="https://github.com/Arvind-4/image-compressor/blob/main/.gitbook/diagram.png" alt="Architecture Diagram" />

### Quick Start:

Run the application using docker. The services running are:

- **API Service**: Exposed on port 8000, accessible via http://0.0.0.0:8000.
- **MongoDB**: Exposed on port 27017, accessible via mongodb://0.0.0.0:27017.
- **Mongo Express**: Exposed on port 8081, accessible via http://0.0.0.0:8081 for MongoDB management. (Auth credentials are **username** is **admin** and **password** is **password**)
- **Redis**: Exposed on port 6379, accessible via redis://0.0.0.0:6379.
- **MinIO**:
  - Main server exposed on port 9000, accessible via http://0.0.0.0:9000.
  - Web-based management console exposed on port 9001, accessible via http://0.0.0.0:9001. (Auth credentials are **username** is **admin** and **password** is **password**)

These ports and services together form the architecture for the image compression service, providing database storage, task management, object storage, and web interfaces for administration and API access.

```bash
cd ~/Dev
mkdir image-compressor
cd ~/Dev/image-compressor
git clone https://github.com/Arvind-4/image-compressor.git .
docker compose up --build
```

### Manual Setup:

- Create a Directory and virtualenv:

```bash
cd ~/Dev
mkdir image-compressor
cd ~/Dev/image-compressor
git clone https://github.com/Arvind-4/image-compressor.git .
```

- Install using `requirements.txt` file or `poetry`:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

<center>
<b>or</b>
</center>

```bash
poetry install
```

- Create a `.env` file :

```bash
cp .env.sample .env
```

**Change values accordingly in env file**

- Run mongodb, mongodb admin and minio:

```bash
docker compose -f compose.service.yaml up --build -d
```

- Set env:

```bash
set -a
source .env.docker
source .env.example
source .env
set +a
```

- Run fastapi:

```bash
bash commands/run.sh
```

- Run celery:

```bash
bash commands/background-task.sh
```

### File Structure:

```bash
.
├── api.Dockerfile # Docker file for fastapi
├── app
│   ├── celery_app.py # Celery app
│   ├── config.py # Config and env variables for the project
│   ├── db.py # Mongo db connection file
│   ├── __init__.py # Module file
│   ├── main.py # Entrypoint file for our application
│   ├── routes.py # Routes for the application
│   ├── schemas.py # Schema and validations for data
│   ├── services.py # Mongo DB CRUD operations
│   ├── storage.py # Minio client file
│   ├── tasks.py # Celery worker file
│   └── utils.py # functions performed on data
│   └── webhooks.py # webhook url for the repo
├── celery.Dockerfile # Docker file for celery
├── commands
│   ├── background-task.sh # Celery command
│   ├── entrypoint.sh # Fastapi production entrypoint
│   ├── export.sh # Export poetry dependencies
│   └── run.sh # Run dev server
├── compose.service.yaml # Service only docker file
├── compose.yaml # Docker file for all services
├── .env.docker # Env file for docker
├── .env.sample # Env file for reference
├── .gitbook
│   └── diagram.png # Architecture diagram
├── LICENSE # LICENSE file forr the project
├── poetry.lock # Poetry lock file
├── pyproject.toml # Poetry file
├── .python-version # Python version
├── pyvenv.cfg # Python venv file
├── requirements-dev.txt # Python dev  requirements
├── requirements.txt # Python requirements file
├── ruff.toml # Format and lint files
├── sample-data
│   └── sheet.csv # Sample csv file for testing and reference
└── set-env.txt # COmmand to set and load env variables

4 directories, 33 files
```

### Components:

**FastAPI** serves as the core framework for handling API requests, ensuring efficient and scalable endpoints for uploading CSV files (`/upload/`), checking task statuses (`/status/{request_id}`), and downloading compressed images (`/download/{request_id}`).

**MongoDB** is utilized to persist image data and track task statuses. The `image_requests` collection stores details of uploaded image data and their processing statuses.

**Celery** manages asynchronous image compression tasks (`process_image_task`). This task downloads original images, compresses them with user-defined quality, uploads both original and compressed images to MinIO, and updates task statuses in MongoDB upon completion.

**MinIO**, an object storage service, stores both original and compressed images in separate buckets (`original-images` and `compressed-images`).

**Docker** is a containerization platform that simplifies the process of packaging applications and their dependencies into portable, self-sufficient containers. These containers can run consistently across different computing environments, ensuring reliable deployment and scalability of applications.

### Usage:

Users interact with the service by uploading CSV files containing image data, monitoring task progress through status queries, and downloading compressed images once tasks are completed.

#### Prerequisites:

- Install Docker and Docker Compose.
- Set up MongoDB instance.
- Configure MinIO server.

#### Build and Run:

1. Clone the repository.
2. Set up environment variables. Refer `.env.sample` file.
3. Build and run Docker containers using `docker-compose up --build`.

### Functionality:

The service allows users to upload CSV files containing image data, initiate image compression tasks asynchronously, check task status, and download compressed images.

### API Endpoints:

#### Upload CSV File:

- **Endpoint**: `/api/upload/`
- **Method**: POST
- **Parameters**:
  - `file`: CSV file containing image data.
- **Functionality**:
  - Parses CSV content.
  - Validates and stores image data in MongoDB.
  - Initiates image compression tasks using Celery.

#### Check Task Status:

- **Endpoint**: `/api/status/{request_id}`
- **Method**: GET
- **Parameters**:
  - `request_id`: Unique identifier for the request.
- **Functionality**:
  - Retrieves the status of the image compression task from MongoDB.

#### Download Compressed Images:

- **Endpoint**: `/api/download/{request_id}`
- **Method**: GET
- **Parameters**:
  - `request_id`: Unique identifier for the request.
- **Functionality**:
  - Checks if image compression task is completed.
  - Converts compressed image data to CSV format and streams it for download.

#### Docs:

- **Endpoint**: `/docs`
- **Method**: GET
- **Functionality**:
  - Automatically generated documentation using Swagger UI.
  - Provides detailed API endpoint descriptions, request/response formats, and example usage scenarios.

This addition includes the `/docs` endpoint, which is automatically generated by FastAPI's built-in Swagger UI. It enhances the usability of the service by providing interactive API documentation directly accessible through a web browser, facilitating easier integration and usage for developers.

### Celery Tasks:

**`process_image_task`**

- **Description**: Asynchronous task for image compression.
- **Functionality**:
  - Downloads original images from provided URLs.
  - Compresses images using specified quality.
  - Uploads original and compressed images to MinIO.
  - Updates task status and Updated URL's in MongoDB upon completion.

### Deployment and Integration:

The service is containerized using **Docker**, facilitating easy deployment and scalability. The Docker setup includes a Dockerfile defining dependencies and a Docker Compose configuration for orchestrating multiple containers (FastAPI, Celery, MongoDB, and MinIO).

#### Docker Deployment:

- **api.Dockerfile**: Defines the environment and dependencies required for the application for fastapi service.
- **celery.Dockerfile**: Defines the environment and dependencies required for the application for background service.
- **Docker Compose**: Orchestrates multiple Docker containers (FastAPI, Celery, MongoDB, MinIO).
- **Environment Variables**: Configures service endpoints, credentials, and other settings. Refer `.env.sample` file.

### Security Considerations:

To enhance security, the service implements authentication mechanisms for API endpoints, controls access to sensitive operations, and ensures data encryption for transmission and storage.

- **Authentication**: Implement authentication mechanisms to secure API endpoints.
- **Authorization**: Control access to sensitive operations like uploading and downloading images.
- **Data Encryption**: Ensure data transmission and storage are encrypted.

### Conclusion:

This document provides a comprehensive overview of the image compression service architecture, including its components, API functionality, Celery task management, integration with MongoDB and MinIO for data storage, Docker deployment setup, security measures, and user interaction scenarios. It serves as a guide for deploying, utilizing, and securing the image compression service effectively in various operational environments. Additionally, it covers API endpoints, usage instructions, and more.

---

<h4 align="center">End of Document</h4>

---
