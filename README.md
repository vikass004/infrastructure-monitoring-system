# Infrastructure Monitoring & Alerting System

![Infrastructure Monitoring](https://img.shields.io/badge/Infrastructure-Monitoring-blue)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![Python](https://img.shields.io/badge/Python-Automation-green)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-orange)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-red)

## 🎯 Project Overview

A **production-ready infrastructure monitoring system** built with modern DevOps tools, featuring real-time metrics collection, automated health scoring, and professional dashboards. This project demonstrates enterprise-level systems engineering skills and monitoring best practices.

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Grafana   │    │ Prometheus  │    │ Python      │
│ Dashboards │◄───┤  Metrics    │◄───┤ Health      │
│   :3000     │    │   :9090     │    │ Monitor     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       │            ┌─────────────┐           │
       │            │AlertManager │           │
       │            │   :9093     │           │
       │            └─────────────┘           │
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
      ┌─────────────┐           ┌─────────────┐
      │Node Exporter│           │  cAdvisor   │
      │   :9100     │           │   :8080     │
      └─────────────┘           └─────────────┘
```

## 🚀 Features

### **Real-time Monitoring**
- ✅ **Service Health Tracking** - Monitor 7+ services simultaneously
- ✅ **System Metrics** - CPU, Memory, Disk, Network monitoring
- ✅ **Container Performance** - Docker container resource tracking
- ✅ **Custom Health Scoring** - Intelligent 0-100 health algorithm

### **Professional Dashboards**
- ✅ **Grafana Visualizations** - Beautiful, real-time dashboards
- ✅ **Alert Management** - Automated notification system
- ✅ **Historical Data** - Time-series data storage and analysis
- ✅ **Multi-panel Views** - Comprehensive system overview

### **Python Automation**
- ✅ **387-line Health Monitor** - Custom Python automation system
- ✅ **JSON Metrics Export** - Structured data output
- ✅ **Intelligent Scoring** - Weighted health calculations
- ✅ **Automated Logging** - Continuous system tracking

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Metrics Collection** | Prometheus | Time-series database and metrics aggregation |
| **Visualization** | Grafana | Dashboard creation and data visualization |
| **Alerting** | AlertManager | Alert routing and notification management |
| **System Metrics** | Node Exporter | Host-level metrics collection |
| **Container Metrics** | cAdvisor | Docker container performance monitoring |
| **Network Monitoring** | Blackbox Exporter | Service availability and response time |
| **Custom Automation** | Python 3.9 | Health monitoring and intelligent scoring |
| **Orchestration** | Docker Compose | Multi-container application management |

## 🚀 Quick Start

### **Prerequisites**
- Docker & Docker Compose installed
- 8GB RAM recommended
- Ports 3000, 8080, 9090-9115 available

### **1. Clone Repository**
```bash
git clone https://github.com/YOUR_USERNAME/infrastructure-monitoring
cd infrastructure-monitoring
```

### **2. Start Monitoring Stack**
```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

### **3. Access Dashboards**
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus Metrics**: http://localhost:9090
- **AlertManager**: http://localhost:9093
- **Container Stats**: http://localhost:8080

### **4. View Health Monitoring**
```bash
# Check Python health monitor logs
docker-compose logs python_monitor

# View metrics files
ls monitoring/python/logs/
```

## 📊 Dashboard Screenshots

### Infrastructure Overview
![Dashboard Overview](screenshots/dashboard-overview.png)

### Service Health Monitor
![Service Status](screenshots/service-status.png)

### System Performance Metrics
![Performance Metrics](screenshots/performance-metrics.png)

## 🐍 Python Health Monitor

The custom Python automation system provides:

```python
# Sample health score output
{
  "timestamp": "2025-09-13T14:30:15Z",
  "health_overall_score": 100.0,
  "system_status": "HEALTHY ✅",
  "cpu_usage_total": 8.5,
  "memory_usage_percent": 45.2,
  "metrics_collected": 75
}
```

**Key Features:**
- **75+ Metric Collection** - Comprehensive system analysis
- **Intelligent Scoring** - Weighted health algorithm
- **Real-time Processing** - 30-second monitoring intervals
- **JSON Export** - Structured data for integration

## 📁 Project Structure

```
infrastructure-monitoring/
├── docker-compose.yml           # Container orchestration
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml       # Metrics collection config
│   ├── grafana/
│   │   ├── provisioning/        # Auto-provisioning config
│   │   └── dashboards/          # Pre-built dashboards
│   ├── alertmanager/
│   │   └── alertmanager.yml     # Alert routing config
│   ├── python/
│   │   ├── system_monitor.py    # Health monitoring script
│   │   └── logs/                # Health monitoring output
│   └── blackbox/
│       └── blackbox.yml         # Network monitoring config
├── docs/                        # Documentation
├── screenshots/                 # Dashboard screenshots
└── README.md                    # Project documentation
```

## 🔧 Configuration

### **Monitoring Intervals**
- **Prometheus Scraping**: 15 seconds
- **Python Health Checks**: 30 seconds
- **Dashboard Refresh**: 30 seconds
- **Alert Evaluation**: 15 seconds

### **Resource Requirements**
- **CPU**: 2+ cores recommended
- **Memory**: 4GB minimum, 8GB recommended
- **Disk**: 10GB for metrics storage
- **Network**: Internet access for container images

## 📈 Monitoring Capabilities

### **System Metrics**
- CPU usage and load averages
- Memory utilization and availability
- Disk usage across filesystems
- Network traffic and interface statistics

### **Container Metrics**
- Docker container resource consumption
- Container lifecycle and health status
- Image and volume usage statistics
- Network and storage performance

### **Service Monitoring**
- Service availability (up/down status)
- Response time measurements
- Error rate tracking
- Custom application metrics

## 🚨 Alerting

**Pre-configured alert rules for:**
- High CPU usage (>80%)
- Memory exhaustion (>90%)
- Disk space critical (<10% free)
- Service downtime
- Container failures

## 🛠️ Development

### **Adding Custom Metrics**
1. Modify [`monitoring/python/system_monitor.py`](monitoring/python/system_monitor.py )
2. Update Prometheus scraping configuration
3. Create new Grafana dashboard panels
4. Configure relevant alerts

### **Dashboard Customization**
1. Access Grafana at localhost:3000
2. Import additional dashboards from [`monitoring/grafana/dashboards/`](monitoring/grafana/dashboards/ )
3. Customize panels and visualizations
4. Export and save configurations

## 🎯 Use Cases

- **Infrastructure Monitoring** - Complete system observability
- **DevOps Operations** - Continuous monitoring and alerting
- **Performance Analysis** - Historical trend analysis
- **Capacity Planning** - Resource utilization forecasting
- **Incident Response** - Real-time problem detection

## 🏆 Portfolio Highlights

This project demonstrates:
- **Systems Engineering Excellence** - Complex multi-service architecture
- **DevOps Best Practices** - Infrastructure as Code, containerization
- **Python Development** - Advanced automation and data processing
- **Monitoring Expertise** - Production-ready observability solution
- **Professional Documentation** - Comprehensive technical writing


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**⭐ Star this repository if it helped you!**
