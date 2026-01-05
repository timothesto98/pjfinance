# PJFinance Deployment Instructions for Windows Users

## Overview
This guide will help you deploy PJFinance to Render (completely free, no credit card required).

---

## Step 1: Create a GitHub Account (Required for Deployment)

1. Open your browser and go to: **https://github.com/signup**
2. Enter your email address
3. Create a password
4. Choose a username (e.g., `yourname-pjfinance`)
5. Click "Create account"
6. Verify your email by clicking the link GitHub sends you
7. You now have a GitHub account

---

## Step 2: Create a GitHub Repository

1. Go to: **https://github.com/new**
2. Fill in the form:
   - **Repository name:** `pjfinance`
   - **Description:** `PJFinance Microfinance Management System`
   - **Visibility:** Select "Public"
3. Click "Create repository"
4. You will see a page with instructions. **STOP HERE** and follow the next step.

---

## Step 3: Upload the ZIP File to GitHub

**Option A: Using GitHub Web Interface (Easiest for Beginners)**

1. On the repository page you just created, click the green "Code" button
2. Click "Upload files"
3. Drag and drop the `pjfinance_permanent.zip` file into the upload area (or click to browse)
4. At the bottom, click "Commit changes"
5. GitHub will extract the ZIP file automatically

**Option B: Using Git Command (If you have Git installed)**

If you have Git installed on Windows:

1. Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
2. Navigate to where you extracted the ZIP file:
   ```
   cd C:\Users\YourUsername\Downloads\pjfinance_deploy
   ```
3. Run these commands one by one:
   ```
   git init
   git add .
   git commit -m "Initial PJFinance deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/pjfinance.git
   git push -u origin main
   ```
   (Replace `YOUR_USERNAME` with your GitHub username)

---

## Step 4: Deploy to Render

1. Go to: **https://render.com**
2. Click "Get Started" or "Sign Up"
3. Click "Continue with GitHub"
4. Click "Authorize render-oss" to connect your GitHub account
5. You will be redirected to Render. Click "New +" button (top right)
6. Select "Web Service"
7. Under "GitHub," find and select your `pjfinance` repository
8. Click "Connect"
9. Fill in the deployment settings:
   - **Name:** `pjfinance`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
10. Click "Create Web Service"
11. Wait 3-5 minutes for deployment to complete
12. You will see a URL like: `https://pjfinance-xxxxx.onrender.com`

**That URL is your permanent live application!**

---

## Step 5: Test Your Deployment

1. Once Render shows "Live," copy your URL
2. Open it in your browser
3. You should see: `{"message":"PJFinance App is running"}`
4. Test the health endpoint: `https://your-url/health`
5. You should see: `{"status":"ok"}`

---

## Troubleshooting

**Problem: Deployment fails**
- Check the Render logs (click "Logs" in Render dashboard)
- Make sure all files are in the repository

**Problem: Page shows "Service Unavailable"**
- Wait a few more minutes for deployment to complete
- Refresh the page

**Problem: 404 Error**
- Make sure you're accessing the correct URL from Render
- Check that the URL ends with `/` or `/health`

---

## Important Notes

- **Render Free Tier:** Your app will spin down after 15 minutes of inactivity. It will restart when you access it (takes 30 seconds).
- **No Credit Card Required:** Render's free tier is completely free
- **Permanent URL:** Your URL will remain the same as long as the repository exists

---

## Need Help?

If you get stuck:
1. Check the Render logs for error messages
2. Verify all files are in your GitHub repository
3. Make sure `main.py` and `requirements.txt` are in the root directory

