#!/usr/bin/env python3
"""
LeapScholar Brand Monitor Launcher
Simple script to run the Streamlit dashboard with proper setup
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 
        'textblob', 'vaderSentiment', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def setup_environment():
    """Set up environment variables if .env file exists"""
    env_file = Path('.env')
    if env_file.exists():
        print("✅ Found .env file")
        return True
    else:
        print("⚠️  No .env file found. Using demo mode with mock data.")
        print("   To enable AI features, create a .env file with your API keys.")
        return True

def run_dashboard():
    """Run the Streamlit dashboard"""
    try:
        print("🚀 Starting LeapScholar Brand Monitor...")
        print("📊 Dashboard will open in your browser at http://localhost:8501")
        print("🔄 Press Ctrl+C to stop the dashboard")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🎓 LeapScholar Brand Perception Monitor")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the project directory.")
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Setup environment
    setup_environment()
    
    # Run dashboard
    return run_dashboard()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 