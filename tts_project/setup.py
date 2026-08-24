#!/usr/bin/env python3
"""
Initialize and setup TTS project for deployment
Supports local development, Vercel, Railway, and Render deployment
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a shell command"""
    print(f"\n📦 {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("=" * 50)
    print("🚀 TTS Project Setup & Deployment Helper")
    print("=" * 50)
    
    print("\n📋 Choose deployment option:")
    print("1. Local development (Flask server)")
    print("2. Deploy to Vercel (Serverless)")
    print("3. Deploy to Railway (Container)")
    print("4. Deploy to Render (Container)")
    print("5. Setup all dependencies (no deployment)")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        setup_local()
    elif choice == "2":
        setup_vercel()
    elif choice == "3":
        setup_railway()
    elif choice == "4":
        setup_render()
    elif choice == "5":
        setup_dependencies()
    else:
        print("❌ Invalid choice")
        sys.exit(1)

def setup_dependencies():
    """Install all dependencies"""
    print("\n🔧 Installing dependencies...")
    
    if not run_command("pip install -r requirements-prod.txt", "Installing Python dependencies"):
        return
    
    print("\n✅ All dependencies installed!")
    print("\nYou can now:")
    print("  • Run local Flask server: python app.py")
    print("  • Run CLI: python main.py --text 'Hello' --output out.wav")
    print("  • Deploy to Vercel, Railway, or Render")

def setup_local():
    """Setup for local development"""
    print("\n🏠 Setting up local development environment...")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing base dependencies"):
        return
    
    print("\n✅ Local setup complete!")
    print("\n🌐 To start the web server:")
    print("   python app.py")
    print("\n   Then open: http://localhost:5000")
    
    print("\n💡 Or use the CLI:")
    print("   python main.py --text 'Your text' --output audio.wav")

def setup_vercel():
    """Setup for Vercel deployment"""
    print("\n☁️  Setting up for Vercel deployment...")
    print("\n📋 Prerequisites:")
    print("  1. Create a Vercel account: https://vercel.com/signup")
    print("  2. Create a GitHub account: https://github.com/signup")
    print("  3. Push this code to GitHub")
    
    print("\n📝 Steps to deploy:")
    print("\n1. Initialize Git (if not done):")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git remote add origin https://github.com/YOUR_USERNAME/tts-project.git")
    print("   git push -u origin main")
    
    print("\n2. Install Vercel CLI:")
    if run_command("npm install -g vercel", "Installing Vercel CLI"):
        print("\n3. Deploy:")
        print("   vercel")
        print("\n4. Follow the prompts and your app will be live!")
    
    print("\n✨ After deployment:")
    print("  • Your app will be at: https://your-project.vercel.app")
    print("  • API endpoints: /api/generate, /api/voices")
    print("  • Auto-scales globally")

def setup_railway():
    """Setup for Railway deployment"""
    print("\n🚂 Setting up for Railway deployment...")
    print("\n📋 Prerequisites:")
    print("  1. Create a Railway account: https://railway.app")
    print("  2. Connect your GitHub account")
    print("  3. Make sure Dockerfile exists")
    
    print("\n📝 Steps to deploy:")
    print("\n1. Push code to GitHub")
    print("\n2. Go to Railway dashboard")
    print("\n3. Click 'New Project' → 'Deploy from GitHub'")
    print("\n4. Select this repository")
    print("\n5. Railway auto-detects the Dockerfile")
    print("\n6. Click 'Deploy'")
    
    print("\n✨ After deployment:")
    print("  • Your app will be at: https://your-app.railway.app")
    print("  • Full Python/Flask support")
    print("  • Persistent storage")
    print("  • Free tier: 500 hours/month")

def setup_render():
    """Setup for Render deployment"""
    print("\n🎨 Setting up for Render deployment...")
    print("\n📋 Prerequisites:")
    print("  1. Create a Render account: https://render.com")
    print("  2. Connect your GitHub account")
    print("  3. Make sure render.yaml exists")
    
    print("\n📝 Steps to deploy:")
    print("\n1. Push code to GitHub")
    print("\n2. Go to Render dashboard")
    print("\n3. Click 'New +' → 'Web Service'")
    print("\n4. Select your GitHub repository")
    print("\n5. Render auto-detects render.yaml")
    print("\n6. Click 'Create Web Service'")
    
    print("\n✨ After deployment:")
    print("  • Your app will be at: https://your-app.onrender.com")
    print("  • Auto-deploys on GitHub push")
    print("  • Free tier available")
    print("  • Easy PostgreSQL integration")

if __name__ == "__main__":
    main()
