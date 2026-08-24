# Deploy Your TTS App to Vercel & Global Platforms

This guide will help you deploy your Text-to-Speech application to Vercel and other global platforms.

## 🚀 Quick Deploy to Vercel (Recommended)

### Prerequisites
- [Vercel Account](https://vercel.com/signup) (free)
- [GitHub Account](https://github.com/signup) (for easy deployment)
- Git installed on your machine

### Step 1: Push to GitHub

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit - TTS application"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/tts-project.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Vercel

**Option A: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project directory
cd c:\Users\Admin\Desktop\tts\tts_project
vercel
```

**Option B: Using Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect Python
5. Click "Deploy"

### Step 3: Configure Environment (if needed)

In Vercel Dashboard:
1. Go to Settings → Environment Variables
2. Add any required environment variables
3. Redeploy

### Your App is Live! 🎉

Your app will be available at: `https://your-project-name.vercel.app`

---

## 📦 Alternative Deployment Options

### Railway (Recommended for Python)

Railway works great with Flask and Python apps:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Why Railway?**
- Free tier: 500 hours/month
- Better Python support than Vercel
- Keep using Flask app.py as-is
- Persistent storage for files
- PostgreSQL included (free)

### Render

Simple Python deployment:

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create New → Web Service
4. Select your GitHub repo
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python app.py`
7. Deploy

**Why Render?**
- Free tier available
- Easy PostgreSQL integration
- Auto-deploys from GitHub

### Heroku (Paid only now)

Still supports Python:

```bash
# Install Heroku CLI
npm install -g heroku

# Login and deploy
heroku login
hercel create
git push heroku main
```

---

## 🌍 Multi-Region Deployment

Deploy to multiple regions for global availability:

### Using Vercel's Global Edge Network
- Vercel automatically deploys to 35+ regions worldwide
- Auto-replicates your app globally
- No additional configuration needed

### Using Cloudflare + Your Backend
1. Deploy backend to Railway/Render
2. Use Cloudflare for global CDN
3. Cloudflare automatically caches responses

---

## 📝 Project Structure for Vercel

```
tts-project/
├── api/                    # Vercel serverless functions
│   ├── generate.py        # Audio generation endpoint
│   └── voices.py          # Voice list endpoint
├── public/                 # Static files (optional)
│   └── index.html         # (if using static HTML)
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html         # Main UI
├── vercel.json            # Vercel configuration
├── .vercelignore          # Files to exclude from deployment
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🔧 Environment Variables

Create `.env.local` for local testing:

```env
PYTHON_VERSION=3.11
DEBUG=False
TTS_BACKEND=edge
MAX_TEXT_LENGTH=50000
```

In Vercel Dashboard, add under Settings → Environment Variables:
- Same variables for production

---

## 🚨 Important Notes for Deployment

### 1. **Edge-TTS vs Local TTS**
- **Local (pyttsx3)**: Works locally, not serverless-friendly
- **Edge-TTS**: Works everywhere (cloud-based), recommended for production

### 2. **Audio Storage**
- Vercel has `/tmp` storage (ephemeral)
- Audio is generated, encoded to base64, and sent immediately
- Files are deleted after response
- For persistent storage, consider S3 or Supabase

### 3. **API Rate Limiting**
- Vercel free tier: 100 deployments/day
- Function execution: Limited by plan
- Edge-tts: Unlimited (free)

### 4. **File Size Limits**
- Vercel functions: 6MB response limit
- Long texts = larger audio files
- Keep texts under 10,000 words for safety

---

## ✅ Deployment Checklist

- [ ] Push code to GitHub
- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Run `vercel` in project directory
- [ ] Connect GitHub account
- [ ] Configure environment variables (if any)
- [ ] Test `/api/generate` endpoint
- [ ] Test `/api/voices` endpoint
- [ ] Test frontend UI
- [ ] Download generated audio
- [ ] Share your live URL!

---

## 🔗 Example URLs After Deployment

```
Frontend:  https://your-app.vercel.app/
API:       https://your-app.vercel.app/api/generate
Voices:    https://your-app.vercel.app/api/voices
```

---

## 📊 Performance Tips

### For Better Performance:
1. **Use CDN**: Vercel's global edge network is automatic
2. **Optimize text**: Shorter texts = faster response
3. **Cache voices**: Browser caches voice list
4. **Monitor**: Vercel Dashboard → Analytics

### Scaling:
- Vercel automatically scales your functions
- Free tier: Sufficient for moderate traffic
- Pro tier: For high-traffic apps

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
# Ensure requirements.txt includes all dependencies
pip freeze > requirements-new.txt
# Compare and update requirements.txt
```

### API 500 Error
- Check Vercel logs: Dashboard → Deployments → Details
- Ensure edge-tts is in requirements.txt
- Restart deployment

### Audio Not Downloading
- Check browser console (F12)
- Verify API returns base64 data
- Test with smaller text first

### Slow Generation
- Text is too long (split into parts)
- Railway/Render might be faster for production
- Consider upgrading plan

---

## 💡 Pro Tips

1. **Custom Domain**: Vercel → Settings → Domains
2. **GitHub Integration**: Auto-deploy on push
3. **Preview URLs**: Get unique URL for each PR
4. **Analytics**: Monitor usage in Dashboard
5. **Email Notifications**: Set up deployment alerts

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **GitHub Issues**: Post errors there

---

## 🎯 Next Steps

1. Deploy to Vercel using quick start above
2. Test your live URL
3. Share with friends
4. Monitor usage
5. Consider upgrading if needed

Good luck! 🚀
