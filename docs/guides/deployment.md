# Streamlit Cloud Deployment Guide

Quick reference for deploying Saison Transform web interface to Streamlit Cloud.

## Quick Deploy to Streamlit Cloud

### Step 1: Prerequisites
- ✅ GitHub account
- ✅ Streamlit Cloud account ([sign up free](https://share.streamlit.io))

### Step 2: Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Fill in the form:
   - **Repository:** `davidklan-png/Expense_Summary`
   - **Branch:** `develop`
   - **Main file path:** `web_app.py`
   - **App URL:** Choose your custom name (e.g., `saison-transform`)

4. Click **"Deploy"**
5. Wait 2-3 minutes ⏱️
6. Your app is live! 🎉

## Deployment Parameters

All required files are already in the repository:

### 📄 requirements.txt
```txt
streamlit>=1.51.0
pandas>=2.2.0
numpy>=2.0.0
chardet>=5.0.0
jinja2>=3.1.0
typer==0.9.0
click==8.1.3
tomli>=2.0.1; python_version < "3.11"
```

### ⚙️ .streamlit/config.toml
- **Theme:** Custom blue theme
- **Max upload:** 200MB
- **Server mode:** Headless
- **CORS:** Disabled (secure)

### 📁 Data Files (Included)
- `data/reference/NameList.csv` - Attendee list
- `data/reference/config.toml` - Processing configuration

## Post-Deployment Setup

### Upload Your Attendee List

1. Open your deployed app
2. Navigate to **"⚙️ Settings"** → **"Manage Attendees"**
3. Upload your `NameList.csv` **OR** add attendees manually

### Verify Configuration

1. Check **"⚙️ Settings"** → **"Processing Parameters"**
2. Adjust settings if needed:
   - Min/Max attendees
   - Amount-based estimation
   - Primary ID weights

## Important Notes

### Free Tier Limitations
- ⏸️ Apps sleep after inactivity (wake on visit)
- 💾 1 GB RAM limit
- 🌐 Public access (anyone with URL)
- 🔄 Temporary file storage (resets on restart)

### Data Persistence
- ✅ Attendee list persists (in git repository)
- ✅ Configuration persists (in git repository)
- ❌ Uploaded files are temporary
- ❌ Processed outputs are temporary

### Recommendations
- For **production use**, consider paid Streamlit Cloud tiers
- For **private deployment**, use self-hosting (see below)
- For **sensitive data**, use local deployment

## Self-Hosting Alternative

### Local Network Deployment

```bash
# Clone repository
git clone https://github.com/davidklan-png/Expense_Summary.git
cd Expense_Summary

# Install dependencies
pip install -r requirements.txt

# Run with network access
streamlit run web_app.py \
  --server.address 0.0.0.0 \
  --server.port 8502 \
  --server.headless true
```

Access from any device on your network:
- Local: `http://localhost:8502`
- Network: `http://YOUR_IP:8502`

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8502

CMD ["streamlit", "run", "web_app.py", \
     "--server.address", "0.0.0.0", \
     "--server.port", "8502", \
     "--server.headless", "true"]
```

Build and run:
```bash
docker build -t saison-transform .
docker run -p 8502:8502 saison-transform
```

## Troubleshooting

### App Won't Start
- Check that all files in `requirements.txt` are valid
- Verify `web_app.py` exists in repository root
- Check Streamlit Cloud logs for errors

### Import Errors
- Ensure `src/saisonxform/` directory structure is correct
- Verify all Python modules have `__init__.py`

### Data Not Persisting
- Remember: Streamlit Cloud is stateless
- Use git-tracked files (`data/reference/`) for persistence
- Upload files are temporary by design

### Performance Issues
- Free tier has resource limits
- Consider upgrading to paid tier for better performance
- Optimize large file processing

## Support

- **Documentation:** [README.md](README.md)
- **Web Interface Guide:** [docs/guides/WEB_INTERFACE_GUIDE.md](docs/guides/WEB_INTERFACE_GUIDE.md)
- **Issues:** [GitHub Issues](https://github.com/davidklan-png/Expense_Summary/issues)

## Security Notes

- 🔒 `.streamlit/secrets.toml` is gitignored
- 🔐 No secrets are required for basic deployment
- 🌐 Free tier apps are publicly accessible
- 🔑 Add authentication if handling sensitive data

---

**Last Updated:** 2025-11-29
**Version:** 0.2.3
**Streamlit Version:** 1.51.0+
