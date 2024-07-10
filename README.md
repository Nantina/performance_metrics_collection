# Overview 
The `feature_extraction.py` script has been created for system performance metrics collection of a raspberry pi3 device.
It logs these metrics into a CSV file at specified intervals. 
The script utilizes the [psutil](https://psutil.readthedocs.io/en/latest/) library to gather system performance data and [watchdog](https://pypi.org/project/watchdog/) library to track file system changes.

# System Performance Metrics 
The specific system performance metrics that can be monitored with the script are mentioned below: 
- Kernel Info (using the `os` and `sys` packages)
- CPU Metrics  
- Memory Metrics (Virtual and Swap)
- Disk Metrics 
- Network Metrics (network I/O statistics) 
- Other System Info (Boot Time, Users, Number of Processes)
- File System Events (Monitoring the root directory) 

# Script Description 
## File System Monitoring 
For the file system monintoring, the `FileHandler` class is created, derived from FileSystemEventHandler. This class is used to handle file system events (file creation, deletion, modification, and movement)

The `on_created`, `on_deleted`, `on_modified`, and `on_moved` methods increment counters for each respective event.
The reset_counts method resets these counters and returns their current values.
## System Metrics Collection

The `collect_metrics` function gathers various system metrics using the psutil library.
This function also includes information about the operating system, kernel, and boot time.

## Saving to CSV file

The `save_metrics` function saves the collected metrics to a CSV file based on the filename provided by the user.
## Main Function

The main function resets the file event counts, collects metrics, and saves them to the CSV file at specified intervals. The sampling interval has been set to 1 second.

# Testing - Results - Usage 
## Prerequisites 
- `Python 3`
- `psutil`
- `watchdog`
## Usage 
In order to execute the script and collect system performance metrics of a machine the following command is used: 
``` bash
    python3 feature_extraction.py <file_name_to_store_the_results.csv>
```

The file should be executed in Unix (some of the included functions are not supported in Windows).
## Results 
The script has been tested in 3 operating systems: 
- Windows 11 (excluding some of the functions) -> `windows_metrics.csv`
- Linux (Ubuntu 22.04) -> `linux_metrics.csv`
- Emulated Raspberry pi3 using QEMU -> `raspberrypi_metrics.csv`

The csv files produced for each of the operating systems are included in this repository. 

