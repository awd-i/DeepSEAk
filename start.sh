#!/bin/bash

echo "======================================"
echo "  Grok Talent Engineer - Startup"
echo "======================================"
echo ""

# Function to kill background processes on exit
cleanup() {
    echo "Shutting down..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup EXIT INT TERM

# Start backend
echo "Starting backend on http://localhost:8000..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend on http://localhost:3001..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "======================================"
echo "  Services Running:"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3001"
echo "======================================"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
wait
