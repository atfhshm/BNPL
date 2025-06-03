# BNPL (Buy Now Pay Later) Platform

A full-stack Buy Now Pay Later platform built with Django and React, featuring a modern architecture and robust features for managing installment payments and customer relationships.

## 🚀 Architecture

The project is structured as a monorepo with two main components:

## 🚀 Features

### Backend (Django)

- RESTful API with Django REST Framework
- JWT Authentication
- Celery for async task processing
- Redis for caching and message broker
- PostgreSQL database
- API documentation with DRF Spectacular
- Django Silk for performance profiling
- S3 storage integration
- Phone number validation
- Money handling with django-money
- CORS support

### Frontend (React)

- Server-side rendering with React Router
- Modern UI with Radix UI components
- State management with Zustand
- Data fetching with TanStack Query
- Form handling with React Hook Form
- TypeScript for type safety
- TailwindCSS for styling
- Dark mode support
- Responsive design

## 🛠️ Tech Stack

### Backend

- Python 3.13+
- Django 5.2+
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- Gunicorn
- Uvicorn

### Frontend

- React 19
- React Router 7
- TypeScript
- Vite
- TailwindCSS
- Radix UI
- Zustand
- TanStack Query

## Development

To start running the development, please refer to the specific documentation for each component:

- [Backend Development Guide](server/README.md) - Django server setup and configuration
- [Frontend Development Guide](web/README.md) - React application setup and configuration

For a complete development environment, you'll need to set up both components. We recommend starting with the backend setup first, followed by the frontend configuration.
