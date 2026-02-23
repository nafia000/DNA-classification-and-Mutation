#!/bin/bash
# Quick start script for Genome-X (macOS/Linux)

echo "================================"
echo "  Genome-X ML Integration Setup"
echo "================================"
echo ""

echo "Step 1: Installing Frontend Dependencies..."
echo ""
npm install
if [ $? -ne 0 ]; then
    echo "Error installing npm dependencies"
    exit 1
fi

echo ""
echo "Step 2: Installing Backend Dependencies..."
echo ""
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing Python dependencies"
    exit 1
fi

echo ""
echo "================================"
echo "  Setup Complete!"
echo "================================"
echo ""
echo "To start the application:"
echo ""
echo "1. Terminal 1 - Start Backend:"
echo "   python server.py"
echo ""
echo "2. Terminal 2 - Start Frontend:"
echo "   npm run dev"
echo ""
echo "Frontend will be available at: http://localhost:5173"
echo "Backend API will be available at: http://localhost:8000"
echo ""
