### LinkedIn Analytics Backend
This project is a backend system built using FastAPI and PostgreSQL, designed to power a simplified LinkedIn analytics platform. The main focus areas are database design, API handling, and scheduling logic.

#### Features
- RESTful API endpoints to create, read, update, and delete posts and analytics data.
- PostgreSQL database integration for reliable data storage.
- Scheduling logic to handle periodic tasks such as analytics updates or post scheduling using APScheduler.
- User authentication and authorization.
- Timezone-aware datetime handling.


#### Tech Stack
- Python 3.10+
- FastAPI for building APIs
- PostgreSQL as the relational database
- SQLAlchemy as the ORM
- APScheduler for background job scheduling
- Pydantic for request/response validation
- Alembic for database migrations (optional) 

#### Setup Instructions
1. Clone the repository
``` git clone https://github.com/astrospkc/Post-Scheduler.git
    cd Post-Scheduler```
2. Install Dependencies
``` uv install ```