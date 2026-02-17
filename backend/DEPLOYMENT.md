# Deployment Guide

## Prerequisites
- Docker & Docker Compose
- Ubuntu 20.04 or later
- 4GB RAM minimum
- SSL certificates

## Local Deployment

```bash
# 1. Clone repository
git clone https://github.com/Haseena3121/online-exam-proctoring.git
cd online-exam-proctoring

# 2. Configure environment
cp backend/.env.example backend/.env
# Edit .env with your settings

# 3. Start services
docker-compose up -d

# 4. Run migrations
docker-compose exec backend flask db upgrade

# 5. Seed data
docker-compose exec backend python seed_data.py