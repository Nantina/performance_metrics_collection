import psutil
import csv
import time
import argparse 
import os
import sys
from datetime import datetime

def collect_metrics():
    """System performance metrics collection"""
    cpu_freq = psutil.cpu_freq()
    cpu_stats = psutil.cpu_stats()
    cpu_times = psutil.cpu_times()
    net_io = psutil.net_io_counters()
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()

    metrics = {
        "timestamp": datetime.now().isoformat(),

        # Kernel info
        "sys_platform": sys.platform,
        "os_name": os.name,
        # "kernel_version": os.uname().release,
        # "system_name": os.uname().sysname,
        # "node_name": os.uname().nodename,
        # "machine": os.uname().machine,

        # CPU 
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count_logical": psutil.cpu_count(),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_freq_current": cpu_freq.current if cpu_freq else None,
        "cpu_freq_min": cpu_freq.min if cpu_freq else None,
        "cpu_freq_max": cpu_freq.max if cpu_freq else None,
        "cpu_stats_ctx_switches": cpu_stats.ctx_switches,
        "cpu_stats_interrupts": cpu_stats.interrupts,
        "cpu_stats_soft_interrupts": cpu_stats.soft_interrupts,
        "cpu_stats_syscalls": cpu_stats.syscalls,
        "cpu_times_user": cpu_times.user,
        "cpu_times_system": cpu_times.system,
        "cpu_times_idle": cpu_times.idle,
        # "cpu_times_nice": cpu_times.nice,
        # "cpu_times_iowait": cpu_times.iowait,
        # "cpu_times_irq": cpu_times.irq,
        # "cpu_times_softirq": cpu_times.softirq,
        # "cpu_times_steal": cpu_times.steal,
        # "cpu_times_guest": cpu_times.guest,
        # "cpu_times_guest_nice": cpu_times.guest_nice,

        # Memory 
        "virtual_memory_total": psutil.virtual_memory().total,
        "virtual_memory_available": psutil.virtual_memory().available,
        "virtual_memory_used": psutil.virtual_memory().used,
        "virtual_memory_percent": psutil.virtual_memory().percent,
        "virtual_memory_free": psutil.virtual_memory().free,
        # "virtual_memory_active": psutil.virtual_memory().active,
        # "virtual_memory_buffers": psutil.virtual_memory().buffers,
        # "virtual_memory_cached": psutil.virtual_memory().cached,
        # "virtual_memory_shared": psutil.virtual_memory().shared if hasattr(psutil.virtual_memory(), 'shared') else None,

        "swap_memory_total": psutil.swap_memory().total,
        "swap_memory_used": psutil.swap_memory().used,
        "swap_memory_free": psutil.swap_memory().free,
        "swap_memory_percent": psutil.swap_memory().percent,
        "swap_memory_sin": psutil.swap_memory().sin,
        "swap_memory_sout": psutil.swap_memory().sout,

        #Disk 
        "disk_partitions_device": psutil.disk_partitions(),## ~~~~~~~~~~~~~~~~~~divide in device, mountpoint etc.

        "disk_usage_total": psutil.disk_usage('/').total,
        "disk_usage_used": psutil.disk_usage('/').used,
        "disk_usage_free": psutil.disk_usage('/').free,
        "disk_usage_percent": psutil.disk_usage('/').percent,

        "disk_io_read_count": psutil.disk_io_counters().read_count,
        "disk_io_write_count": psutil.disk_io_counters().write_count,
        "disk_io_read_bytes": psutil.disk_io_counters().read_bytes,
        "disk_io_write_bytes": psutil.disk_io_counters().write_bytes,
        "disk_read_time": psutil.disk_io_counters().read_time,
        "disk_write_time": psutil.disk_io_counters().write_time,
        # "disk_busy_time": psutil.disk_io_counters().busy_time, # Linux 
        # "disk_read_merged_count": psutil.disk_io_counters().read_merged_count,
        # "disk_write_merged_count": psutil.disk_io_counters().write_merged_count,

        # Network
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ add more ??
        "net_io_bytes_sent": psutil.net_io_counters().bytes_sent,
        "net_io_bytes_recv": psutil.net_io_counters().bytes_recv,
        "net_io_packets_sent": psutil.net_io_counters().packets_sent,
        "net_io_packets_recv": psutil.net_io_counters().packets_recv,

        # Other System Info
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "users": len(psutil.users()),

        # Processes
        "num_of_process": len(psutil.pids())
    }
    return metrics

def save_metrics(metrics, filename):
    """Save collected metrics to a CSV file"""
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(filename, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=metrics.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(metrics)

def main(interval,filename):
    while True:
        # collect metrics  
        metrics = collect_metrics()
        # save metrics to csv
        save_metrics(metrics, filename)
        # interval of collection
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="The CSV filename to save the metrics.")
    args = parser.parse_args()
    
    main(10, args.filename)
