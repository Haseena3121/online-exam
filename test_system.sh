#!/bin/bash

echo "🔍 Testing Online Exam Proctoring System..."
echo ""

# Test MySQL
echo "1️⃣  Testing MySQL..."
mysql -u exam_user -p'exam_password' online_exam_proctoring -e "SELECT COUNT(*) as user_count FROM users;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ MySQL: Connected"
else
    echo "❌ MySQL: Failed"
fi

# Test Redis
echo "2️⃣  Testing Redis..."
redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Redis: Connected"
else
    echo "❌ Redis: Failed"
fi

# Test Backend API
echo "3️⃣  Testing Backend API..."
curl -s http://localhost:5000/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Backend: Running"
else
    echo "❌ Backend: Not responding"
fi

# Test Frontend
echo "4️⃣  Testing Frontend..."
curl -s http://localhost:3000 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Frontend: Running"
else
    echo "❌ Frontend: Not responding"
fi

echo ""
echo "✅ All tests completed!"