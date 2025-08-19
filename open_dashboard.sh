#!/bin/bash

echo "🚀 Employee Performance Dashboard"
echo "=================================="
echo ""
echo "✅ Your dashboard is ready! Choose an option:"
echo ""
echo "🌐 OPTION 1: Web Server (Recommended)"
echo "   Open: http://localhost:4000/simple_dashboard.html"
echo ""
echo "📁 OPTION 2: Direct File Access"
echo "   Double-click: simple_dashboard.html"
echo ""
echo "🔗 OPTION 3: Alternative Files"
echo "   - dashboard_standalone.html"
echo "   - index.html"
echo ""
echo "📧 SHARING WITH MANAGER:"
echo "   - Send them: simple_dashboard.html (works offline)"
echo "   - Or share URL: http://localhost:4000/simple_dashboard.html"
echo ""
echo "💡 If port 4000 doesn't work, try:"
echo "   python3 start_server.py"
echo ""

# Try to open browser
if command -v xdg-open > /dev/null; then
    echo "🔄 Opening dashboard in browser..."
    xdg-open "http://localhost:4000/simple_dashboard.html" 2>/dev/null || xdg-open "simple_dashboard.html"
elif command -v open > /dev/null; then
    echo "🔄 Opening dashboard in browser..."
    open "http://localhost:4000/simple_dashboard.html" 2>/dev/null || open "simple_dashboard.html"
else
    echo "📋 Please open http://localhost:4000/simple_dashboard.html in your browser"
fi