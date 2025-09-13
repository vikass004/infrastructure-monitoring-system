# 🚀 Quick Start Guide

## Infrastructure Monitoring & Alerting System

### **⚡ 5-Minute Setup**

#### **Prerequisites**
- Docker Desktop installed and running
- Git (for cloning)
- 4GB RAM available
- Ports 3000, 9090, 9093 available

#### **🔧 Installation Steps**

1. **Clone or Download Project**
   ```bash
   # If using git
   git clone <your-repo-url>
   cd infrastructure-monitoring-system
   
   # Or download and extract ZIP file
   ```

2. **Start the Complete Stack**
   ```bash
   docker-compose up -d
   ```
   
3. **Verify All Services**
   ```bash
   docker-compose ps
   ```
   
   All services should show "Up" status.

4. **Access Web Interfaces**
   - **Prometheus**: http://localhost:9090
   - **Grafana**: http://localhost:3000 (admin/admin123)
   - **Alertmanager**: http://localhost:9093

#### **🎯 First Steps After Setup**

1. **Check Prometheus Targets**
   - Go to http://localhost:9090/targets
   - Verify all targets are "UP"

2. **Login to Grafana**
   - Navigate to http://localhost:3000
   - Login: admin / admin123
   - Data source should auto-configure

3. **Verify Health Monitoring**
   - Python health checks run automatically
   - Check logs: `docker-compose logs python_monitor`

#### **🛑 Quick Troubleshooting**

**If containers won't start:**
```bash
# Check Docker is running
docker --version

# Check port conflicts
netstat -an | findstr "3000\|9090\|9093"

# Restart with fresh state
docker-compose down
docker-compose up -d
```

**If web interfaces don't load:**
- Wait 30 seconds for full startup
- Check Windows Firewall/antivirus
- Verify Docker Desktop is running

#### **📊 What You'll See**

- **Prometheus**: Raw metrics and query interface
- **Grafana**: Beautiful dashboards (login required)
- **Alertmanager**: Alert management interface
- **Python Monitor**: Automatic health checks every restart

#### **🔧 Management Commands**

```bash
# View all logs
docker-compose logs

# Stop everything
docker-compose down

# Update and restart
docker-compose down && docker-compose up -d

# View specific service
docker-compose logs grafana
```

#### **💡 Next Steps**

1. Import pre-built dashboards in Grafana
2. Configure alert notifications
3. Add custom monitoring targets
4. Review runbooks for operations

---

**Need help?** Check the troubleshooting guide: `documentation/troubleshooting/common-issues.md`
