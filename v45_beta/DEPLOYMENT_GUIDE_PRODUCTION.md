# YSenseAI v4.5-Beta: Production Deployment Guide

**Target**: ysenseai.org on Google Cloud Platform  
**Version**: 4.5-beta FINAL  
**Date**: November 27, 2025

---

## 🎯 What's Included

### Complete Platform Features
- ✅ User authentication (register/login)
- ✅ Personal wisdom library with search
- ✅ Story-first AI extraction (5 layers)
- ✅ Collaborative 3-word distillation dialogue
- ✅ Z-Protocol consent & attribution
- ✅ Export (JSON/MD/CSV for personal LLM)
- ✅ Public sharing links
- ✅ SQLite database (data vault)
- ✅ Quality metrics & analytics

---

## 📋 Prerequisites

### 1. Google Cloud Setup
- GCP project created
- Billing enabled
- Cloud Run or Compute Engine access

### 2. API Keys Required
```bash
# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-api03-...
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Alibaba Cloud (Qwen)
QWEN_API_KEY=sk-9f933e251786491bba21a0ddb3c417d1
QWEN_MODEL=qwen-plus
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

### 3. Domain Configuration
- Domain: ysenseai.org
- DNS pointing to GCP
- SSL certificate (Let's Encrypt or GCP managed)

---

## 🚀 Deployment Options

### Option A: Google Cloud Run (Recommended)

**Pros**: Auto-scaling, managed, easy  
**Cons**: Stateless (need Cloud SQL for production DB)

#### Step 1: Prepare Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY v45_beta/ .

# Expose port
EXPOSE 8080

# Run Streamlit
CMD ["streamlit", "run", "app_final.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]
```

#### Step 2: Build and Deploy
```bash
# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ysenseai

# Deploy to Cloud Run
gcloud run deploy ysenseai \
  --image gcr.io/YOUR_PROJECT_ID/ysenseai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="ANTHROPIC_API_KEY=sk-ant-...,QWEN_API_KEY=sk-9f..." \
  --memory 2Gi \
  --cpu 2

# Map custom domain
gcloud run services update ysenseai --platform managed --region us-central1 --domain ysenseai.org
```

### Option B: Compute Engine (Full Control)

**Pros**: Persistent storage, full control  
**Cons**: Manual scaling, more maintenance

#### Step 1: Create VM Instance
```bash
gcloud compute instances create ysenseai-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --tags=http-server,https-server
```

#### Step 2: SSH and Setup
```bash
# SSH into VM
gcloud compute ssh ysenseai-vm --zone=us-central1-a

# Install dependencies
sudo apt update
sudo apt install -y python3.11 python3-pip nginx certbot python3-certbot-nginx

# Clone repository
cd /opt
sudo git clone YOUR_REPO ysenseai
cd ysenseai/v45_beta

# Install Python packages
sudo pip3 install -r requirements.txt

# Configure API keys
sudo nano config.py
# Update QWEN_API_KEY and ANTHROPIC_API_KEY
```

#### Step 3: Setup Systemd Service
```bash
sudo nano /etc/systemd/system/ysenseai.service
```

```ini
[Unit]
Description=YSenseAI Platform
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ysenseai/v45_beta
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/streamlit run app_final.py --server.port 8501 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable ysenseai
sudo systemctl start ysenseai
sudo systemctl status ysenseai
```

#### Step 4: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/ysenseai
```

```nginx
server {
    listen 80;
    server_name ysenseai.org www.ysenseai.org;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/ysenseai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d ysenseai.org -d www.ysenseai.org
```

---

## 🗄️ Database Configuration

### Development (SQLite)
- Default: `database/ysense_production.db`
- Good for: Testing, low traffic (<100 users)
- Backup: Copy `.db` file regularly

### Production (Cloud SQL)
For >1000 users, migrate to PostgreSQL:

```bash
# Create Cloud SQL instance
gcloud sql instances create ysenseai-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create ysenseai --instance=ysenseai-db

# Update config.py
DATABASE_URL=postgresql://user:pass@/cloudsql/PROJECT:REGION:INSTANCE/ysenseai
```

---

## 🔒 Security Checklist

- [ ] API keys stored in environment variables (not in code)
- [ ] HTTPS enabled (SSL certificate)
- [ ] Database backups automated
- [ ] Password hashing (SHA-256)
- [ ] Session tokens secure (32-byte random)
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] Firewall rules configured

---

## 📊 Monitoring & Maintenance

### Health Check Endpoint
Add to `app_final.py`:
```python
@st.cache_data(ttl=60)
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
```

### Logging
```bash
# View logs (Compute Engine)
sudo journalctl -u ysenseai -f

# View logs (Cloud Run)
gcloud run services logs read ysenseai --region us-central1
```

### Backup Database
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /opt/ysenseai/v45_beta/database/ysense_production.db \
   /opt/backups/ysense_$DATE.db

# Keep only last 30 days
find /opt/backups -name "ysense_*.db" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /opt/scripts/backup_ysense.sh
```

---

## 🧪 Testing Checklist

### Pre-Deployment
- [ ] Register new account works
- [ ] Login/logout works
- [ ] Submit wisdom (full flow)
- [ ] Collaborative distillation works
- [ ] Library displays submissions
- [ ] Search finds content
- [ ] Export (JSON/MD/CSV) works
- [ ] Sharing links work
- [ ] Database persists data

### Post-Deployment
- [ ] HTTPS works (no certificate errors)
- [ ] Domain resolves correctly
- [ ] Performance acceptable (<3s page load)
- [ ] Mobile responsive
- [ ] API keys working (no fallback mode)
- [ ] Database backups running

---

## 📈 Scaling Strategy

### Phase 1: Launch (0-100 users)
- Compute Engine e2-medium
- SQLite database
- Single instance
- Manual backups

### Phase 2: Growth (100-1000 users)
- Compute Engine e2-standard-2
- Migrate to Cloud SQL PostgreSQL
- Add Redis for sessions
- Automated backups

### Phase 3: Scale (1000+ users)
- Cloud Run with auto-scaling
- Cloud SQL with read replicas
- Cloud CDN for static assets
- Cloud Monitoring & Alerting

---

## 🐛 Troubleshooting

### Issue: Streamlit Won't Start
```bash
# Check logs
sudo journalctl -u ysenseai -n 50

# Common fixes
sudo systemctl restart ysenseai
pip install --upgrade streamlit
```

### Issue: Database Locked
```bash
# SQLite issue - migrate to PostgreSQL or:
# Ensure only one process accesses DB
sudo systemctl restart ysenseai
```

### Issue: API Keys Not Working
```bash
# Verify environment variables
env | grep API_KEY

# Test APIs manually
python3 -c "from agents.anthropic_integration_v45 import AnthropicClient; print(AnthropicClient().use_fallback)"
```

### Issue: High Memory Usage
```bash
# Monitor
htop

# Restart service
sudo systemctl restart ysenseai

# Upgrade instance if needed
gcloud compute instances set-machine-type ysenseai-vm --machine-type e2-standard-2 --zone us-central1-a
```

---

## 📞 Support & Resources

### Documentation
- Master Plan: `YSENSEAI_V45_BETA_MASTERPLAN.md`
- TODO: `TODO_V45_BETA.md`
- Database Schema: `database/schema.py`

### Useful Commands
```bash
# Check service status
sudo systemctl status ysenseai

# View real-time logs
sudo journalctl -u ysenseai -f

# Restart service
sudo systemctl restart ysenseai

# Check disk space
df -h

# Check memory
free -h

# Check database size
du -h database/ysense_production.db
```

---

## 🎉 Launch Checklist

### Pre-Launch
- [ ] All features tested
- [ ] API keys configured
- [ ] Database initialized
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] Backups automated
- [ ] Monitoring set up

### Launch Day
- [ ] Deploy to production
- [ ] Verify HTTPS works
- [ ] Test user registration
- [ ] Test wisdom submission
- [ ] Monitor logs for errors
- [ ] Announce launch

### Post-Launch (Week 1)
- [ ] Monitor user signups
- [ ] Track submission quality
- [ ] Check database growth
- [ ] Review error logs
- [ ] Collect user feedback
- [ ] Plan improvements

---

**Version**: 4.5-beta FINAL  
**Last Updated**: November 27, 2025  
**Status**: Production Ready ✅

**Ready to deploy? Follow Option B (Compute Engine) for full control, or Option A (Cloud Run) for simplicity.**
