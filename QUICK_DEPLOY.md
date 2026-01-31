# ⚡ Quick Deploy Guide

## For You (Server - 5 Minutes)

```bash
# 1. Find your IP
ipconfig
# Note your IPv4 Address (e.g., 192.168.1.100)

# 2. Start backends
# Terminal 1:
python main.py

# Terminal 2:
cd verification_backend
python run.py

# 3. Configure firewall (Run as Admin)
netsh advfirewall firewall add rule name="Main" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="Verification" dir=in action=allow protocol=TCP localport=8001

# 4. Create Git branch
git checkout -b vendor-receiver-system
git add verification_backend/ verification_webapp/ *.md
git commit -m "Vendor System"
git push origin vendor-receiver-system

# 5. Share with friend:
# - Repo URL: https://github.com/YOUR_USERNAME/YOUR_REPO
# - Branch: vendor-receiver-system
# - Your IP: 192.168.1.XXX
```

---

## For Your Friend (Client - 3 Minutes)

```bash
# 1. Clone
git clone -b vendor-receiver-system REPO_URL
cd REPO_NAME/verification_webapp

# 2. Install
npm install

# 3. Configure
echo "VITE_API_URL=http://SERVER_IP:8001/api/v1" > .env
echo "VITE_MAIN_API_URL=http://SERVER_IP:8000/api/v1" >> .env
# Replace SERVER_IP with the IP you received

# 4. Run
npm run dev

# 5. Open
# http://localhost:5174
```

---

## Test Connection

```bash
# From friend's laptop:
curl http://SERVER_IP:8000/health
curl http://SERVER_IP:8001/health

# Should return: {"status": "healthy"}
```

---

## Done! 🎉

- **Your laptop**: Runs backends + database
- **Friend's laptop**: Runs vendor frontend
- **Both**: Share same database via API

**That's it!**
