#!/usr/bin/env python3
"""
Simple HTTP server to serve the employee dashboard
Run this script to make the dashboard accessible via web browser
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    # Change to the directory containing the dashboard files
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Employee Dashboard Server Starting...")
        print(f"📊 Dashboard URL: http://localhost:{PORT}")
        print(f"🌐 Share this URL with your manager!")
        print(f"📱 Also accessible on mobile devices on your network")
        print(f"⚡ Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("✅ Dashboard opened in your default browser")
        except:
            print("ℹ️  Please open http://localhost:{PORT} in your browser")
        
        # Start serving
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            sys.exit(0)

if __name__ == "__main__":
    main()