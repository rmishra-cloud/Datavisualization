#!/bin/bash

# Employee Performance Dashboard Launcher
echo "🚀 Starting Employee Performance Dashboard..."
echo "=================================="

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
    python3 serve_dashboard.py
elif command -v python &> /dev/null; then
    echo "✅ Python found"
    python serve_dashboard.py
else
    echo "❌ Python not found. Opening dashboard directly in browser..."
    
    # Try to open the HTML file directly
    if command -v xdg-open &> /dev/null; then
        xdg-open index.html
    elif command -v open &> /dev/null; then
        open index.html
    elif command -v start &> /dev/null; then
        start index.html
    else
        echo "📁 Please open 'index.html' in your web browser"
    fi
fi