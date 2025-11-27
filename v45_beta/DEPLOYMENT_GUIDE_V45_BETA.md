# YSenseAI v4.5-Beta: Production Deployment Guide

**Version**: 4.5-beta  
**Target Domain**: ysenseai.org  
**Launch Date**: December 4, 2025  
**Status**: Ready for Production ✅

---

## 🎯 Overview

YSenseAI v4.5-Beta is a complete wisdom extraction and attribution platform with:

- **5-Layer Perception Toolkit** - Structured wisdom extraction
- **AI Distillation** - 3-word essence generation (Claude)
- **Quality Metrics** - 6 training optimization signals
- **Z-Protocol Consent** - 3-tier revenue sharing (15-30%)
- **Attribution Engine** - Cryptographic signing + DID
- **Export Pipeline** - Training-ready datasets (JSONL, Alpaca, ShareGPT)
- **Transparency Dashboard** - Real-time quality & revenue tracking

---

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11+
- **RAM**: 2GB minimum
- **Storage**: 5GB minimum
- **OS**: Ubuntu 22.04 or compatible Linux

### API Keys Required
1. **Anthropic (Claude)**: For AI distillation
   - Model: `claude-3-haiku-20240307`
   - Get key: https://console.anthropic.com/

2. **Alibaba Cloud (Qwen)**: For quality analysis
   - Model: `qwen-plus`
   - Region: Singapore (`dashscope-intl.aliyuncs.com`)
   - Get key: https://www.alibabacloud.com/help/zh/model-studio/get-api-key

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone Repository
```bash
cd /opt
git clone https://github.com/your-org/ysenseai-platform.git
cd ysenseai-platform/v45_beta
```

### Step 2: Install Dependencies
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure API Keys
Edit `config.py` and update:
```python
QWEN_API_KEY = "your-qwen-api-key-here"
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
```

### Step 4: Test Installation
```bash
python test_integration.py
```

Expected output: `✅ All systems operational!`

### Step 5: Launch Application
```bash
streamlit run app_complete.py --server.port 8501
```

Access at: `http://your-domain.com:8501`

---

## 📦 File Structure

```
v45_beta/
├── app_complete.py              # Main Streamlit application
├── config.py                    # Configuration & API keys
├── test_integration.py          # End-to-end test
├── requirements.txt             # Python dependencies
│
├── ui/
│   └── layer_config.py          # 5-layer perception config
│
├── agents/
│   ├── anthropic_integration_v45.py  # Claude integration
│   └── qwen_integration_v45.py       # Qwen integration
│
├── attribution/
│   ├── attribution_engine.py    # Cryptographic attribution
│   └── quality_metrics.py       # Training quality calculator
│
├── exports/
│   └── export_pipeline.py       # Dataset export (JSONL, Alpaca, etc.)
│
└── database/
    └── ysense_v45_beta.db       # SQLite database (auto-created)
```

---

## 🔧 Production Configuration

### 1. Environment Variables

Create `.env` file (optional, config.py has defaults):
```bash
# API Keys
QWEN_API_KEY=sk-9f933e251786491bba21a0ddb3c417d1
QWEN_MODEL=qwen-plus
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1

ANTHROPIC_API_KEY=sk-ant-api03-...
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Platform
PLATFORM_NAME=YSenseAI v4.5-Beta
PLATFORM_VERSION=4.5-beta
DATABASE_URL=sqlite:///database/ysense_v45_beta.db
```

### 2. Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#4c1d95"
backgroundColor = "#FDFBF7"
secondaryBackgroundColor = "#ffffff"
textColor = "#1e293b"
font = "sans serif"
```

### 3. Systemd Service (Auto-restart)

Create `/etc/systemd/system/ysenseai.service`:
```ini
[Unit]
Description=YSenseAI v4.5-Beta Platform
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ysenseai-platform/v45_beta
Environment="PATH=/opt/ysenseai-platform/venv/bin"
ExecStart=/opt/ysenseai-platform/venv/bin/streamlit run app_complete.py --server.port 8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ysenseai
sudo systemctl start ysenseai
sudo systemctl status ysenseai
```

### 4. Nginx Reverse Proxy

Create `/etc/nginx/sites-available/ysenseai`:
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
        
        # WebSocket support
        proxy_read_timeout 86400;
    }
}
```

Enable and reload:
```bash
sudo ln -s /etc/nginx/sites-available/ysenseai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ysenseai.org -d www.ysenseai.org
```

---

## 🧪 Testing Checklist

### Pre-Deployment Tests

- [ ] **API Connectivity**
  ```bash
  python -c "from agents.anthropic_integration_v45 import AnthropicClient; print(AnthropicClient().use_fallback)"
  python -c "from agents.qwen_integration_v45 import QWENClient; print(QWENClient().use_fallback)"
  ```
  Expected: Both return `False`

- [ ] **End-to-End Workflow**
  ```bash
  python test_integration.py
  ```
  Expected: `✅ All systems operational!`

- [ ] **UI Accessibility**
  - Open browser to `http://localhost:8501`
  - Test story submission
  - Verify all 5 layers work
  - Check quality metrics display
  - Confirm attribution proof visible

- [ ] **Export Functionality**
  - Submit test wisdom
  - Download JSON
  - Verify JSONL format
  - Check dataset card generation

### Post-Deployment Monitoring

- [ ] **Health Check**
  ```bash
  curl -I https://ysenseai.org
  ```
  Expected: `200 OK`

- [ ] **Performance**
  - Page load time < 3 seconds
  - AI distillation < 10 seconds
  - Quality calculation < 2 seconds

- [ ] **Logs**
  ```bash
  sudo journalctl -u ysenseai -f
  ```
  Monitor for errors

---

## 📊 Core Metrics to Track

### User Engagement
- Total submissions
- Completion rate (story → minting)
- Average quality score
- Tier distribution (tier1/tier3/tier4)

### Technical Performance
- API response times
- Error rates
- Database size
- Export volume

### Business Metrics
- Training-ready submissions
- Revenue potential (mock calculation)
- User retention
- Dataset downloads

---

## 🔒 Security Considerations

### API Key Protection
- ✅ Never commit API keys to Git
- ✅ Use environment variables or config.py
- ✅ Restrict file permissions: `chmod 600 config.py`

### Data Privacy
- ✅ User data stored locally (SQLite)
- ✅ No external data transmission (except AI APIs)
- ✅ Attribution proof cryptographically signed

### HTTPS
- ✅ Force HTTPS in production
- ✅ Use Let's Encrypt for free SSL
- ✅ Enable HSTS headers

---

## 🐛 Troubleshooting

### Issue: API Authentication Errors

**Symptom**: `401 - invalid x-api-key`

**Solution**:
1. Verify API keys in `config.py`
2. Check key format (no extra spaces)
3. For Qwen: Ensure Singapore region endpoint
4. For Claude: Verify model name is `claude-3-haiku-20240307`

### Issue: Streamlit Won't Start

**Symptom**: `ModuleNotFoundError` or port conflicts

**Solution**:
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check port availability
sudo lsof -i :8501

# Use different port
streamlit run app_complete.py --server.port 8502
```

### Issue: Quality Scores Always Low

**Symptom**: All submissions get < 0.60 quality score

**Solution**:
- Ensure layer responses are detailed (>50 words each)
- Include cultural markers and emotional descriptors
- Add specific, verifiable details
- Check that all 5 layers are filled

### Issue: Export Files Empty

**Symptom**: JSONL/CSV files have 0 bytes

**Solution**:
- Verify submissions are marked `training_ready: True`
- Check quality scores meet thresholds
- Ensure export directory has write permissions

---

## 📈 Scaling Considerations

### Database Migration (SQLite → PostgreSQL)

When submissions exceed 10,000:
```python
# Update config.py
DATABASE_URL = "postgresql://user:pass@localhost/ysense_v45_beta"
```

### Load Balancing

For high traffic (>1000 concurrent users):
- Deploy multiple Streamlit instances
- Use Nginx load balancer
- Consider Redis for session state

### API Rate Limiting

Monitor API usage:
- Claude: 50,000 tokens/min (Haiku)
- Qwen: Check Alibaba Cloud limits

Implement queuing for high load.

---

## 🎯 Success Criteria

### Launch Day (December 4, 2025)
- [ ] Platform accessible at ysenseai.org
- [ ] SSL certificate active
- [ ] All 5 layers functional
- [ ] AI distillation working
- [ ] Quality metrics accurate
- [ ] Export pipeline operational

### Week 1
- [ ] 10+ wisdom submissions
- [ ] Average quality score > 0.70
- [ ] Zero critical errors
- [ ] User feedback collected

### Q1 2026 Target
- [ ] €15,000 revenue potential
- [ ] 1000+ training-ready submissions
- [ ] Partnership with 1 AI lab
- [ ] Dataset published on HuggingFace

---

## 📞 Support & Contact

**Technical Issues**:
- GitHub: https://github.com/your-org/ysenseai-platform/issues
- Email: alton@ysenseai.org or creator35lwb@gmail.com

**Business Inquiries**:
- Website: https://ysenseai.org
- Email: partnerships@ysenseai.org

**Documentation**:
- Master Plan: `/YSENSEAI_V45_BETA_MASTERPLAN.md`
- TODO: `/TODO_V45_BETA.md`
- API Docs: `/agents/README.md`

---

## 🎉 Deployment Checklist

Final checklist before going live:

- [ ] All dependencies installed
- [ ] API keys configured and tested
- [ ] End-to-end test passed
- [ ] Systemd service enabled
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed
- [ ] Domain DNS pointing to server
- [ ] Monitoring tools set up
- [ ] Backup strategy in place
- [ ] Team trained on platform

**Ready to deploy?** Run:
```bash
sudo systemctl start ysenseai
sudo systemctl status ysenseai
curl https://ysenseai.org
```

---

**Version**: 4.5-beta  
**Last Updated**: November 27, 2025  
**Status**: Production Ready ✅
