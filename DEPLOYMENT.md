# ResumeAI Classifier - Deployment Guide

## 🚀 Quick Deployment

This guide will help you deploy the ResumeAI Classifier to free hosting platforms.

## Prerequisites

1. **GitHub Account**: Create a repository and push your code
2. **Railway Account**: For backend deployment (free tier)
3. **Vercel Account**: For frontend deployment (free tier)
4. **Git**: Installed on your machine

## Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository

```bash
# Navigate to your project directory
cd "ResumeAI Classifier"

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: ResumeAI Classifier"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/resumeai-classifier.git

# Push to GitHub
git push -u origin main
```

### 1.2 Environment Variables Setup

Create a `.env` file in the backend directory:

```bash
# Backend Environment Variables
DATABASE_URL=postgresql://resumeai:resumeai123@localhost:5432/resumeai
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=false
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-frontend-domain.vercel.app
GROK_API_KEY=your-grok-api-key-here
```

## Step 2: Deploy Backend to Railway

### 2.1 Railway Setup

1. Go to [Railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `resumeai-classifier` repository
5. Choose the `main` branch

### 2.2 Configure Railway Environment Variables

In your Railway project dashboard:

1. Go to "Variables" tab
2. Add the following environment variables:

```
DATABASE_URL=postgresql://resumeai:resumeai123@localhost:5432/resumeai
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=false
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
GROK_API_KEY=your-grok-api-key-here
```

### 2.3 Add PostgreSQL Database

1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway will automatically provide the DATABASE_URL
3. Update your environment variables with the new DATABASE_URL

### 2.4 Deploy Backend

Railway will automatically detect the `railway.json` configuration and deploy your backend.

**Expected deployment time**: 5-10 minutes

## Step 3: Deploy Frontend to Vercel

### 3.1 Vercel Setup

1. Go to [Vercel.com](https://vercel.com)
2. Sign up with your GitHub account
3. Click "New Project"
4. Import your `resumeai-classifier` repository
5. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 3.2 Configure Vercel Environment Variables

In your Vercel project settings:

1. Go to "Settings" → "Environment Variables"
2. Add the following variables:

```
REACT_APP_API_URL=https://your-backend-domain.railway.app
REACT_APP_GROK_API_KEY=your-grok-api-key-here
```

### 3.3 Deploy Frontend

Click "Deploy" and Vercel will build and deploy your frontend.

**Expected deployment time**: 3-5 minutes

## Step 4: Update Configuration

### 4.1 Update CORS Settings

After getting your deployment URLs, update the backend CORS settings:

1. Go to Railway dashboard
2. Update `ALLOWED_ORIGINS` with your Vercel frontend URL
3. Redeploy the backend

### 4.2 Update Frontend API URL

1. Go to Vercel dashboard
2. Update `REACT_APP_API_URL` with your Railway backend URL
3. Redeploy the frontend

## Step 5: Verify Deployment

### 5.1 Backend Health Check

Visit your Railway backend URL + `/health`:
```
https://your-backend-domain.railway.app/health
```

Expected response: `{"status": "healthy"}`

### 5.2 Frontend Verification

Visit your Vercel frontend URL and verify:
- ✅ Application loads without errors
- ✅ Login/Register pages work
- ✅ API calls to backend succeed

## Step 6: Local Development Setup

### 6.1 Clone and Setup

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/resumeai-classifier.git
cd resumeai-classifier

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
```

### 6.2 Run Locally

```bash
# Backend (Terminal 1)
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (Terminal 2)
cd frontend
npm start
```

## Troubleshooting

### Common Issues

1. **Backend Deployment Fails**
   - Check Railway logs for errors
   - Verify all environment variables are set
   - Ensure `railway.json` is in the root directory

2. **Frontend Build Fails**
   - Check Vercel build logs
   - Verify all dependencies are in `package.json`
   - Ensure `vercel.json` is in the frontend directory

3. **CORS Errors**
   - Update `ALLOWED_ORIGINS` in Railway
   - Ensure frontend URL is correct
   - Redeploy backend after changes

4. **Database Connection Issues**
   - Verify DATABASE_URL in Railway
   - Check if PostgreSQL service is running
   - Ensure database tables are created

### Debug Commands

```bash
# Check backend logs
railway logs

# Check frontend build logs
# View in Vercel dashboard

# Test API endpoints
curl https://your-backend-domain.railway.app/health
```

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to Git
2. **HTTPS**: Both Railway and Vercel provide HTTPS by default
3. **CORS**: Properly configure allowed origins
4. **Rate Limiting**: Implement rate limiting for production
5. **Input Validation**: Validate all user inputs

## Performance Optimization

1. **Caching**: Implement Redis caching for frequently accessed data
2. **CDN**: Vercel provides global CDN for static assets
3. **Database Indexing**: Optimize database queries
4. **Image Optimization**: Compress uploaded resume files

## Monitoring

1. **Railway**: Monitor backend performance and logs
2. **Vercel**: Monitor frontend performance and analytics
3. **Database**: Monitor PostgreSQL performance
4. **Error Tracking**: Implement Sentry for error monitoring

## Cost Management

### Free Tier Limits

**Railway:**
- 500 hours/month free
- 1GB RAM per service
- Shared CPU

**Vercel:**
- Unlimited deployments
- 100GB bandwidth/month
- 100GB storage

### Optimization Tips

1. Use efficient database queries
2. Implement proper caching
3. Optimize bundle size
4. Use lazy loading for components

## Next Steps

1. **Custom Domain**: Add custom domain to your deployment
2. **SSL Certificate**: Both platforms provide automatic SSL
3. **CI/CD**: Set up automatic deployments on Git push
4. **Monitoring**: Add application monitoring and alerting
5. **Backup**: Set up database backups
6. **Scaling**: Plan for scaling when needed

## Support

- **Railway Documentation**: https://docs.railway.app
- **Vercel Documentation**: https://vercel.com/docs
- **GitHub Issues**: Create issues in your repository

---

**Your ResumeAI Classifier is now deployed and ready to use! 🎉** 