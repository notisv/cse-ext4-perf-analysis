# Code to automate the running of experiments
# Lia Vergou, AM 4325
# Notis Vouzalis, AM 2653

##### IMPORTANT NOTES #####
# start-disk.sh: Changed first line shebang to #!/bin/bash instead of #/bin/bash
# stop-disk.sh: Changed first line shebang to #!/bin/bash instead of #/bin/bash
# Redirected output of mpstat, iostat, vmstat, to directories in the same location as autoexp.py
# Redirected output of sar to directory in the same location as autoexp.py
# Redirected output of perf record to directory in the same location as autoexp.py
# Redirected output of perf stat to directory in the same location as autoexp.py
# Redirected output of filebench to directory in the same location as autoexp.py

import subprocess
from datetime import datetime
import time
import sys
import os
import math
import setcaches
import parsefiles

def fibonacci_stress(n):
    if n < 2: return n
    return fibonacci_stress(n-1) + fibonacci_stress(n-2)

def create_directory(dirName):
    parent_dir = './'
    path = os.path.join(parent_dir, dirName)
    os.mkdir(path)

def start_usage_monitoring(dirName, interval):
    print('\nStarting resource usage monitors...')
    
    # Open mpstat, vmstat, iostat, perf in background with Popen
    #subprocess.Popen(['mpstat', interval], stdout = open(dirName + '/mpstat.out', 'wb'))
    #subprocess.Popen(['iostat', '-d', interval], stdout = open(dirName + '/iostat.out', 'wb'))
    #subprocess.Popen(['vmstat', interval], stdout = open(dirName + '/vmstat.out', 'wb'))
    subprocess.Popen(['sar', interval], stdout = open(dirName + '/cpu_stats.txt', 'w'))
    subprocess.Popen(['sar', '-r', interval], stdout = open(dirName + '/memory_stats.txt', 'w'))
    subprocess.Popen(['sar', '-d', interval], stdout = open(dirName + '/disk_stats.txt', 'w'))
    #subprocess.Popen(['sar', '-B', interval], stdout = open(dirName + '/paging_stats.txt', 'w'))
    subprocess.Popen(['perf', 'record', '-o', './' + dirName + '/perf.data'])
    subprocess.Popen(['perf', 'stat', '-ddd', '-o', './' + dirName + '/perf_stat.txt'])

def execute_benchmark(dirName):
    print('\nExecuting stress test with workload %s on ext4 journal mode %s' % (workload_path, ext4_dataMode))
    print('Approximate run duration: 60 seconds /// 30 seconds to create fileset - 30 seconds to benchmark')
    #print('Approximate run duration: 120 seconds /// 60 seconds to create fileset - 60 seconds to benchmark')
    #print('The %ith fibonacci number is: %i' % (40, fibonacci_stress(40))) # use number greater than 35
    subprocess.run(['filebench', '-f', workload_path], stdout = open(dirName + '/filebench_stats.txt', 'w'))

def stop_usage_monitoring():
    print('\nStopping resource usage monitors...\n')

    #subprocess.run(['pkill', '-2', 'mpstat'])
    #subprocess.run(['pkill', '-2', 'iostat'])
    #subprocess.run(['pkill', '-2', 'vmstat'])
    subprocess.run(['pkill', '-2', 'sar'])
    subprocess.run(['pkill', '-2', 'perf'])
    time.sleep(2) # Give some time to filebench perf in order to print the stderr on screen

def perf_data_to_txt(dirName):
    os.chdir(dirName)
    subprocess.run(['perf', 'report'], stdout = open('perf_data.txt', 'w'))
    os.chdir('..')

def calculate_statistics():
    cpu_usr_avg = total_cpu_usr / runs
    cpu_sys_avg = total_cpu_sys / runs
    cpu_iowait_avg = total_cpu_iowait / runs
    cpu_idle_avg = total_cpu_idle / runs

    mem_used_avg = total_mem_used / runs
    mem_commit_avg = total_mem_commit / runs

    disk_tps_avg = total_disk_tps / runs
    disk_read_kBs_avg = total_disk_read_kBs / runs
    disk_write_kBs_avg = total_disk_write_kBs / runs
    disk_util_avg = total_disk_util / runs

    ops_avg = total_ops / runs
    ops_per_sec_avg = total_ops_per_sec / runs
    reads_avg = total_reads / runs
    writes_avg = total_writes / runs
    mb_per_sec_avg = total_mb_per_sec / runs
    ms_per_op_avg = total_ms_per_op / runs

    # top1_processes is a global variable
    # top2_processes is a global variable     

    context_switches_avg = total_context_switches / runs
    page_faults_avg = total_page_faults / runs
    l1_dcache_misses_avg = total_l1_dcache_misses / runs
    l1_icache_misses_avg = total_l1_icache_misses / runs

    return cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg, mem_used_avg, mem_commit_avg, disk_tps_avg, disk_read_kBs_avg, disk_write_kBs_avg, disk_util_avg, ops_avg, ops_per_sec_avg, reads_avg, writes_avg, mb_per_sec_avg, ms_per_op_avg, context_switches_avg, page_faults_avg, l1_dcache_misses_avg, l1_icache_misses_avg

def print_statistics():
    cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg, mem_used_avg, mem_commit_avg, disk_tps_avg, disk_read_kBs_avg, disk_write_kBs_avg, disk_util_avg, ops_avg, ops_per_sec_avg, reads_avg, writes_avg, mb_per_sec_avg, ms_per_op_avg, context_switches_avg, page_faults_avg, l1_dcache_misses_avg, l1_icache_misses_avg = calculate_statistics()

    try:
        with open('benchmark_stats.txt', 'w') as file:
            print('Average CPU util percentage (user): %.2f / Average CPU util percentage (sys): %.2f / Average CPU iowait percentage: %.2f / Average CPU idle percentage: %.2f' % (cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg))
            file.write('Average CPU util percentage (user): %.2f / Average CPU util percentage (sys): %.2f / Average CPU iowait percentage: %.2f / Average CPU idle percentage: %.2f' % (cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg))
            file.write('\n')

            print('Average memory usage percentage: %.2f / Average memory commit percentage: %.2f' % (mem_used_avg, mem_commit_avg))
            file.write('Average memory usage percentage: %.2f / Average memory commit percentage: %.2f' % (mem_used_avg, mem_commit_avg))
            file.write('\n')

            print('Average disk tranfers per second (tps): %.2f / Average disk read kBs: %.2f / Average disk write kBs: %.2f / Average disk util percentage: %.2f' % (disk_tps_avg, disk_read_kBs_avg, disk_write_kBs_avg, disk_util_avg))
            file.write('Average disk tranfers per second (tps): %.2f / Average disk read kBs: %.2f / Average disk write kBs: %.2f / Average disk util percentage: %.2f' % (disk_tps_avg, disk_read_kBs_avg, disk_write_kBs_avg, disk_util_avg))
            file.write('\n')

            print('Average ops: %i / Average ops per sec: %.2f / Average reads: %i / Average writes: %i / Average mb/s: %.2f / Average ms/op: %.2f' % (ops_avg, ops_per_sec_avg, reads_avg, writes_avg, mb_per_sec_avg, ms_per_op_avg))
            file.write('Average ops: %i / Average ops per sec: %.2f / Average reads: %i / Average writes: %i / Average mb/s: %.2f / Average ms/op: %.2f' % (ops_avg, ops_per_sec_avg, reads_avg, writes_avg, mb_per_sec_avg, ms_per_op_avg))
            file.write('\n')

            print('Average context switches: %i / Average page faults: %i / Average L1 dcache misses percentage: %.2f / Average L1 icache misses percentage: %.2f' % (context_switches_avg, page_faults_avg, l1_dcache_misses_avg, l1_icache_misses_avg))
            file.write('Average context switches: %i / Average page faults: %i / Average L1 dcache misses percentage: %.2f / Average L1 icache misses percentage: %.2f' % (context_switches_avg, page_faults_avg, l1_dcache_misses_avg, l1_icache_misses_avg))
            file.write('\n')

            print('Top 2 processes of each run:'); print('~~~~~~~~~~')
            file.write('Top 2 processes of each run:\n'); file.write('~~~~~~~~~~\n')
            for id in range(runs):
                print(top1_processes[id])
                print(top2_processes[id])
                print('~~~~~~~~~~')

            for id in range(runs):
                file.write(top1_processes[id]); file.write('\n')
                file.write(top2_processes[id]); file.write('\n')
                file.write('~~~~~~~~~~\n')

    except FileNotFoundError as e:
        print('Cannot create benchmark_stats.txt. Quitting...')
        sys.exit()

def calculate_standard_deviation(operations_tput_avg, opsPerSec_tput_avg, reads_tput_avg, writes_tput_avg):
    sum_of_squares_ops = 0
    sum_of_squares_opsPerSec = 0
    sum_of_squares_reads = 0
    sum_of_squares_writes = 0
    for run_id in range(runs):
        sum_of_squares_ops += (operations_list[run_id] - operations_tput_avg) ** 2
        sum_of_squares_opsPerSec += (opsPerSec_list[run_id] - opsPerSec_tput_avg) ** 2
        sum_of_squares_reads += (reads_list[run_id] - reads_tput_avg) ** 2
        sum_of_squares_writes += (writes_list[run_id] - writes_tput_avg) ** 2

    variance_ops = sum_of_squares_ops / runs
    variance_opsPerSec = sum_of_squares_opsPerSec / runs
    variance_reads = sum_of_squares_reads / runs
    variance_writes = sum_of_squares_writes / runs

    sd_ops = math.sqrt(variance_ops)
    sd_opsPerSec = math.sqrt(variance_opsPerSec)
    sd_reads = math.sqrt(variance_reads)
    sd_writes = math.sqrt(variance_writes)

    return sd_ops, sd_opsPerSec, sd_reads, sd_writes

def calculate_95conf_interval(sd_ops, sd_opsPerSec, sd_reads, sd_writes, operations_tput_avg, opsPerSec_tput_avg, reads_tput_avg, writes_tput_avg):
    df = runs - 1 # degrees of freedom
    cl = (1 - 0.95) / 2 # 95% confidence level

    tDistr_res = tDistribution_95_conf[df - 1]

    res_ops = sd_ops / math.sqrt(runs)
    res_opsPerSec = sd_opsPerSec / math.sqrt(runs)
    res_reads = sd_reads / math.sqrt(runs)
    res_writes = sd_writes / math.sqrt(runs)

    mul_ops = tDistr_res * res_ops
    mul_opsPerSec = tDistr_res * res_opsPerSec
    mul_reads = tDistr_res * res_reads
    mul_writes = tDistr_res * res_writes

    # Upper tail probability
    conf95_ops = mul_ops + operations_tput_avg
    conf95_opsPerSec = mul_opsPerSec + opsPerSec_tput_avg
    conf95_reads = mul_reads + reads_tput_avg
    conf95_writes = mul_writes + writes_tput_avg

    return conf95_ops, conf95_opsPerSec, conf95_reads, conf95_writes

####################

total_cpu_usr = 0.0 # percentage
total_cpu_sys = 0.0 # percentage
total_cpu_iowait = 0.0 # percentage
total_cpu_idle = 0.0 # percentage

total_mem_used = 0.0 # percentage
total_mem_commit = 0.0 # percentage

total_disk_tps = 0.0 # float
total_disk_read_kBs = 0.0 # float
total_disk_write_kBs = 0.0 # float
total_disk_util = 0.0 # percentage

total_ops = 0 # float
total_ops_per_sec = 0.0 # float
total_reads = 0 # int
total_writes = 0 # int
total_mb_per_sec = 0.0 # float
total_ms_per_op = 0.0 # float

top1_processes = [] # string list
top2_processes = [] # string list

total_context_switches = 0 # int
total_page_faults = 0 # int
total_l1_dcache_misses = 0.0 # percentage
total_l1_icache_misses = 0.0 # percentage

####################

operations_list = []
opsPerSec_list = []
reads_list = []
writes_list = []

####################

tDistribution_95_conf = [12.076, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093]

####################

alpha = 0.05 # 95% confidence interval
ext4_dataMode = 'ext4-journal' # ext4-journal, ext4-ordered, ext4-writeback

workload = 'webserver.f'
workload_path = './workloads/' + workload

polling_interval = '2' # Polling time in seconds for the usage monitors
print_detailed_run_statistics = False # Set to True to print each run's statistics in detail

runs = 0 # experiment repetitions
moreRunsNeeded = True # flag used to stop experiment

print('////////// Autobench started //////////\n')
setcaches.setcaches() # Clean caches, set dirty_expire to 5 sec, set dirty_writeback to 1 sec
print('\nExt4 Journal mode =', ext4_dataMode)
print('\nUsage monitors polling interval = %s seconds' % polling_interval)
print('\nExecuting experiments...\n')

# Make sure that /dev/sda3 is unmounted before running experiments
print('Confirming /dev/sda3/ is not mounted before starting the benchmark...')
subprocess.run('/root/scripts/stop-disk.sh')

while (moreRunsNeeded == True) and (runs < 20):
    # Update number of runs
    runs +=1
    print('\n////////// Run ' + str(runs) + ' started //////////')

    # Clean filesystem caches
    print('\nCleaning filesystem caches...')
    subprocess.run(['echo', '3'], stdout = open('/proc/sys/vm/drop_caches', 'wb'))

    # Start a clean filesystem
    print('\nStarting filesystem...')
    subprocess.run(['/root/scripts/start-disk.sh', ext4_dataMode])

    # Create a directory for the output files of the run
    outputDirName = 'run_' + str(runs)
    create_directory(outputDirName)
    print('\nRedirecting mpstat, vmstat, iostat, sar, perf, filebench outputs to ./%s/' % outputDirName)

    # Start resource usage monitors and write output to files
    start_usage_monitoring(outputDirName, polling_interval)
    print('\nBenchmark start time:', datetime.now().strftime('%H:%M:%S'),
        '(Cross reference with usage monitors)')

    # Run benchmark and write output to file
    execute_benchmark(outputDirName)
    # Sometimes (not always) the following warning comes up at this point when calling the method execute_benchmark()
    # Lowering default frequency rate to 1750.
    # Please consider tweaking /proc/sys/kernel/perf_event_max_sample_rate.

    # Stop resource usage monitors
    stop_usage_monitoring()
    print('\nBenchmark end time:', datetime.now().strftime('%H:%M:%S'),
        '(Cross reference with usage monitors)')

    # Print perf.data to perf_data.txt
    perf_data_to_txt(outputDirName)

    # Update statistical metrics
    print('\nRun %s statistics:\n' % str(runs))

    # cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg
    cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg = parsefiles.parse_cpustats('./run_' + str(runs))
    total_cpu_usr += cpu_usr_avg
    total_cpu_sys += cpu_sys_avg
    total_cpu_iowait += cpu_iowait_avg
    total_cpu_idle += cpu_idle_avg
    print('cpu_usr_avg percentage = %.2f / cpu_sys_avg percentage = %.2f / cpu_iowait_avg percentage = %.2f / cpu_idle_avg percentage = %.2f' % (cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg))
    
    # mem_avg, commit_avg
    mem_avg, commit_avg = parsefiles.parse_memorystats('./run_' + str(runs))
    total_mem_used += mem_avg
    total_mem_commit += commit_avg
    print('mem_used_avg percentage = %.2f / commit_avg percentage = %.2f' % (mem_avg, commit_avg))

    # disk_read_tput_avg, disk_write_tput_avg
    tps_avg, rkBs_avg, wKBs_avg, util_avg = parsefiles.parse_diskstats('./run_' + str(runs))
    total_disk_tps += tps_avg
    total_disk_read_kBs += rkBs_avg
    total_disk_write_kBs += wKBs_avg
    total_disk_util += util_avg
    print('disk transfers per sec_avg = %.2f / disk read kBs_avg = %.2f / disk written KBs_avg = %.2f / disk util_avg percentage = %.2f' % (tps_avg, rkBs_avg, wKBs_avg, util_avg))

    # filebench stats
    mem_allocation, workload, logfiles_stats, bigfileset_stats, filereader_instances, run_time, io_summary, ops, ops_per_sec, reads, writes, mb_per_sec, ms_per_op = parsefiles.parse_filebenchstats('./run_' + str(runs))
    total_ops += ops
    total_ops_per_sec += ops_per_sec
    total_reads += reads
    total_writes += writes
    total_mb_per_sec += mb_per_sec
    total_ms_per_op += ms_per_op

    operations_list.append(ops)
    opsPerSec_list.append(ops_per_sec)
    reads_list.append(reads)
    writes_list.append(writes)

    if print_detailed_run_statistics == True:
        print('Filebench stats:')
        print('\t' + mem_allocation[:-1])
        print('\t' + workload[:-1])
        print('\t' + logfiles_stats[:-1])
        print('\t' + bigfileset_stats[:-1])
        print('\t' + filereader_instances[:-1])
        print('\t' + run_time[:-1])
        print('\t' + io_summary[:-1])
        print('\t', end ='')
    print('total ops = %i / ops_per_sec = %.3f / reads/writes = %i/%i / mb_per_sec = %.1f / ms_per_op = %.1f' % (ops, ops_per_sec, reads, writes, mb_per_sec, ms_per_op))

    # perf.data
    perf_data = parsefiles.parse_perfdata('./run_' + str(runs))
    if print_detailed_run_statistics == True:
        print('Perf_data stats:')
        for elem in perf_data: print('\t' + elem)
    top1_processes.append(perf_data[0])
    top2_processes.append(perf_data[1])

    # perf_stat
    context_switches_line, page_faults_line, L1_dcache_misses_line, L1_icache_misses_line, context_switches, page_faults, L1_dcache_misses, L1_icache_misses = parsefiles.parse_perfstat('./run_' + str(runs))
    total_context_switches += context_switches
    total_page_faults += page_faults
    total_l1_dcache_misses += L1_dcache_misses
    total_l1_icache_misses += L1_icache_misses
    if print_detailed_run_statistics == True:
        print('Perf_stat stats:')
        print('\t' + context_switches_line[:-1])
        print('\t' + page_faults_line[:-1])
        print('\t' + L1_dcache_misses_line[:-1])
        print('\t' + L1_icache_misses_line[:-1])
        print('\t', end ='')
    print('context switches = %i / page faults = %i / L1 dcache misses percentage = %.2f / L1 icache misses percentage = %.2f' % (context_switches, page_faults, L1_dcache_misses, L1_icache_misses))

    # Update result metrics
    # total_tput_avg
    # read_tput_avg
    # write_tput_avg
    # ...

    # Metric chosen: operations
    print('\nOperation-centric throughputs across %i runs:' % runs)
    operations_tput_avg = total_ops / runs
    opsPerSec_tput_avg = total_ops_per_sec / runs
    reads_tput_avg = total_reads / runs
    writes_tput_avg = total_writes / runs
    print('Total operations average throuput: %i/run' % operations_tput_avg)
    print('Operations/sec average throuput: %i/run' % opsPerSec_tput_avg)
    print('Reads average throuput: %i/run' % reads_tput_avg)
    print('Writes average throuput: %i/run' % writes_tput_avg)

    # Choose one metric and calculate
    # 1 - Standard deviation
    # 2 - 95% confidence interval

    sd_ops, sd_opsPerSec, sd_reads, sd_writes = calculate_standard_deviation(operations_tput_avg, opsPerSec_tput_avg, reads_tput_avg, writes_tput_avg)
    print('\nStandard deviations across %i runs:' % runs)
    print('Total ops standard deviation: %.2f' % sd_ops)
    print('Ops/sec standard deviation: %.2f' % sd_opsPerSec)
    print('Reads standard deviation: %.2f' % sd_reads)
    print('Writes standard deviation: %.2f' % sd_writes)

    # Check if more runs are needed
    # if 95_conf_interval / avg_of_chosen_metric < alpha: moreRunsNeeded = False

    if runs > 1:
        conf95_ops, conf95_opsPerSec, conf95_reads, conf95_writes = calculate_95conf_interval(sd_ops, sd_opsPerSec, sd_reads, sd_writes, operations_tput_avg, opsPerSec_tput_avg, reads_tput_avg, writes_tput_avg)
        print('\n95-percent confidence intervals across %i runs:' % runs)
        print('Total ops 95-percent confidence interval: %.2f' % conf95_ops)
        print('Ops/sec 95-percent confidence interval: %.2f' % conf95_opsPerSec)
        print('Reads 95-percent confidence interval: %.2f' % conf95_reads)
        print('Writes 95-percent confidence interval: %.2f' % conf95_writes)

        # Check if more runs are needed
        print('\nconf95_ops/ ops avg = %.2f' % (conf95_ops / operations_tput_avg))
        #if conf95_ops / operations_tput_avg < alpha: moreRunsNeeded = False

        print('conf95_opsPerSec/ opsPerSec avg = %.2f' % (conf95_opsPerSec / opsPerSec_tput_avg))
        if conf95_opsPerSec / opsPerSec_tput_avg < alpha: moreRunsNeeded = False

        print('conf95_reads/ reads avg = %.2f' % (conf95_reads / reads_tput_avg))
        #if conf95_reads / reads_tput_avg < alpha: moreRunsNeeded = False

        print('conf95_writes/ writes avg = %.2f' % (conf95_writes / writes_tput_avg))
        #if conf95_writes / writes_tput_avg < alpha: moreRunsNeeded = False

    # Stop the filesystem
    print('\nStopping filesystem...')
    subprocess.run('/root/scripts/stop-disk.sh')

    # Be a helpful little script
    print('\nCheck ./%s/ for the above results...' % outputDirName)

# Print statistics and results
print('\n////////// Autobench ended //////////\n')
print('Statistics:')
print_statistics()