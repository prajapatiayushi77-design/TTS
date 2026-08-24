#!/bin/bash

# TTS Application - Quick Deployment Script

echo "🚀 TTS Application - Deployment Helper"
echo "========================================"
echo ""

# Check if vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not installed."
    echo "Please install Git: https://git-scm.com/download/win"
    exit 1
fi

echo "📝 Deploying to Vercel..."
echo ""
echo "Make sure you have:"
echo "  ✓ A GitHub account (https://github.com)"
echo "  ✓ A Vercel account (https://vercel.com)"
echo "  ✓ Code pushed to GitHub"
echo ""
echo "Deploying now..."
vercel

echo ""
echo "✅ Deployment started!"
echo ""
echo "Your app will be available at: https://your-project.vercel.app"
echo ""
echo "Next steps:"
echo "1. Check Vercel dashboard for deployment status"
echo "2. Test your live URL"
echo "3. Share with the world! 🌍"
