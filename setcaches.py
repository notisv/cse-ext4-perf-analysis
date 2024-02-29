# Code to set up the correct cache parameters
# Lia Vergou, AM 4325
# Notis Vouzalis, AM 2653

##### IMPORTANT NOTES #####
# /proc/sys/vm/drop_caches
# Write the value "3" to this file to empty the cache memory

# /proc/sys/vm/dirty_expire_centisecs
# Defines after how many centisecs the cached data are written to the disk
# Default value is 3000 centisecs == 30 sec - SET THIS TO A VALUE UP TO 500 centisecs == 5 sec

# /proc/sys/vm/dirty_writeback_centisecs
# Defines the interval between runs of the threads that move data from the caches to the disk
# Default value is 500 centisecs == 5 sec - SET THIS TO A VALUE OF 100 centisecs == 1 sec

import subprocess

# Benchmark run time of 60 seconds means dirty_expire will be called at least 20 times
# Benchmark run time of 30 seconds means dirty_expire will be called at least 10 times
dirty_expire = 300 # centisecs
dirty_writeback = 100 # centisecs

def setcaches():
	# Clean filesystem caches
	print('Cleaned filesystem caches.')
	subprocess.run(['echo', '3'], stdout = open('/proc/sys/vm/drop_caches', 'wb'))

	# Set dirty_expire
	print('Set dirty_expire to %i seconds.' % (dirty_expire/100))
	try:
	    with open('/proc/sys/vm/dirty_expire_centisecs', 'w') as file:
	    	file.write(str(dirty_expire))

	except FileNotFoundError as e:
	    print('Cannot open dirty_expire_centisecs. Quitting...')
	    sys.exit()

	# Set dirty_writeback
	print('Set dirty_writeback to %i seconds.' % (dirty_writeback/100))
	try:
	    with open('/proc/sys/vm/dirty_writeback_centisecs', 'w') as file:
	    	file.write(str(dirty_writeback))

	except FileNotFoundError as e:
	    print('Cannot open dirty_writeback_centisecs. Quitting...')
	    sys.exit()

#setcaches()