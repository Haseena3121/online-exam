#!/bin/bash

set -e

echo "🚀 Starting Online Exam Proctoring System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please configure .env file and run again${NC}"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip install -q -r requirements.txt

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p uploads/evidence uploads/videos logs

# Initialize database
echo -e "${YELLOW}🗄️  Initializing database...${NC}"
flask db upgrade

# Load seed data (optional)
if [ -f "seed_data.py" ]; then
    echo -e "${YELLOW}🌱 Loading seed data...${NC}"
    python seed_data.py
fi

# Start server
echo -e "${GREEN}✅ Starting Flask server...${NC}"
python run.py