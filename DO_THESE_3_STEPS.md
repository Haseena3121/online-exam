# ✅ Only 3 Things YOU Need To Do

Everything else is already configured. Just follow these steps.

---

## STEP 1 — Create Free MongoDB Database (2 minutes)

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up (free)
3. Click "Build a Database" → choose FREE tier → click "Create"
4. Username: `examadmin` | Password: `exam1234` → click "Create User"
5. Under "Where would you like to connect from?" → click "Allow Access from Anywhere" → "Add IP Address"
6. Click "Connect" → "Drivers" → copy the connection string

It looks like:
```
mongodb+srv://examadmin:exam1234@cluster0.xxxxx.mongodb.net/exam_proctoring
```

Save this — you need it in Step 3.

---

## STEP 2 — Push Code to GitHub (3 minutes)

1. Go to: https://github.com/new
2. Create a new repo named `exam-proctoring` (set to Public)
3. Open your terminal in this project folder and run:

```bash
git init
git add .
git commit -m "deploy"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/exam-proctoring.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

---

## STEP 3 — Deploy on Render (5 minutes)

1. Go to: https://render.com → Sign up with GitHub
2. Click "New +" → "Blueprint"
3. Select your `exam-proctoring` repo
4. Render will read the `render.yaml` file automatically

**You'll see 3 services being created:**
- `exam-backend`
- `exam-frontend`
- `exam-redis`

5. For `exam-backend`, click "Add Environment Variable":
   - Key: `MONGO_URI`
   - Value: paste your MongoDB connection string from Step 1

6. Click "Apply" → wait ~5 minutes for deployment

---

## ✅ Your HTTPS Links (after deployment)

| What | URL |
|------|-----|
| 📱 App (use on phone) | `https://exam-frontend.onrender.com` |
| 🔧 Backend API | `https://exam-backend.onrender.com` |

Open `https://exam-frontend.onrender.com` on your phone.
Camera, microphone, and all AI models will work automatically.

---

## ⚠️ Notes

- First load may take 30-60 seconds (free tier spins down when idle)
- Camera/mic will ask for permission on phone — click Allow
- If you change the Render service names, update `CORS_ORIGINS` and `REACT_APP_API_URL` accordingly
