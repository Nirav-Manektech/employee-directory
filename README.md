# HR Employee Directory Microservice

A FastAPI-based microservice for searching employees across organizations with dynamic field visibility, rate-limiting, and OpenAPI support.

## 🧰 Features

- Dynamic field config per organization
- Custom rate limiting (no external lib)
- OpenAPI docs `/docs`
- Dockerized
- Fully tested

## 🚀 Getting Started

```bash
# Build and run
docker build -t hr-service .
docker run -p 8000:8000 hr-service

# API available at
http://localhost:8000/docs
