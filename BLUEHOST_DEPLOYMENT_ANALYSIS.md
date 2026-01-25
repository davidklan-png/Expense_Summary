# Bluehost Deployment Feasibility Analysis
## Saison Transform Web Hosting Options

**Generated**: 2026-01-23
**Current Version**: 0.2.3
**Current Stack**: Python 3.10+, Streamlit, Poetry

---

## Executive Summary

**Can Saison Transform run on Bluehost?**
**Short Answer**: ⚠️ **Possible but NOT RECOMMENDED** for shared hosting. **YES** for VPS/Dedicated plans with significant modifications.

**Recommended Alternatives**: Render, Railway, PythonAnywhere, or Heroku (better Python support, easier deployment).

---

## Table of Contents

1. [Current Architecture Analysis](#current-architecture-analysis)
2. [Bluehost Hosting Tiers](#bluehost-hosting-tiers)
3. [Technical Challenges](#technical-challenges)
4. [Deployment Options](#deployment-options)
5. [Required Modifications](#required-modifications)
6. [Better Alternatives](#better-alternatives)
7. [Cost Comparison](#cost-comparison)
8. [Recommendation](#recommendation)

---

## 1. Current Architecture Analysis

### Technology Stack

```
┌─────────────────────────────────────────┐
│  Frontend: Streamlit (Python-based)    │
│  - Runs on port 8501                    │
│  - Requires persistent process          │
│  - WebSocket connections                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Backend: Python 3.10-3.13              │
│  - pandas, numpy (data processing)      │
│  - Jinja2 (HTML templates)              │
│  - chardet (encoding detection)         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Storage: Local File System             │
│  - data/input (CSV uploads)             │
│  - data/output (reports)                │
│  - data/reference (config, NameList)    │
│  - data/archive (monthly archives)      │
└─────────────────────────────────────────┘
```

### Key Requirements

1. **Python 3.10+**: Modern Python version
2. **Long-running process**: Streamlit server must stay running
3. **Port access**: Needs to listen on a port (default 8501)
4. **File uploads**: Write access to directories
5. **Memory**: ~200-500MB for pandas/numpy operations
6. **Dependencies**: 15+ Python packages via Poetry

---

## 2. Bluehost Hosting Tiers

### 2.1 Shared Hosting (Basic, Plus, Choice Plus)

**Price**: $2.95 - $13.95/month

**Python Support**:
- ❌ Python available but **limited to version 3.6-3.8** (too old)
- ❌ No root/sudo access
- ❌ No systemd/process managers
- ❌ CGI/FastCGI only (not suitable for Streamlit)
- ❌ Cannot run persistent processes
- ❌ Limited pip/Poetry support
- ❌ No custom port access

**Verdict**: ❌ **NOT COMPATIBLE** - Cannot run Streamlit

---

### 2.2 VPS Hosting (Standard, Enhanced, Ultimate)

**Price**: $18.99 - $59.99/month

**Python Support**:
- ✅ Root access (can install Python 3.10+)
- ✅ Can run persistent processes
- ✅ systemd for process management
- ✅ Full pip/Poetry support
- ✅ Custom port access
- ⚠️ Requires manual server administration

**Verdict**: ✅ **COMPATIBLE** - But requires significant setup

---

### 2.3 Dedicated Hosting

**Price**: $79.99 - $119.99/month

**Python Support**:
- ✅ Full root access
- ✅ Complete control over environment
- ✅ Can install any Python version
- ✅ Process management

**Verdict**: ✅ **COMPATIBLE** - But expensive and overkill

---

## 3. Technical Challenges

### Challenge 1: Streamlit Requires Persistent Process

**Problem**: Streamlit is a long-running web server, but Bluehost shared hosting only supports:
- PHP (Apache mod_php)
- Python CGI/WSGI (one request, one process lifecycle)

**Streamlit Architecture**:
```python
# Streamlit runs like this:
streamlit run web_app.py
# Creates persistent server on port 8501
# Maintains WebSocket connections
# Keeps session state in memory
```

**Bluehost Shared Hosting**:
- Cannot keep processes running
- Kills processes after request completes
- No process supervisor (systemd, supervisor, pm2)

**Solution**: Need VPS or convert to Flask/Django

---

### Challenge 2: Python Version Limitations

**Required**: Python 3.10 - 3.13
**Bluehost Shared**: Python 3.6 - 3.8

**Breaking Changes**:
- Type hints syntax (`list[str]` not available in 3.8)
- Match statements (Python 3.10+ only)
- Improved error messages
- Performance improvements

**Solution**: Need VPS with custom Python installation

---

### Challenge 3: Port Access & Proxy

**Problem**: Streamlit runs on port 8501

**Bluehost Shared**:
- Only ports 80 (HTTP) and 443 (HTTPS) accessible
- Cannot bind custom ports
- No reverse proxy configuration

**Bluehost VPS**:
- Need to configure Apache/Nginx reverse proxy
- Forward requests from port 80 → 8501

**Example Nginx Config Needed**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

### Challenge 4: File System Permissions

**Requirements**:
- Write access to `data/input`, `data/output`, `data/archive`
- Create temporary files
- Read/write CSV files

**Bluehost Shared**:
- Limited directory permissions
- Cannot write outside specific directories
- `/tmp` may have size limits

**Solution**: Configure proper directory permissions and paths

---

### Challenge 5: Memory & CPU Limits

**Pandas/NumPy Requirements**:
- Loading CSV: ~50-200MB RAM
- Processing: Up to 500MB for large files
- NumPy operations can be CPU-intensive

**Bluehost Shared**:
- Memory limits: ~512MB - 1GB (shared with other sites)
- CPU throttling for high usage
- May timeout on large files

**Solution**: VPS with dedicated resources

---

### Challenge 6: Dependency Installation

**Current**: Poetry for dependency management

**Bluehost Shared**:
- No Poetry pre-installed
- Limited pip version
- Cannot install build tools (gcc, make) for some packages
- No virtual environment control

**Bluehost VPS**:
- Full control, can install Poetry
- Need to compile some dependencies

---

## 4. Deployment Options

### Option A: Bluehost VPS with Streamlit (POSSIBLE)

**Complexity**: 🔴 High
**Cost**: $18.99 - $59.99/month
**Recommended For**: Teams already using Bluehost

**Steps**:
1. Order Bluehost VPS (Standard or higher)
2. Install Python 3.10+ from source
3. Install Poetry
4. Clone repository and install dependencies
5. Configure systemd service for Streamlit
6. Set up Nginx reverse proxy
7. Configure SSL (Let's Encrypt)
8. Set up firewall rules

**Pros**:
- Keep existing Streamlit UI
- Full control over environment

**Cons**:
- Requires Linux administration skills
- Manual server management
- More expensive than specialized Python hosts
- No auto-scaling
- Manual security updates

---

### Option B: Convert to Flask/Django + Bluehost Shared (MAJOR REWRITE)

**Complexity**: 🔴🔴🔴 Very High
**Cost**: $2.95 - $13.95/month
**Recommended For**: Not recommended (too much work)

**Required Changes**:
1. **Replace Streamlit with Flask/Django**
   - Rewrite entire UI (394 lines in web_app.py)
   - Rewrite 3,039 lines in src/saisonxform/ui/
   - Convert session state to Flask sessions
   - Build HTML forms for file upload
   - Implement AJAX for interactivity

2. **Convert to WSGI**
   - Create wsgi.py entry point
   - Configure .htaccess for mod_wsgi
   - Handle file uploads differently

3. **Database for Session State**
   - Add SQLite or MySQL for persistent storage
   - Store processed data between requests

**Estimated Effort**: 40-60 hours of development

**Pros**:
- Works on cheap shared hosting
- Standard web hosting model

**Cons**:
- Massive rewrite (basically a new application)
- Lose Streamlit's reactive UI
- Much more complex code
- Harder to maintain

---

### Option C: Docker Container on Bluehost VPS (MODERATE)

**Complexity**: 🟡 Moderate
**Cost**: $18.99+/month
**Recommended For**: Teams familiar with Docker

**Steps**:
1. Order Bluehost VPS
2. Install Docker
3. Create Dockerfile for Saison Transform
4. Build and run container
5. Configure reverse proxy
6. Set up Docker Compose for management

**Example Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Pros**:
- Reproducible environment
- Easier deployment
- Isolated from host system

**Cons**:
- Still requires VPS
- Docker overhead
- Need to learn Docker

---

## 5. Required Modifications for Bluehost VPS

### 5.1 Configuration Changes

**Update `web_app.py`**:
```python
# Add production configuration
st.set_page_config(
    page_title="Saison Transform",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add production mode detection
import os
PRODUCTION = os.getenv("STREAMLIT_PRODUCTION", "false").lower() == "true"

if PRODUCTION:
    # Disable file watcher (saves resources)
    # Disable development features
    pass
```

**Create systemd service** (`/etc/systemd/system/saisonxform.service`):
```ini
[Unit]
Description=Saison Transform Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/saisonxform
Environment="PATH=/var/www/saisonxform/.venv/bin"
ExecStart=/var/www/saisonxform/.venv/bin/streamlit run web_app.py --server.port=8501 --server.address=127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration** (`/etc/nginx/sites-available/saisonxform`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Redirect to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeouts for large file uploads
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # Increase max upload size
    client_max_body_size 50M;
}
```

### 5.2 Environment Configuration

**Create `.env` file**:
```bash
# Production settings
STREAMLIT_PRODUCTION=true
INPUT_DIR=/var/www/saisonxform/data/input
REFERENCE_DIR=/var/www/saisonxform/data/reference
OUTPUT_DIR=/var/www/saisonxform/data/output
ARCHIVE_DIR=/var/www/saisonxform/data/archive
```

### 5.3 File Upload Size Limits

**Streamlit Config** (`~/.streamlit/config.toml`):
```toml
[server]
maxUploadSize = 50  # MB
port = 8501
address = "127.0.0.1"
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

---

## 6. Better Alternatives to Bluehost

### Option 1: Render (RECOMMENDED)

**Pricing**: FREE tier available, $7/month for paid
**Python Support**: ✅ Excellent
**Complexity**: 🟢 Low (easiest deployment)

**Why Render**:
- ✅ Native Streamlit support
- ✅ Automatic HTTPS
- ✅ Git-based deployment (auto-deploy on push)
- ✅ Built-in logging and monitoring
- ✅ Free tier for testing
- ✅ Persistent disk storage
- ✅ No server management required

**Deployment Steps**:
1. Push code to GitHub
2. Connect Render to repository
3. Create new "Web Service"
4. Set build command: `pip install poetry && poetry install`
5. Set start command: `streamlit run web_app.py`
6. Deploy

**Cost**:
- Free tier: 750 hours/month
- Starter: $7/month (always on)
- Standard: $25/month (more resources)

---

### Option 2: Railway

**Pricing**: FREE $5 credit/month, then $0.000231/GB-hour
**Python Support**: ✅ Excellent
**Complexity**: 🟢 Low

**Why Railway**:
- ✅ One-click Streamlit deployment
- ✅ Automatic HTTPS
- ✅ Git integration
- ✅ Environment variables via dashboard
- ✅ Database support (PostgreSQL, MySQL)
- ✅ Volume storage for files

**Deployment**: Connect GitHub → Deploy

---

### Option 3: PythonAnywhere

**Pricing**: FREE tier, $5/month basic
**Python Support**: ✅ Excellent
**Complexity**: 🟡 Moderate

**Why PythonAnywhere**:
- ✅ Python-focused hosting
- ✅ Pre-installed Python 3.10+
- ✅ Web-based IDE
- ✅ Scheduled tasks (for archives)
- ⚠️ Requires WSGI conversion (no Streamlit on free tier)
- ✅ $5/month tier supports Streamlit

---

### Option 4: Heroku

**Pricing**: $5/month minimum (Eco dyno)
**Python Support**: ✅ Excellent
**Complexity**: 🟡 Moderate

**Why Heroku**:
- ✅ Mature platform
- ✅ Streamlit support
- ✅ Add-ons (databases, monitoring)
- ✅ CLI tools
- ⚠️ No free tier anymore
- ⚠️ File storage is ephemeral (need S3 for persistence)

---

### Option 5: AWS Lightsail

**Pricing**: $3.50/month (512MB RAM)
**Python Support**: ✅ Good
**Complexity**: 🟡 Moderate

**Why Lightsail**:
- ✅ Cheap VPS
- ✅ AWS integration
- ✅ Persistent storage
- ⚠️ Requires server setup (similar to Bluehost VPS)

---

### Option 6: Google Cloud Run

**Pricing**: Pay-per-use (FREE tier: 2M requests/month)
**Python Support**: ✅ Excellent
**Complexity**: 🟡 Moderate (requires Docker)

**Why Cloud Run**:
- ✅ Serverless (auto-scaling)
- ✅ Pay only for actual usage
- ✅ Generous free tier
- ⚠️ Requires containerization
- ⚠️ Stateless (need Cloud Storage for files)

---

## 7. Cost Comparison (Annual)

| Platform | Free Tier | Paid Tier | Annual Cost | Complexity |
|----------|-----------|-----------|-------------|------------|
| **Render** | ✅ Yes (limited) | $7/month | $84/year | 🟢 Low |
| **Railway** | ✅ $5 credit/mo | ~$10-15/mo | ~$120-180/year | 🟢 Low |
| **PythonAnywhere** | ✅ Yes (no Streamlit) | $5/month | $60/year | 🟡 Moderate |
| **Heroku** | ❌ No | $5/month | $60/year | 🟡 Moderate |
| **Bluehost Shared** | ❌ No | $3-14/month | $36-168/year | 🔴 **NOT COMPATIBLE** |
| **Bluehost VPS** | ❌ No | $19-60/month | $228-720/year | 🔴 High |
| **AWS Lightsail** | ❌ No | $3.50/month | $42/year | 🟡 Moderate |
| **Google Cloud Run** | ✅ 2M req/mo | Pay-per-use | $0-50/year | 🟡 Moderate |

---

## 8. Recommendation

### For Most Users: **Render** or **Railway**

**Recommended Choice**: **Render (Free or Starter plan)**

**Why**:
1. ✅ **Easiest deployment** - No server management
2. ✅ **Native Streamlit support** - No code changes needed
3. ✅ **Free tier for testing** - Try before buying
4. ✅ **Automatic HTTPS** - Security built-in
5. ✅ **Git-based workflow** - Push to deploy
6. ✅ **Better support for Python** than Bluehost
7. 💰 **Cheaper than Bluehost VPS** - $7/mo vs $19+/mo

**Deployment Time**: ~15 minutes (vs hours for Bluehost VPS setup)

---

### If You Must Use Bluehost

**Only viable option**: **Bluehost VPS ($18.99+/month)**

**Why NOT Shared Hosting**:
- ❌ Cannot run Streamlit (no persistent processes)
- ❌ Python version too old
- ❌ Converting to Flask = 40-60 hours of work

**VPS Setup Checklist**:
1. Order VPS (Standard tier minimum)
2. Install Python 3.10+ from source (~30 min)
3. Install Poetry and dependencies (~15 min)
4. Configure systemd service (~15 min)
5. Set up Nginx reverse proxy (~30 min)
6. Configure SSL with Let's Encrypt (~15 min)
7. Set up firewall and security (~30 min)
8. Deploy and test (~30 min)

**Total Setup Time**: ~3-4 hours (requires Linux skills)

**Ongoing Maintenance**:
- Security updates (monthly)
- Python version updates (quarterly)
- Dependency updates (monthly)
- Server monitoring
- Backup management

---

## 9. Migration Plan: Bluehost Shared → Render

### Step 1: Prepare Repository

```bash
# Ensure repository is clean and tested
git status
poetry run pytest
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up (free)
3. Connect GitHub account

### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Select repository: `Expense_Summary`
3. Configure:
   - **Name**: `saison-transform`
   - **Environment**: `Python 3`
   - **Build Command**:
     ```bash
     pip install poetry && poetry install
     ```
   - **Start Command**:
     ```bash
     streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0
     ```
   - **Instance Type**: Free (or Starter for $7/mo)

### Step 4: Configure Environment Variables

In Render dashboard, add:
```
REFERENCE_DIR=data/reference
INPUT_DIR=data/input
OUTPUT_DIR=data/output
ARCHIVE_DIR=data/archive
```

### Step 5: Add Persistent Disk (Optional)

If you need to persist uploaded files:
1. Add disk in Render dashboard
2. Mount at `/data`
3. Update paths to use `/data/input`, etc.

### Step 6: Deploy

1. Click "Create Web Service"
2. Wait for deployment (~5 minutes)
3. Access at: `https://saison-transform.onrender.com`

### Step 7: Custom Domain (Optional)

1. In Render dashboard: Settings → Custom Domain
2. Add your domain
3. Update DNS with CNAME record

**Total Migration Time**: ~30 minutes

---

## 10. Quick Start: Deploy to Render NOW

### Create `render.yaml` (Infrastructure as Code)

Add to repository root:

```yaml
services:
  - type: web
    name: saison-transform
    env: python
    region: oregon
    plan: free  # or 'starter' for $7/mo
    buildCommand: pip install poetry && poetry install
    startCommand: streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
    healthCheckPath: /_stcore/health
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: REFERENCE_DIR
        value: data/reference
      - key: INPUT_DIR
        value: data/input
      - key: OUTPUT_DIR
        value: data/output
      - key: ARCHIVE_DIR
        value: data/archive

    # Optional: persistent disk
    # disk:
    #   name: saison-data
    #   mountPath: /data
    #   sizeGB: 1
```

### Commit and Push

```bash
git add render.yaml
git commit -m "feat: add Render deployment configuration"
git push origin main
```

### Deploy

1. Go to Render dashboard
2. "New +" → "Blueprint"
3. Select repository
4. Render will auto-detect `render.yaml`
5. Click "Apply"

**Done!** Your app is live.

---

## 11. Conclusion

### Summary Table

| Factor | Bluehost Shared | Bluehost VPS | Render |
|--------|-----------------|--------------|---------|
| **Compatible?** | ❌ No | ✅ Yes | ✅ Yes |
| **Code Changes?** | 🔴 Major rewrite | 🟢 Minor | 🟢 None |
| **Setup Time** | N/A | 🔴 3-4 hours | 🟢 15 min |
| **Monthly Cost** | $3-14 | $19-60 | $0-7 |
| **Python Support** | ⭐ Poor | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Maintenance** | N/A | 🔴 High | 🟢 None |
| **Recommended** | ❌ No | ⚠️ Only if necessary | ✅ **Yes** |

---

### Final Recommendation

**🎯 Best Option: Deploy to Render**

**Reasons**:
1. **Zero code changes required**
2. **15-minute deployment** vs hours of VPS setup
3. **$7/month** vs $19+ for Bluehost VPS
4. **Better Python ecosystem support**
5. **No server maintenance**
6. **Free tier for testing**
7. **Automatic scaling and updates**

**When to Use Bluehost**:
- ✅ You already have Bluehost VPS for other services
- ✅ Your team has Linux administration skills
- ✅ You need on-premise-like control
- ❌ Never use Bluehost Shared for this application

---

## 12. Next Steps

### Recommended Path

1. **Test on Render Free Tier** (Today - 30 min)
   - Deploy to Render
   - Test all functionality
   - Verify file uploads work

2. **Evaluate Performance** (This Week)
   - Monitor response times
   - Test with real data
   - Check memory usage

3. **Decision Point** (End of Week)
   - If satisfied → Upgrade to Render Starter ($7/mo)
   - If need more control → Consider Bluehost VPS
   - If need self-hosting → AWS Lightsail ($3.50/mo)

### Resources

- **Render Deployment Guide**: https://render.com/docs/deploy-streamlit-app
- **Streamlit Cloud (Alternative)**: https://streamlit.io/cloud
- **Railway Deployment**: https://railway.app/template/streamlit

---

**Questions?** Let me know which deployment path you'd like to pursue, and I can provide detailed step-by-step instructions.
