#!/usr/bin/env python3
"""
Test script for the Flask backend integration
This script tests the backend without requiring Retell AI
"""

import requests
import json
import time
import sys
from threading import Thread

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_anthony_endpoint(base_url):
    """Test the Anthony persona endpoint"""
    print("🤖 Testing Anthony persona endpoint...")
    
    # Test conversation flow
    conversation_steps = [
        "Hi, I need help with housing",
        "California, 90210",
        "John",
        "35",
        "25000"
    ]
    
    call_id = "test-conversation-123"
    
    for i, user_input in enumerate(conversation_steps):
        try:
            response = requests.post(
                f"{base_url}/test-anthony",
                json={
                    "call_id": call_id,
                    "user_input": user_input
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Step {i+1}: '{user_input}'")
                print(f"   Anthony: {data['anthony_response'][:100]}...")
                print(f"   Step: {data['conversation_step']}")
                print()
            else:
                print(f"❌ Step {i+1} failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Step {i+1} error: {e}")
            return False
    
    return True

def test_retell_webhook(base_url):
    """Test the Retell webhook endpoint"""
    print("📞 Testing Retell webhook...")
    
    # Test conversation turn event
    webhook_data = {
        "event": "conversation_turn",
        "call": {
            "call_id": "test-call-123"
        },
        "transcript": "I need help finding housing resources"
    }
    
    try:
        response = requests.post(
            f"{base_url}/retell/webhook",
            json=webhook_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook test passed")
            print(f"   Response: {data.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ Webhook test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

def run_server_in_background(port=5000):
    """Run the Flask server in the background"""
    import subprocess
    import os
    
    # Change to the flask_backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start the server
    process = subprocess.Popen([
        sys.executable, 'run_server.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a bit for server to start
    time.sleep(3)
    
    return process

def main():
    """Main test function"""
    print("🧪 Flask Backend Integration Test")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    # Start server in background
    print("🚀 Starting Flask server...")
    server_process = run_server_in_background()
    
    try:
        # Wait for server to be ready
        print("⏳ Waiting for server to start...")
        time.sleep(5)
        
        # Run tests
        tests_passed = 0
        total_tests = 3
        
        if test_health_endpoint(base_url):
            tests_passed += 1
        
        if test_anthony_endpoint(base_url):
            tests_passed += 1
        
        if test_retell_webhook(base_url):
            tests_passed += 1
        
        # Results
        print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
        
        if tests_passed == total_tests:
            print("✅ All tests passed! The Flask backend is working correctly.")
            print("\n🎉 Your backend is ready for Retell AI integration!")
            print("📋 Next steps:")
            print("1. Deploy your Flask app to a cloud platform")
            print("2. Configure Retell AI webhook with your deployed URL")
            print("3. Test with actual voice calls")
        else:
            print("❌ Some tests failed. Please check the errors above.")
            sys.exit(1)
            
    finally:
        # Clean up - stop the server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == '__main__':
    main()
