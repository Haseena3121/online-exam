#!/bin/bash

# ============================================
# Complete Setup Script for Backend
# ============================================

set -e

echo "🚀 Setting up Online Exam Proctoring Backend..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Step 1: Create virtual environment
echo -e "${YELLOW}Step 1: Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Step 2: Install dependencies
echo -e "${YELLOW}Step 2: Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Create .env file
echo -e "${YELLOW}Step 3: Creating .env file...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please configure .env file${NC}"
fi

# Step 4: Create directories
echo -e "${YELLOW}Step 4: Creating directories...${NC}"
mkdir -p uploads/evidence uploads/videos logs migrations/versions

# Step 5: Initialize database
echo -e "${YELLOW}Step 5: Initializing database...${NC}"
flask db init 2>/dev/null || true
flask db migrate -m "Initial migration"
flask db upgrade

# Step 6: Seed data (optional)
echo -e "${YELLOW}Step 6: Loading seed data...${NC}"
python seed_data.py

echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo -e "${GREEN}Run 'python run.py' to start the server${NC}"