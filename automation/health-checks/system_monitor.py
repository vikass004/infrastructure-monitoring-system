#!/usr/bin/env python3
"""
System Health Monitor
Performs comprehensive system health checks and reports metrics to Prometheus.

This script demonstrates:
- System resource monitoring
- Custom metrics collection
- Error handling and logging
- Integration with monitoring stack
"""

import psutil
import time
import logging
import json
import requests
from datetime import datetime
from typing import Dict, List, Any
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/health_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SystemHealthMonitor:
    """
    Comprehensive system health monitoring class.
    
    Collects system metrics and provides health assessment.
    """
    
    def __init__(self):
        self.prometheus_url = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
        self.metrics_cache = {}
        logger.info("SystemHealthMonitor initialized")
    
    def get_cpu_metrics(self) -> Dict[str, float]:
        """
        Collect CPU usage metrics.
        
        Returns:
            Dict containing CPU usage percentages
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            load_avg = [0, 0, 0]  # Windows doesn't have load average
            try:
                load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            except (OSError, AttributeError):
                pass
            
            metrics = {
                'cpu_usage_total': cpu_percent,
                'cpu_cores_count': psutil.cpu_count(),
                'load_average_1m': load_avg[0],
                'load_average_5m': load_avg[1],
                'load_average_15m': load_avg[2]
            }
            
            # Add per-core metrics
            for i, core_usage in enumerate(cpu_per_core):
                metrics[f'cpu_core_{i}_usage'] = core_usage
            
            logger.debug(f"CPU metrics collected: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting CPU metrics: {e}")
            return {}
    
    def get_memory_metrics(self) -> Dict[str, float]:
        """
        Collect memory usage metrics.
        
        Returns:
            Dict containing memory usage statistics
        """
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            metrics = {
                'memory_total_bytes': memory.total,
                'memory_available_bytes': memory.available,
                'memory_used_bytes': memory.used,
                'memory_usage_percent': memory.percent,
                'memory_cached_bytes': getattr(memory, 'cached', 0),
                'memory_buffers_bytes': getattr(memory, 'buffers', 0),
                'swap_total_bytes': swap.total,
                'swap_used_bytes': swap.used,
                'swap_usage_percent': swap.percent
            }
            
            logger.debug(f"Memory metrics collected: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting memory metrics: {e}")
            return {}
    
    def get_disk_metrics(self) -> Dict[str, Any]:
        """
        Collect disk usage metrics for all mounted filesystems.
        
        Returns:
            Dict containing disk usage statistics
        """
        try:
            disk_metrics = {}
            
            # Get disk usage for all mounted partitions
            partitions = psutil.disk_partitions()
            for partition in partitions:
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    
                    # Clean mountpoint name for metric naming
                    mount_clean = partition.mountpoint.replace('/', '_root_').replace('\\', '_').replace(':', '_drive')
                    if mount_clean.startswith('_'):
                        mount_clean = mount_clean[1:]
                    if not mount_clean:
                        mount_clean = 'root'
                    
                    disk_metrics.update({
                        f'disk_{mount_clean}_total_bytes': partition_usage.total,
                        f'disk_{mount_clean}_used_bytes': partition_usage.used,
                        f'disk_{mount_clean}_free_bytes': partition_usage.free,
                        f'disk_{mount_clean}_usage_percent': (partition_usage.used / partition_usage.total) * 100
                    })
                    
                except PermissionError:
                    # Skip partitions we can't access
                    continue
            
            # Get disk I/O statistics
            disk_io = psutil.disk_io_counters()
            if disk_io:
                disk_metrics.update({
                    'disk_read_bytes_total': disk_io.read_bytes,
                    'disk_write_bytes_total': disk_io.write_bytes,
                    'disk_read_count_total': disk_io.read_count,
                    'disk_write_count_total': disk_io.write_count
                })
            
            logger.debug(f"Disk metrics collected: {len(disk_metrics)} metrics")
            return disk_metrics
            
        except Exception as e:
            logger.error(f"Error collecting disk metrics: {e}")
            return {}
    
    def get_network_metrics(self) -> Dict[str, float]:
        """
        Collect network interface metrics.
        
        Returns:
            Dict containing network statistics
        """
        try:
            network_metrics = {}
            
            # Get network I/O statistics
            net_io = psutil.net_io_counters(pernic=True)
            for interface, stats in net_io.items():
                # Clean interface name for metric naming
                interface_clean = interface.replace(' ', '_').replace('-', '_')
                
                network_metrics.update({
                    f'network_{interface_clean}_bytes_sent': stats.bytes_sent,
                    f'network_{interface_clean}_bytes_recv': stats.bytes_recv,
                    f'network_{interface_clean}_packets_sent': stats.packets_sent,
                    f'network_{interface_clean}_packets_recv': stats.packets_recv,
                    f'network_{interface_clean}_errors_in': stats.errin,
                    f'network_{interface_clean}_errors_out': stats.errout,
                    f'network_{interface_clean}_drops_in': stats.dropin,
                    f'network_{interface_clean}_drops_out': stats.dropout
                })
            
            # Get network connections count
            connections = len(psutil.net_connections())
            network_metrics['network_connections_total'] = connections
            
            logger.debug(f"Network metrics collected: {len(network_metrics)} metrics")
            return network_metrics
            
        except Exception as e:
            logger.error(f"Error collecting network metrics: {e}")
            return {}
    
    def get_process_metrics(self) -> Dict[str, int]:
        """
        Collect process-related metrics.
        
        Returns:
            Dict containing process statistics
        """
        try:
            processes = list(psutil.process_iter(['pid', 'name', 'status']))
            
            # Count processes by status
            status_counts = {}
            for proc in processes:
                try:
                    status = proc.info['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            metrics = {
                'processes_total': len(processes),
                'processes_running': status_counts.get(psutil.STATUS_RUNNING, 0),
                'processes_sleeping': status_counts.get(psutil.STATUS_SLEEPING, 0),
                'processes_zombie': status_counts.get(psutil.STATUS_ZOMBIE, 0)
            }
            
            logger.debug(f"Process metrics collected: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting process metrics: {e}")
            return {}
    
    def perform_health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive system health check.
        
        Returns:
            Dict containing all collected metrics and health status
        """
        logger.info("Starting comprehensive health check")
        start_time = time.time()
        
        all_metrics = {}
        
        # Collect all metric types
        metrics_collectors = [
            ('cpu', self.get_cpu_metrics),
            ('memory', self.get_memory_metrics),
            ('disk', self.get_disk_metrics),
            ('network', self.get_network_metrics),
            ('process', self.get_process_metrics)
        ]
        
        for metric_type, collector in metrics_collectors:
            try:
                metrics = collector()
                all_metrics.update(metrics)
                logger.info(f"Collected {len(metrics)} {metric_type} metrics")
            except Exception as e:
                logger.error(f"Failed to collect {metric_type} metrics: {e}")
        
        # Calculate health scores
        health_status = self.calculate_health_status(all_metrics)
        all_metrics.update(health_status)
        
        # Add metadata
        all_metrics.update({
            'health_check_timestamp': datetime.now().isoformat(),
            'health_check_duration_seconds': time.time() - start_time,
            'health_check_metrics_count': len(all_metrics)
        })
        
        logger.info(f"Health check completed in {time.time() - start_time:.2f} seconds")
        logger.info(f"Collected {len(all_metrics)} total metrics")
        
        return all_metrics
    
    def calculate_health_status(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate overall system health scores based on collected metrics.
        
        Args:
            metrics: Dictionary of collected system metrics
            
        Returns:
            Dict containing health scores (0-100)
        """
        health_scores = {}
        
        try:
            # CPU Health Score (0-100, lower is better)
            cpu_usage = metrics.get('cpu_usage_total', 0)
            if cpu_usage <= 50:
                cpu_health = 100
            elif cpu_usage <= 80:
                cpu_health = 100 - (cpu_usage - 50) * 2
            else:
                cpu_health = max(0, 40 - (cpu_usage - 80) * 2)
            health_scores['health_cpu_score'] = cpu_health
            
            # Memory Health Score
            memory_usage = metrics.get('memory_usage_percent', 0)
            if memory_usage <= 60:
                memory_health = 100
            elif memory_usage <= 85:
                memory_health = 100 - (memory_usage - 60) * 2
            else:
                memory_health = max(0, 50 - (memory_usage - 85) * 3)
            health_scores['health_memory_score'] = memory_health
            
            # Disk Health Score (average across all disks)
            disk_scores = []
            for key, value in metrics.items():
                if 'disk_' in key and 'usage_percent' in key:
                    disk_usage = value
                    if disk_usage <= 70:
                        disk_score = 100
                    elif disk_usage <= 90:
                        disk_score = 100 - (disk_usage - 70) * 2.5
                    else:
                        disk_score = max(0, 50 - (disk_usage - 90) * 5)
                    disk_scores.append(disk_score)
            
            health_scores['health_disk_score'] = sum(disk_scores) / len(disk_scores) if disk_scores else 100
            
            # Overall Health Score
            individual_scores = [health_scores[key] for key in health_scores]
            health_scores['health_overall_score'] = sum(individual_scores) / len(individual_scores)
            
            # Health Status Classification
            overall_score = health_scores['health_overall_score']
            if overall_score >= 80:
                health_scores['health_status_code'] = 1  # Healthy
            elif overall_score >= 60:
                health_scores['health_status_code'] = 2  # Warning
            else:
                health_scores['health_status_code'] = 3  # Critical
            
        except Exception as e:
            logger.error(f"Error calculating health status: {e}")
            health_scores['health_overall_score'] = 0
            health_scores['health_status_code'] = 3
        
        return health_scores
    
    def save_metrics_to_file(self, metrics: Dict[str, Any], filename: str = None):
        """
        Save metrics to JSON file for debugging and historical analysis.
        
        Args:
            metrics: Dictionary of metrics to save
            filename: Optional custom filename
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/app/logs/health_metrics_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(metrics, f, indent=2, default=str)
            logger.info(f"Metrics saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving metrics to file: {e}")

def main():
    """
    Main execution function for the health monitor.
    """
    logger.info("Starting System Health Monitor")
    
    # Initialize monitor
    monitor = SystemHealthMonitor()
    
    try:
        # Perform health check
        metrics = monitor.perform_health_check()
        
        # Save metrics to file
        monitor.save_metrics_to_file(metrics)
        
        # Print summary
        print(f"Health Check Summary:")
        print(f"Overall Health Score: {metrics.get('health_overall_score', 0):.1f}/100")
        print(f"CPU Usage: {metrics.get('cpu_usage_total', 0):.1f}%")
        print(f"Memory Usage: {metrics.get('memory_usage_percent', 0):.1f}%")
        print(f"Total Metrics Collected: {metrics.get('health_check_metrics_count', 0)}")
        
        # Determine exit code based on health
        health_code = metrics.get('health_status_code', 3)
        if health_code == 1:
            print("System Status: HEALTHY ✅")
            exit_code = 0
        elif health_code == 2:
            print("System Status: WARNING ⚠️")
            exit_code = 1
        else:
            print("System Status: CRITICAL ❌")
            exit_code = 2
        
        return exit_code
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        print("System Status: ERROR ❌")
        return 3

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
