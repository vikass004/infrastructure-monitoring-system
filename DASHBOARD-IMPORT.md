# Dashboard Import Instructions

## Manual Dashboard Import (Recommended)

Since the automated API import requires additional authentication setup, follow these steps to import the beautiful dashboards:

### Step 1: Access Grafana
1. Open your browser to `http://localhost:3000`
2. Login with username: `admin`, password: `admin`
3. Skip password change prompt (or change if desired)

### Step 2: Import Infrastructure Overview Dashboard
1. Click the "+" icon in the left sidebar
2. Select "Import"
3. Click "Upload JSON file"
4. Navigate to `monitoring/grafana/dashboards/infrastructure-overview.json`
5. Click "Load"
6. Click "Import"

### Step 3: Import Container Performance Dashboard
1. Repeat the import process with `container-performance.json`

### Step 4: Import Monitoring Stack Health Dashboard
1. Repeat the import process with `monitoring-stack-health.json`

## Expected Results
After importing, you should see:
- **Infrastructure Overview**: CPU, Memory, Disk, Network metrics
- **Container Performance**: Docker container resource usage
- **Monitoring Stack Health**: Prometheus, Grafana, and exporter status

## Troubleshooting
- If dashboards show "No data", wait 1-2 minutes for metrics to populate
- Ensure all Docker containers are running: `docker-compose ps`
- Check Prometheus targets at `http://localhost:9090/targets`

## Dashboard Features
- Real-time metrics with 30-second refresh
- Historical data with configurable time ranges
- Beautiful visualizations with color-coded thresholds
- Professional layout suitable for NOC displays

---
*These dashboards provide enterprise-grade monitoring visualization perfect for demonstrating infrastructure monitoring capabilities.*
