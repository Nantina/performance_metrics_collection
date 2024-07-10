import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import psutil
import csv
import time
import argparse 
import os
import sys
from datetime import datetime
    
class FileHandler(FileSystemEventHandler):
    """File System Event Handling"""
    def __init__(self):
        self.files_created = 0
        self.files_deleted = 0
        self.files_modified = 0
        self.filed_moved = 0

    def on_modified(self, event):
        self.files_modified += 1

    def on_created(self, event):
        self.files_created += 1

    def on_deleted(self, event):
        self.files_deleted += 1
    
    def on_moved(self, event):
        self.filed_moved += 1

    def reset_counts(self):
        created = self.files_created
        deleted = self.files_deleted
        modified = self.files_modified
        moved = self.filed_moved
        self.files_created = 0
        self.files_deleted = 0
        self.files_modified = 0
        self.filed_moved = 0 
        return created, deleted, modified, moved

def collect_metrics(created, deleted, modified, moved):
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
        "kernel_version": os.uname().release,
        "system_name": os.uname().sysname,
        "node_name": os.uname().nodename,
        "machine": os.uname().machine,

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
        "cpu_times_nice": cpu_times.nice,
        "cpu_times_iowait": cpu_times.iowait,
        "cpu_times_irq": cpu_times.irq,
        "cpu_times_softirq": cpu_times.softirq,
        "cpu_times_steal": cpu_times.steal,
        "cpu_times_guest": cpu_times.guest,
        "cpu_times_guest_nice": cpu_times.guest_nice,

        # Memory 
        "virtual_memory_total": psutil.virtual_memory().total,
        "virtual_memory_available": psutil.virtual_memory().available,
        "virtual_memory_used": psutil.virtual_memory().used,
        "virtual_memory_percent": psutil.virtual_memory().percent,
        "virtual_memory_free": psutil.virtual_memory().free,
        "virtual_memory_active": psutil.virtual_memory().active,
        "virtual_memory_buffers": psutil.virtual_memory().buffers,
        "virtual_memory_cached": psutil.virtual_memory().cached,
        "virtual_memory_shared": psutil.virtual_memory().shared if hasattr(psutil.virtual_memory(), 'shared') else None,

        "swap_memory_total": psutil.swap_memory().total,
        "swap_memory_used": psutil.swap_memory().used,
        "swap_memory_free": psutil.swap_memory().free,
        "swap_memory_percent": psutil.swap_memory().percent,
        "swap_memory_sin": psutil.swap_memory().sin,
        "swap_memory_sout": psutil.swap_memory().sout,

        #Disk 
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
        "disk_busy_time": psutil.disk_io_counters().busy_time, 
        "disk_read_merged_count": psutil.disk_io_counters().read_merged_count,
        "disk_write_merged_count": psutil.disk_io_counters().write_merged_count,

        # Network
        "net_io_bytes_sent": psutil.net_io_counters().bytes_sent,
        "net_io_bytes_recv": psutil.net_io_counters().bytes_recv,
        "net_io_packets_sent": psutil.net_io_counters().packets_sent,
        "net_io_packets_recv": psutil.net_io_counters().packets_recv,
        "net_io_errin": psutil.net_io_counters().errin,
        "net_io_errout": psutil.net_io_counters().errout,
        "net_io_dropin": psutil.net_io_counters().dropin,
        "net_io_dropout": psutil.net_io_counters().dropout,
        "net_io_dropin": psutil.net_io_counters().dropin,
        # "num_of_net_connections": len(psutil.net_connections(kind='inet')),
        "net_connections": psutil.net_connections(kind='inet'),
        
        # Other System Info
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "users": len(psutil.users()),

        # Processes
        "num_of_process": len(psutil.pids()),

        # File system
        "num_of_files_created": created,
        "num_of_files_deleted": deleted,
        "num_of_files_modified": modified,
        "num_of_files_moved": moved
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
    """Reset file event counts and collect and save metrics"""
    try: 
        while True:
            created, deleted, modified, moved = event_handler.reset_counts()
            # collect metrics  
            metrics = collect_metrics(created, deleted, modified, moved)
            # save metrics to csv
            save_metrics(metrics, filename)
            # interval of collection
            time.sleep(interval)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()    

if __name__ == "__main__":
    # Extract the csv file name by the user
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="The CSV filename to save the metrics.")
    args = parser.parse_args()

    # Start the Observer 
    event_handler = FileHandler()
    observer = Observer()
    # observer.schedule(event_handler, path='c:\\', recursive=True) # Windows
    observer.schedule(event_handler, path='/home/', recursive=True) # Unix
    observer.start()
    
    main(1, args.filename)