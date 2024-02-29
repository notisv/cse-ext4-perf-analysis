# Code to parse the output files
# Lia Vergou, AM 4325
# Notis Vouzalis, AM 2653

def parse_cpustats(path):
    try:
        with open(path + '/cpu_stats.txt', 'r') as file:
            last_line = file.readlines()[-1]
            #print(last_line)
            tokens = last_line.split()
            #print(tokens)
            cpu_usr_avg = float(tokens[2])
            cpu_sys_avg = float(tokens[4])
            cpu_iowait_avg = float(tokens[5])
            cpu_idle_avg = float(tokens[7])
            #print('cpu_usr_avg_% = %.2f / cpu_sys_avg_% = %.2f / cpu_iowait_avg_% = %.2f / cpu_idle_avg_% = %.2f' % (cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg))
            return cpu_usr_avg, cpu_sys_avg, cpu_iowait_avg, cpu_idle_avg

    except FileNotFoundError as e:
        print('Cannot open cpu_stats.txt. Quitting...')
        sys.exit()

def parse_memorystats(path):
    try:
        with open(path + '/memory_stats.txt', 'r') as file:
            last_line = file.readlines()[-1]
            #print(last_line)
            tokens = last_line.split()
            #print(tokens)
            mem_used_avg = float(tokens[4])
            commit_avg = float(tokens[8])
            #print('mem_used_avg_% = %.2f / commit_avg_% = %.2f' % (mem_avg, commit_avg))
            return mem_used_avg, commit_avg

    except FileNotFoundError as e:
        print('Cannot open memory_stats.txt. Quitting...')
        sys.exit()

def parse_diskstats(path):
    try:
        with open(path + '/disk_stats.txt', 'r') as file:
            last_line = file.readlines()[-1]
            #print(last_line)
            tokens = last_line.split()
            #print(tokens)
            tps_avg = float(tokens[2])
            rkBs_avg = float(tokens[3])
            wKBs_avg = float(tokens[4])
            util_avg = float(tokens[9])
            #print('transfers per sec_avg = %.2f / read kBs_avg = %.2f / written KBs_avg = %.2f / util_avg_% = %.2f' % (tps_avg, rkBs_avg, wKBs_avg, util_avg))
            return tps_avg, rkBs_avg, wKBs_avg, util_avg

    except FileNotFoundError as e:
        print('Cannot open disk_stats.txt. Quitting...')
        sys.exit()

def parse_filebenchstats(path):
    try:
        with open(path + '/filebench_stats.txt', 'r') as file:
            lines = file.readlines()
            mem_allocation = lines[1]
            workload = lines[2]
            logfiles_stats = lines[4]
            bigfileset_stats = lines[8]
            filereader_instances = lines[14]
            run_time = lines[16]
            io_summary = lines[-2]

            io_summary_tokens = io_summary.split()
            #print(io_summary_tokens)
            total_ops = int(io_summary_tokens[3])
            ops_per_sec = float(io_summary_tokens[5])
            reads_writes = io_summary_tokens[7]
            reads_writes = reads_writes.replace('/', ' ')
            reads = int(reads_writes.split()[0])
            writes = int(reads_writes.split()[1])
            mb_per_sec = float((io_summary_tokens[9])[:-4])
            ms_per_op = float((io_summary_tokens[10])[:-5])

            #print('Filebench stats:')
            #print('\t' + mem_allocation[:-1])
            #print('\t' + workload[:-1])
            #print('\t' + logfiles_stats[:-1])
            #print('\t' + bigfileset_stats[:-1])
            #print('\t' + filereader_instances[:-1])
            #print('\t' + run_time[:-1])
            #print('\t' + io_summary[:-1])

            #print('\ttotal ops = %i / ops_per_sec = %.3f / reads/writes = %i/%i / mb_per_sec = %.1f / ms_per_op = %.1f' % (total_ops, ops_per_sec, reads, writes, mb_per_sec, ms_per_op))

            return mem_allocation, workload, logfiles_stats, bigfileset_stats, filereader_instances, run_time, io_summary, total_ops, ops_per_sec, reads, writes, mb_per_sec, ms_per_op

    except FileNotFoundError as e:
        print('Cannot open filebench_stats.txt. Quitting...')
        sys.exit()

def parse_perfdata(path):
    try:
        with open(path + '/perf_data.txt', 'r') as file:
            lines = file.readlines()
            perf_data = []
            for id in range(11,21):
                #print((lines[id])[:-1])
                perf_data.append((lines[id])[:-1])

            return perf_data

    except FileNotFoundError as e:
        print('Cannot open perf_data.txt. Quitting...')
        sys.exit()

def parse_perfstat(path):
    try:
        with open(path + '/perf_stat.txt', 'r') as file:
            lines = file.readlines()
            context_switches_line = lines[6]
            page_faults_line = lines[8]
            L1_dcache_misses_line = lines[17]
            L1_icache_misses_line = lines[21]
            
            #print(context_switches_line[:-1])
            #print(page_faults_line[:-1])
            #print(L1_dcache_misses_line[:-1])
            #print(L1_icache_misses_line[:-1])

            context_switches = int(context_switches_line.split()[0].replace(',', ''))
            page_faults = int(page_faults_line.split()[0].replace(',', ''))
            L1_dcache_misses = float(L1_dcache_misses_line.split()[3].replace('%', ''))
            L1_icache_misses = float(L1_icache_misses_line.split()[3].replace('%', ''))

            #print('context switches = %i / page faults = %i / L1 dcache misses percentage = %.2f / L1 icache misses percentage = %.2f' % (context_switches, page_faults, L1_dcache_misses, L1_icache_misses))
            return context_switches_line, page_faults_line, L1_dcache_misses_line, L1_icache_misses_line, context_switches, page_faults, L1_dcache_misses, L1_icache_misses

    except FileNotFoundError as e:
        print('Cannot open perf_stat.txt. Quitting...')
        sys.exit()

#parse_filebenchstats('./run_1')