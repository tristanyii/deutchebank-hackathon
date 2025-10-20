#!/usr/bin/env python3
"""
Deployment script for the Flask backend
This script helps deploy the backend to various platforms
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if .env file exists in parent directory
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        print("❌ .env file not found in parent directory")
        print("   Please create a .env file with GROQ_API_KEY and SERP_API_KEY")
        return False
    
    # Check if required environment variables are set
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    required_vars = ['GROQ_API_KEY', 'SERP_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All requirements met")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_server():
    """Test if the server can start"""
    print("🧪 Testing server startup...")
    try:
        # Import the app to test for import errors
        from app import app
        print("✅ Server imports successfully")
        return True
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def generate_retell_config():
    """Generate Retell AI configuration template"""
    print("📋 Generating Retell AI configuration...")
    
    config = {
        "webhook_url": "https://your-domain.com/retell/webhook",
        "events": [
            "call_started",
            "call_ended", 
            "call_analyzed",
            "conversation_turn"
        ],
        "response_format": {
            "response": "string - The text response to be spoken",
            "end_call": "boolean - Whether to end the call"
        }
    }
    
    config_path = Path(__file__).parent / 'retell_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Retell configuration saved to {config_path}")
    return True

def main():
    """Main deployment function"""
    print("🚀 Flask Backend Deployment Script")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Deployment failed: Requirements not met")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Deployment failed: Could not install dependencies")
        sys.exit(1)
    
    # Test server
    if not test_server():
        print("\n❌ Deployment failed: Server test failed")
        sys.exit(1)
    
    # Generate Retell config
    generate_retell_config()
    
    print("\n✅ Deployment preparation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Deploy your Flask app to a cloud platform (Heroku, Railway, etc.)")
    print("2. Update the webhook URL in retell_config.json")
    print("3. Configure your Retell AI webhook with the deployed URL")
    print("4. Test the integration with a voice call")

if __name__ == '__main__':
    main()
