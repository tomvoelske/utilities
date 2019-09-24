#!usr/bin/env python
import re
import subprocess
import threading


class Ping:

	ping_list = []
	found = 0
	not_found = 0
	responsive = 0
	unresponsive = 0

	def __init__(self, hostname):
		self.hostname = hostname
		self.ping_thread = threading.Thread(target=self.ping_test)
		self.ping_list.append(self)

	def ping_test(self):

		ip_pattern = '(\d+[.]\d+[.]\d+[.]\d+)'
		packet_loss_pattern = '(\d+)% packet loss'

		process = subprocess.Popen(['ping', '-c', '10', self.hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		outputs = process.communicate()
		ip_extract_raw = outputs[0].split('\n')[0]
		pattern_extract_raw = outputs[0]
		if re.search(ip_pattern, ip_extract_raw):
			ip_extract = re.findall(ip_pattern, ip_extract_raw)[0]
			packet_loss_extract = re.findall(packet_loss_pattern, pattern_extract_raw)[0]
			self.success_rate = str((100 - int(packet_loss_extract)))
			if self.success_rate == "0":
				Ping.unresponsive += 1
			else:
				Ping.responsive += 1
			Ping.found += 1
		else:
			ip_extract = 'DID NOT RESOLVE'
			self.success_rate = "N/A"
			Ping.not_found += 1
		self.result = '{0},{1},{2}'.format(self.hostname, ip_extract, self.success_rate)

	def start_thread(self):
		self.ping_thread.start()

	def end_thread(self):
		self.ping_thread.join()


def main():

	root_dir = '/directory/with/hostnames/file/'
	host_file_path = root_dir + 'hostnames.txt'
	result_file_path = root_dir + 'results.txt'

	with open(host_file_path, 'r') as host_file:
		host_list = host_file.readlines()
		host_list = [x.strip() for x in host_list]

	print('Found {0} hostnames to process.'.format(len(host_list)))

	for host in host_list:
		_ = Ping(host)

	# splits it into chunks to avoid excess memory consumption and silent failures

	MAX_CHUNK_SIZE = 250

	n_pings = len(Ping.ping_list)
	count = 0

	while count < n_pings:

		chunk_size = min(MAX_CHUNK_SIZE, n_pings)
		ping_chunk = Ping.ping_list[count: count + chunk_size]

		print('{0} / {1} processed - now beginning next {2}!'.format(count, n_pings, chunk_size))

		for ping in ping_chunk:
			ping.start_thread()
		for ping in ping_chunk:
			ping.end_thread()

		count += chunk_size

	with open(result_file_path, 'w') as result_file:
		result_file.write('HOSTNAME,IP_ADDRESS,PACKET_SUCCESS_RATE\n')
		for ping in Ping.ping_list:
			result_file.write(ping.result + '\n')

	print('Initial hostname amount: {0}\nResolved: {1}\nUnresolved: {2}\nOf resolved, responsive: {3}\n'
		  'Of resolved, completely unresponsive: {4}'.format(Ping.found + Ping.not_found, Ping.found, Ping.not_found,
												  			 Ping.responsive, Ping.unresponsive))
	print('Result file path: {0}'.format(result_file_path))


if __name__ == '__main__':
	main()
