#!/usr/bin/env python3
"""
Flask server runner for Retell AI integration
This script starts the Flask backend server
"""

import os
import sys
from app import app

def main():
    """Main function to run the Flask server"""
    print("🚀 Starting Flask backend for Retell AI integration...")
    print("📞 Voice call webhook endpoint: /retell/webhook")
    print("🔍 Test endpoint: /test-agent")
    print("❤️  Health check: /health")
    print("-" * 50)
    
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🌐 Server will run on: http://{host}:{port}")
    print(f"🐛 Debug mode: {debug}")
    print("-" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
