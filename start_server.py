#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import threading
import time
import sys
import os

def find_free_port():
    """Find a free port to use"""
    import socket
    ports_to_try = [4000, 4001, 4002, 5000, 5001, 5002, 6000, 6001, 7000, 7001, 8000, 8001, 8002, 9000, 9001]
    
    for port in ports_to_try:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return 8080  # fallback

def start_server():
    # Change to the directory containing the dashboard
    os.chdir('/workspace')
    
    # Find available port
    port = find_free_port()
    
    class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # Suppress server logs
    
    try:
        with socketserver.TCPServer(("", port), QuietHTTPRequestHandler) as httpd:
            print("🚀 Employee Dashboard Server Started!")
            print("=" * 50)
            print(f"📊 Dashboard URL: http://localhost:{port}/simple_dashboard.html")
            print(f"🌐 Alternative: http://localhost:{port}/index.html")
            print("=" * 50)
            print("✅ Server is running...")
            print("🔗 Opening dashboard in your browser...")
            print("📱 Share the URL above with your manager!")
            print("⚡ Press Ctrl+C to stop")
            
            # Try to open browser
            def open_browser():
                time.sleep(1)  # Wait for server to start
                try:
                    webbrowser.open(f'http://localhost:{port}/simple_dashboard.html')
                except:
                    print("ℹ️  Please manually open the URL above in your browser")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try opening simple_dashboard.html directly in your browser")

if __name__ == "__main__":
    start_server()