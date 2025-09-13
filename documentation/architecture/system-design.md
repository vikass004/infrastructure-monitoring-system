# System Architecture Overview

## 🏗️ Infrastructure Monitoring & Alerting System

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Monitoring System             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Prometheus  │────│   Grafana   │────│ Alertmanager│         │
│  │   :9090     │    │    :3000    │    │    :9093    │         │
│  │             │    │             │    │             │         │
│  │ • Metrics   │    │ • Dashboards│    │ • Routing   │         │
│  │ • Storage   │    │ • Visualization│ │ • Notifications│      │
│  │ • Queries   │    │ • User Auth │    │ • Escalation│         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                   │                   │              │
│         │                   │                   │              │
│         ▼                   ▼                   ▼              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Data Collection Layer                    │   │
│  │                                                         │   │
│  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │   │
│  │ │Node Exporter│ │  cAdvisor   │ │   Blackbox  │        │   │
│  │ │    :9100    │ │    :8080    │ │   :9115     │        │   │
│  │ │             │ │             │ │             │        │   │
│  │ │• System     │ │• Container  │ │• Network    │        │   │
│  │ │  Metrics    │ │  Metrics    │ │  Probes     │        │   │
│  │ └─────────────┘ └─────────────┘ └─────────────┘        │   │
│  │                                                         │   │
│  │ ┌─────────────────────────────────────────────────────┐ │   │
│  │ │            Python Health Monitor                   │ │   │
│  │ │                                                     │ │   │
│  │ │ • Custom Health Checks    • JSON Metrics Export    │ │   │
│  │ │ • System Analysis         • Intelligent Scoring    │ │   │
│  │ │ • Performance Monitoring  • Automated Reporting    │ │   │
│  │ └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Component Responsibilities**

### **Core Monitoring Stack**

#### **Prometheus (Metrics Engine)**
- **Purpose**: Central metrics collection and storage
- **Port**: 9090
- **Key Features**:
  - Time-series database
  - Pull-based metrics collection
  - PromQL query language
  - Built-in alerting rules
  - Service discovery

#### **Grafana (Visualization)**
- **Purpose**: Dashboard and visualization platform
- **Port**: 3000
- **Key Features**:
  - Rich dashboard creation
  - Real-time data visualization
  - User authentication
  - Panel customization
  - Dashboard provisioning

#### **Alertmanager (Alert Management)**
- **Purpose**: Alert routing and notification handling
- **Port**: 9093
- **Key Features**:
  - Alert deduplication
  - Notification routing
  - Escalation policies
  - Silence management
  - Multiple notification channels

### **Data Collection Layer**

#### **Node Exporter (System Metrics)**
- **Purpose**: Host system metrics collection
- **Port**: 9100
- **Metrics Collected**:
  - CPU usage and load
  - Memory and swap utilization
  - Disk space and I/O
  - Network interface statistics
  - System processes

#### **cAdvisor (Container Metrics)**
- **Purpose**: Container performance monitoring
- **Port**: 8080
- **Metrics Collected**:
  - Container resource usage
  - Memory and CPU per container
  - Network and storage metrics
  - Container lifecycle events

#### **Blackbox Exporter (Network Probes)**
- **Purpose**: External endpoint monitoring
- **Port**: 9115
- **Capabilities**:
  - HTTP/HTTPS health checks
  - TCP connectivity tests
  - DNS resolution monitoring
  - SSL certificate validation

#### **Python Health Monitor (Custom Automation)**
- **Purpose**: Advanced system analysis and custom metrics
- **Key Features**:
  - Comprehensive health scoring
  - Multi-dimensional analysis
  - JSON metrics export
  - Intelligent alerting
  - Custom business logic

---

## 🌐 **Network Architecture**

### **Docker Network: `project1_monitoring`**
```
┌────────────────────────────────────────────────────────┐
│                Docker Bridge Network                   │
│                                                        │
│  prometheus:9090 ←→ grafana:3000 ←→ alertmanager:9093  │
│           ↕                ↕              ↕           │
│  node_exporter:9100    cadvisor:8080   blackbox:9115  │
│           ↕                ↕              ↕           │
│               python_monitor (batch)                   │
│                                                        │
│  Host Network Mapping:                                 │
│  • localhost:9090 → prometheus:9090                   │
│  • localhost:3000 → grafana:3000                      │
│  • localhost:9093 → alertmanager:9093                 │
│  • localhost:9100 → node_exporter:9100                │
│  • localhost:8080 → cadvisor:8080                     │
│  • localhost:9115 → blackbox_exporter:9115            │
└────────────────────────────────────────────────────────┘
```

---

## 📊 **Data Flow Architecture**

### **Metrics Collection Flow**
```
1. System/Container Metrics → Exporters
2. Exporters → Prometheus (scraping)
3. Prometheus → Grafana (queries)
4. Prometheus → Alertmanager (alerts)
5. Python Monitor → Log Files (analysis)
```

### **Alert Processing Flow**
```
1. Prometheus (rule evaluation) → Alert triggered
2. Alert → Alertmanager (routing)
3. Alertmanager → Notification channels
4. Notification → Operations team
5. Acknowledgment → Alert resolution
```

---

## 🔄 **Configuration Management**

### **Configuration Files Structure**
```
config/
├── prometheus/
│   ├── prometheus.yml      # Main Prometheus configuration
│   └── alert_rules.yml     # Alerting rules definition
├── grafana/
│   ├── provisioning/
│   │   ├── datasources.yml # Auto data source configuration
│   │   └── dashboards.yml  # Dashboard provisioning
│   └── dashboards/         # Dashboard JSON files
├── alertmanager/
│   └── alertmanager.yml    # Alert routing configuration
└── docker/
    └── docker-compose.yml  # Container orchestration
```

---

## 🛡️ **Security Architecture**

### **Access Control**
- **Grafana**: Username/password authentication
- **Prometheus**: Network-level access control
- **Alertmanager**: Configuration-based access
- **Docker Network**: Isolated container communication

### **Data Protection**
- **Metrics Storage**: Local volume persistence
- **Configuration**: Version controlled
- **Logs**: Centralized logging with rotation
- **Secrets**: Environment variable management

---

## 📈 **Scalability Design**

### **Horizontal Scaling Options**
1. **Multi-Prometheus Setup**: Federation for large environments
2. **Grafana Clustering**: Multiple Grafana instances
3. **Alert Distribution**: Multiple Alertmanager instances
4. **Data Retention**: Configurable storage policies

### **Performance Considerations**
- **Prometheus**: Efficient time-series storage
- **Grafana**: Dashboard caching and optimization
- **Exporters**: Lightweight metric collection
- **Python Scripts**: Optimized execution patterns

---

## 🔌 **Integration Points**

### **External System Integration**
- **Cloud Platforms**: AWS, Azure, GCP exporters
- **Databases**: MySQL, PostgreSQL, MongoDB exporters
- **Applications**: Custom metric endpoints
- **Notification Systems**: Email, Slack, PagerDuty

### **API Interfaces**
- **Prometheus API**: Query and configuration endpoints
- **Grafana API**: Dashboard and user management
- **Alertmanager API**: Alert management and configuration

---

## 📝 **Maintenance Architecture**

### **Backup Strategy**
- **Configuration Files**: Git version control
- **Metrics Data**: Volume backup procedures
- **Dashboard Definitions**: Export/import procedures
- **Alert Configurations**: Documentation and versioning

### **Monitoring the Monitoring**
- **Self-monitoring**: Prometheus monitors itself
- **Health Checks**: Python automation validates stack
- **Performance Metrics**: Resource usage tracking
- **Alert Testing**: Regular alert validation

---

*Architecture documented on September 12, 2025*  
*Version: 1.0*  
*Next Review: Weekly*
