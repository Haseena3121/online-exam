# 🔒 HTTPS Deployment Guide for Phone Access

## 📱 Why HTTPS is Required for Phones

Modern browsers on phones **require HTTPS** for:
- ✅ Camera access
- ✅ Microphone access  
- ✅ All AI models (face detection, phone detection, etc.)
- ✅ WebRTC features

**Without HTTPS, camera and audio will NOT work on phones!**

---

## 🚀 Quick Deployment Options

### Option 1: Deploy on Render.com (Recommended - FREE HTTPS)

**Step 1: Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/exam-proctoring.git
git push -u origin main
```

**Step 2: Deploy on Render**

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Create **3 services**:

**Service A - MongoDB:**
- Name: `exam-mongo`
- Environment: `Docker`
- Plan: `Free`
- Click "Create Database" instead, choose MongoDB

**Service B - Backend:**
- Name: `exam-backend`
- Environment: `Docker`
- Root Directory: `backend`
- Plan: `Free`
- Add Environment Variables:
  ```
  MONGO_URI=mongodb://[YOUR_MONGO_CONNECTION_STRING]
  REDIS_URL=redis://[YOUR_REDIS_URL]
  JWT_SECRET_KEY=xK9#mP2$qL7nR4vT8wY1zA6bC3dE5fG0
  FLASK_ENV=production
  ```

**Service C - Frontend:**
- Name: `exam-frontend`
- Environment: `Docker`
- Root Directory: `frontend`
- Plan: `Free`
- Add Environment Variable:
  ```
  REACT_APP_API_URL=https://exam-backend.onrender.com
  ```

**Your HTTPS URLs will be:**
- Frontend: `https://exam-frontend.onrender.com` ← **Use this on phones!**
- Backend: `https://exam-backend.onrender.com`

---

### Option 2: Deploy on Railway.app (FREE HTTPS)

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Connect GitHub repository
4. Railway auto-detects Docker and deploys
5. Get your HTTPS URL: `https://your-app.railway.app`

---

### Option 3: Deploy on Vercel + Backend Hosting

**Frontend on Vercel (FREE HTTPS):**
```bash
cd frontend
npm install -g vercel
vercel --prod
```

**Backend on Render/Railway/Heroku**

Your URL: `https://your-app.vercel.app`

---

### Option 4: Use Ngrok for Testing (Temporary HTTPS)

**Quick test with HTTPS tunnel:**

```bash
# Install ngrok
# Download from https://ngrok.com/download

# Start your app locally
docker-compose up

# In another terminal, create HTTPS tunnel
ngrok http 80
```

**You'll get a URL like:**
```
https://abc123.ngrok.io ← Use this on your phone!
```

⚠️ **Note:** Ngrok URLs change every time you restart. Good for testing only.

---

### Option 5: Deploy on Your Own Server with Let's Encrypt

**Requirements:**
- A domain name (e.g., `examproctoring.com`)
- A server (VPS like DigitalOcean, AWS, etc.)

**Step 1: Point domain to your server**
- Add A record: `examproctoring.com` → `YOUR_SERVER_IP`

**Step 2: Install Docker and Docker Compose on server**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

**Step 3: Update docker-compose.yml for HTTPS**

Create `docker-compose.production.yml`:

```yaml
services:
  mongo:
    image: mongo:7
    container_name: exam_mongo
    restart: unless-stopped
    volumes:
      - mongo_data:/data/db
    networks:
      - exam_net

  redis:
    image: redis:7-alpine
    container_name: exam_redis
    restart: unless-stopped
    networks:
      - exam_net

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: exam_backend
    restart: unless-stopped
    env_file:
      - ./backend/.env.production
    environment:
      - MONGO_URI=mongodb://mongo:27017/exam_proctoring
      - REDIS_URL=redis://redis:6379/0
      - FLASK_ENV=production
    volumes:
      - evidence_uploads:/app/uploads/evidence
    depends_on:
      - mongo
      - redis
    networks:
      - exam_net
    expose:
      - "5000"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: exam_frontend
    restart: unless-stopped
    networks:
      - exam_net
    expose:
      - "80"

  # Nginx with SSL
  nginx:
    image: nginx:alpine
    container_name: exam_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - frontend
      - backend
    networks:
      - exam_net

  # Certbot for SSL certificates
  certbot:
    image: certbot/certbot
    container_name: exam_certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

volumes:
  mongo_data:
  evidence_uploads:

networks:
  exam_net:
    driver: bridge
```

**Step 4: Create nginx.conf**

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }

    upstream frontend {
        server frontend:80;
    }

    # HTTP - redirect to HTTPS
    server {
        listen 80;
        server_name examproctoring.com www.examproctoring.com;
        
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    # HTTPS
    server {
        listen 443 ssl;
        server_name examproctoring.com www.examproctoring.com;

        ssl_certificate /etc/letsencrypt/live/examproctoring.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/examproctoring.com/privkey.pem;

        # API requests
        location /api/ {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

**Step 5: Get SSL Certificate**

```bash
# Create directories
mkdir -p certbot/conf certbot/www

# Get certificate
docker-compose -f docker-compose.production.yml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  -d examproctoring.com \
  -d www.examproctoring.com \
  --email your-email@example.com \
  --agree-tos \
  --no-eff-email

# Start all services
docker-compose -f docker-compose.production.yml up -d
```

**Your HTTPS URL:** `https://examproctoring.com`

---

## 📱 Testing on Phone

1. **Open your HTTPS URL on phone:**
   - `https://your-app.onrender.com` (Render)
   - `https://your-app.railway.app` (Railway)
   - `https://abc123.ngrok.io` (Ngrok)
   - `https://examproctoring.com` (Your domain)

2. **Test camera access:**
   - Go to Camera Test page
   - Browser will ask for camera permission
   - Click "Allow"
   - Camera should work ✅

3. **Test during exam:**
   - Register as student
   - Start an exam
   - All AI models should work:
     - Face detection ✅
     - Phone detection ✅
     - Eye gaze tracking ✅
     - Sound detection ✅
     - Background blur ✅

---

## 🔧 Frontend Configuration for HTTPS

Update `frontend/.env.production`:

```env
# For Render/Railway/Vercel
REACT_APP_API_URL=https://your-backend-url.onrender.com

# For custom domain
REACT_APP_API_URL=https://api.examproctoring.com
```

Update `frontend/src/config.js` (if exists):

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.onrender.com';
export default API_URL;
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Frontend loads on HTTPS
- [ ] Backend API responds on HTTPS
- [ ] Camera works on phone
- [ ] Microphone works on phone
- [ ] Face detection works
- [ ] Phone detection works
- [ ] Eye gaze tracking works
- [ ] Sound detection works
- [ ] No mixed content warnings
- [ ] No CORS errors

---

## 🎯 Recommended: Render.com (Easiest)

**Why Render?**
- ✅ FREE HTTPS automatically
- ✅ Auto-deploys from GitHub
- ✅ Easy environment variables
- ✅ Free tier available
- ✅ Works perfectly on phones

**Your final URL:** `https://exam-frontend.onrender.com`

---

## 🆘 Troubleshooting

**Camera not working on phone?**
- ✅ Check URL starts with `https://`
- ✅ Check browser permissions
- ✅ Try Chrome or Safari on phone
- ✅ Clear browser cache

**Mixed content error?**
- ✅ Ensure ALL resources load via HTTPS
- ✅ Check API URL uses HTTPS
- ✅ Update frontend environment variables

**CORS errors?**
- ✅ Update backend CORS settings
- ✅ Add your frontend domain to allowed origins

---

## 📞 Quick Start Command

**For Render deployment:**
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Deploy to Render"
git push origin main

# 2. Go to render.com
# 3. Connect repo
# 4. Deploy!
```

**Your app will be live at:** `https://your-app.onrender.com`

**Test on phone immediately!** 📱✅
