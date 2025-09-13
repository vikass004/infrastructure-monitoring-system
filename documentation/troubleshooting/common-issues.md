# Troubleshooting Guide

## 🔧 Common Issues & Solutions

### **Quick Diagnostics Checklist**
Before diving into specific issues, run these quick checks:

```bash
# 1. Check Docker status
docker --version
docker-compose --version

# 2. Check container status
docker-compose ps

# 3. Check system resources
docker stats --no-stream

# 4. Check logs for errors
docker-compose logs --tail=20
```

---

## 🚫 **Startup Issues**

### **Problem: Containers Won't Start**

#### **Symptoms:**
- `docker-compose up -d` fails
- Containers exit immediately
- Port binding errors

#### **Solution Steps:**

1. **Check Port Conflicts**
   ```bash
   # Windows
   netstat -an | findstr "3000\|9090\|9093\|9100\|8080\|9115"
   
   # If ports are in use, find the process
   netstat -ano | findstr :3000
   tasklist /FI "PID eq [PID_NUMBER]"
   ```

2. **Free Up Ports**
   ```bash
   # Stop conflicting services or change ports in docker-compose.yml
   # Kill specific process (if safe to do so)
   taskkill /PID [PID_NUMBER] /F
   ```

3. **Check Docker Resources**
   ```bash
   # Ensure Docker has enough memory (4GB recommended)
   # Check Docker Desktop settings
   ```

4. **Reset Docker State**
   ```bash
   docker-compose down
   docker system prune -f
   docker-compose up -d
   ```

### **Problem: "Version is obsolete" Warning**

#### **Symptoms:**
```
Warning: the attribute `version` is obsolete
```

#### **Solution:**
✅ **Already Fixed** - This warning is harmless and has been resolved in our configuration.

---

## 🔌 **Connectivity Issues**

### **Problem: Web Interfaces Not Loading**

#### **Symptoms:**
- Browser shows "This site can't be reached"
- Connection timeout errors
- Blank pages

#### **Solution Steps:**

1. **Verify Container Status**
   ```bash
   docker-compose ps
   # All services should show "Up"
   ```

2. **Check Specific Service**
   ```bash
   # Test individual services
   curl http://localhost:9090/api/v1/status/config  # Prometheus
   curl http://localhost:3000/api/health           # Grafana
   curl http://localhost:9093/api/v1/status        # Alertmanager
   ```

3. **Check Windows Firewall**
   ```bash
   # Temporarily disable Windows Firewall to test
   # Or add Docker Desktop to firewall exceptions
   ```

4. **Docker Desktop Network Issues**
   ```bash
   # Restart Docker Desktop
   # Check if running in WSL2 mode (recommended)
   ```

### **Problem: Grafana Login Issues**

#### **Symptoms:**
- Cannot login with admin/admin123
- Login page not loading
- Authentication errors

#### **Solution Steps:**

1. **Verify Grafana is Running**
   ```bash
   docker-compose logs grafana
   # Look for "HTTP Server Listen" message
   ```

2. **Reset Grafana Password**
   ```bash
   # Stop containers
   docker-compose down
   
   # Remove Grafana data volume (WARNING: Will lose dashboards)
   docker volume rm project1_grafana_data
   
   # Restart
   docker-compose up -d
   ```

3. **Check Environment Variables**
   ```yaml
   # In docker-compose.yml, verify:
   - GF_SECURITY_ADMIN_PASSWORD=admin123
   ```

---

## 📊 **Monitoring Issues**

### **Problem: No Metrics Showing in Prometheus**

#### **Symptoms:**
- Prometheus UI loads but shows no targets
- "No data" in query results
- Targets page shows all targets as "Down"

#### **Solution Steps:**

1. **Check Prometheus Configuration**
   ```bash
   # Validate configuration syntax
   docker exec prometheus promtool check config /etc/prometheus/prometheus.yml
   ```

2. **Check Target Connectivity**
   ```bash
   # Test if Prometheus can reach targets
   docker exec prometheus wget -qO- http://node_exporter:9100/metrics
   docker exec prometheus wget -qO- http://cadvisor:8080/metrics
   ```

3. **Review Prometheus Logs**
   ```bash
   docker-compose logs prometheus
   # Look for scraping errors or configuration issues
   ```

4. **Reload Configuration**
   ```bash
   # Reload Prometheus configuration
   curl -X POST http://localhost:9090/-/reload
   ```

### **Problem: Grafana Shows "No Data Sources"**

#### **Symptoms:**
- Grafana loads but dashboards show "No Data Source"
- Data source configuration missing
- Cannot query Prometheus from Grafana

#### **Solution Steps:**

1. **Check Data Source Auto-Provisioning**
   ```bash
   docker-compose logs grafana
   # Look for data source provisioning messages
   ```

2. **Manual Data Source Configuration**
   - Login to Grafana (http://localhost:3000)
   - Go to Configuration → Data Sources
   - Add Prometheus data source
   - URL: `http://prometheus:9090`
   - Save & Test

3. **Verify Network Connectivity**
   ```bash
   # Test Grafana to Prometheus connection
   docker exec grafana wget -qO- http://prometheus:9090/api/v1/status/config
   ```

---

## 🐍 **Python Monitor Issues**

### **Problem: Python Monitor Keeps Restarting**

#### **Symptoms:**
- Python monitor container shows "Restarting"
- No health metrics being generated
- Container logs show errors

#### **Solution Steps:**

1. **Check Container Logs**
   ```bash
   docker-compose logs python_monitor
   # Look for Python errors or missing dependencies
   ```

2. **Test Script Locally**
   ```bash
   # Run health check script directly
   cd automation
   python health-checks/system_monitor.py
   ```

3. **Check Volume Mounting**
   ```bash
   # Verify log directory exists and is writable
   docker exec python_monitor ls -la /app/logs
   ```

4. **Rebuild Container**
   ```bash
   docker-compose down
   docker-compose build python_monitor
   docker-compose up -d
   ```

### **Problem: Health Check Script Errors**

#### **Common Error: ModuleNotFoundError**
```python
ModuleNotFoundError: No module named 'psutil'
```

**Solution:**
```bash
# Check if requirements are installed
pip install -r automation/requirements.txt

# Or rebuild Docker container
docker-compose build python_monitor
```

#### **Common Error: Permission Denied**
```
PermissionError: [Errno 13] Permission denied: '/app/logs/health_monitor.log'
```

**Solution:**
```bash
# Fix container permissions
docker exec python_monitor chmod 777 /app/logs
```

---

## 🚨 **Alert Issues**

### **Problem: Alerts Not Firing**

#### **Symptoms:**
- Expected alerts not triggering
- Alertmanager shows no alerts
- No notifications received

#### **Solution Steps:**

1. **Check Alert Rules Syntax**
   ```bash
   # Validate alert rules
   docker exec prometheus promtool check rules /etc/prometheus/alert_rules.yml
   ```

2. **Verify Rule Evaluation**
   - Go to Prometheus UI → Alerts
   - Check if rules are loaded and evaluating
   - Look for any evaluation errors

3. **Test Alert Conditions**
   ```bash
   # Manually trigger high CPU to test alerts
   # Or adjust alert thresholds temporarily
   ```

4. **Check Alertmanager Configuration**
   ```bash
   # Validate Alertmanager config
   docker exec alertmanager amtool config check /etc/alertmanager/alertmanager.yml
   ```

### **Problem: Alertmanager Configuration Errors**

#### **Common Error: YAML Syntax**
```
yaml: unmarshal errors: line X: field Y not found
```

**Solution:**
✅ **Already Fixed** - Alertmanager configuration has been corrected to use proper YAML syntax.

---

## 💾 **Data & Storage Issues**

### **Problem: Metrics Data Loss**

#### **Symptoms:**
- Historical data missing
- Dashboards show gaps in data
- Storage volume issues

#### **Solution Steps:**

1. **Check Volume Status**
   ```bash
   docker volume ls
   docker volume inspect project1_prometheus_data
   ```

2. **Check Disk Space**
   ```bash
   # Check host disk space
   df -h
   
   # Check Docker space usage
   docker system df
   ```

3. **Backup Important Data**
   ```bash
   # Backup Prometheus data
   docker run --rm -v project1_prometheus_data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus-backup.tar.gz /data
   ```

### **Problem: Log File Growth**

#### **Symptoms:**
- Large log files consuming disk space
- Container performance issues
- Out of disk space errors

#### **Solution Steps:**

1. **Check Log Sizes**
   ```bash
   du -sh automation/logs/*
   du -sh logs/*
   ```

2. **Implement Log Rotation**
   ```bash
   # Archive old logs
   find automation/logs -name "*.log" -mtime +7 -exec gzip {} \;
   
   # Remove old compressed logs
   find automation/logs -name "*.gz" -mtime +30 -delete
   ```

3. **Configure Log Limits**
   ```yaml
   # In docker-compose.yml, add logging configuration
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

---

## 🔧 **Performance Issues**

### **Problem: Slow Dashboard Loading**

#### **Symptoms:**
- Grafana dashboards take >10 seconds to load
- Query timeouts
- Browser becomes unresponsive

#### **Solution Steps:**

1. **Optimize Query Time Ranges**
   - Use shorter time ranges for dashboards
   - Adjust refresh intervals (5m instead of 30s)
   - Optimize PromQL queries

2. **Check System Resources**
   ```bash
   docker stats
   # Verify containers aren't CPU/memory constrained
   ```

3. **Tune Prometheus Configuration**
   ```yaml
   # Adjust query timeout in prometheus.yml
   global:
     evaluation_interval: 30s  # Increase if needed
   ```

### **Problem: High Memory Usage**

#### **Symptoms:**
- Containers consuming excessive memory
- System becomes slow
- Out of memory errors

#### **Solution Steps:**

1. **Add Memory Limits**
   ```yaml
   # In docker-compose.yml
   services:
     prometheus:
       deploy:
         resources:
           limits:
             memory: 1G
   ```

2. **Tune Prometheus Retention**
   ```yaml
   # Reduce data retention period
   command:
     - '--storage.tsdb.retention.time=15d'
   ```

---

## 🆘 **Emergency Recovery**

### **Complete System Reset**

If all else fails, here's how to completely reset the system:

```bash
# 1. Stop everything
docker-compose down

# 2. Remove all data (WARNING: Will lose all data!)
docker volume prune -f
docker system prune -a -f

# 3. Rebuild from scratch
docker-compose build
docker-compose up -d

# 4. Wait for services to start (2-3 minutes)
docker-compose ps

# 5. Verify functionality
curl http://localhost:9090
curl http://localhost:3000
curl http://localhost:9093
```

### **Backup and Restore Procedures**

#### **Creating Backup:**
```bash
# Backup all persistent data
docker run --rm -v project1_prometheus_data:/prometheus -v project1_grafana_data:/grafana -v $(pwd):/backup alpine tar czf /backup/monitoring-backup-$(date +%Y%m%d).tar.gz /prometheus /grafana
```

#### **Restoring from Backup:**
```bash
# Stop services
docker-compose down

# Restore data
docker run --rm -v project1_prometheus_data:/prometheus -v project1_grafana_data:/grafana -v $(pwd):/backup alpine tar xzf /backup/monitoring-backup-YYYYMMDD.tar.gz

# Restart services
docker-compose up -d
```

---

## 📞 **Getting Additional Help**

### **Useful Commands for Support**

When asking for help, provide these diagnostic outputs:

```bash
# System information
docker --version
docker-compose --version
docker info

# Service status
docker-compose ps
docker-compose logs --tail=50

# Resource usage
docker stats --no-stream
df -h

# Network connectivity
curl -I http://localhost:9090
curl -I http://localhost:3000
curl -I http://localhost:9093
```

### **Log Files to Check**
- `automation/logs/health_monitor.log` - Python script logs
- `logs/daily/` - Development and testing logs
- Container logs via `docker-compose logs <service>`

---

*Troubleshooting Guide Version: 1.0*  
*Last Updated: September 12, 2025*  
*For additional support, check the project documentation or contact the development team.*
