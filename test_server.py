#!/usr/bin/env python3
"""
Simple HTTP Server for testing HTML, CSS, JS connections
Usage: python3 test_server.py
Then open: http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import os
import sys

def start_server(port=8000):
    try:
        # Change to the current directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        Handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🔫 GUN WiFi Tool - Test Server")
            print(f"📁 Serving directory: {os.getcwd()}")
            print(f"🌐 Server running at: http://localhost:{port}")
            print(f"📄 Main page: http://localhost:{port}/index.html")
            print(f"🧪 Test page: http://localhost:{port}/test-connections.html")
            print(f"⏹️  Press Ctrl+C to stop the server")
            print("-" * 50)
            
            # Try to open browser
            try:
                webbrowser.open(f'http://localhost:{port}/test-connections.html')
                print("🔥 Opening test page in browser...")
            except:
                print("💡 Manually open: http://localhost:{port}/test-connections.html")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use!")
            print(f"💡 Try a different port: python3 test_server.py {port+1}")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number!")
            sys.exit(1)
    
    start_server(port)
