#!/bin/bash
# Local testing script for Pokemon TCG Analyst

echo "🧪 Starting local testing environment..."

# Start SAM local API
echo "Starting SAM local API on port 3001..."
sam local start-api --port 3001 &
SAM_PID=$!

# Wait for API to be ready
sleep 5

# Start frontend dev server
echo "Starting frontend dev server on port 3000..."
cd frontend
REACT_APP_API_URL="http://localhost:3001" npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Local environment started!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for Ctrl+C
trap "kill $SAM_PID $FRONTEND_PID; exit" INT
wait
