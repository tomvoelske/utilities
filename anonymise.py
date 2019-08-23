#!usr/bin/env python
import re
import sys


def anonymise(inputfile):

	'''

	Purpose: "anonymises" python scripts, removing most identifying sensitive file locations/ip addresses.
	This makes the script suitable to share and display without worrying about compromising security
	
	:param inputfile: the script to anonymise
	:return: None
	'''

	# the filenamepattern will catch "secret" UNIX files but not those without extensions
	filenamepattern = "[.]?\w+[.][a-zA-Z]{1,3}\s*['\"]$"
	# filepathpattern works with UNIX paths only
	filepathpattern = '#?!?\w*\/?(?:\/\w+)+'
	ippattern = '\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}(?:\/\d{1,2})?'

	try:
		with open(inputfile, 'r') as startfile:
			olddata = startfile.read()

			filenames = re.findall(filenamepattern, olddata, re.MULTILINE)

			# anonymises file names first

			for filenameindex, filename in enumerate(filenames):
				olddata = olddata.replace(filename, 'anonymised_file_' + str(filenameindex))

			filepaths = re.findall(filepathpattern, olddata, re.MULTILINE)

			for filepath in filepaths:

				if filepath.startswith('#!'):
					# ignores shebang
					continue

				subnettest = filepath.replace('/', '')
				try:
					# do nothing, this is just a subnet mask
					_ = int(subnettest)
				except ValueError:
					# proceed with anonymising
					olddata = olddata.replace(filepath, '/anonymised/path')

			olddata = re.sub(ippattern, 'ano.nym.ise.dip', olddata)

		newfilename = inputfile.replace('.py', '') + '_anonymised.py'

		with open(newfilename, 'w') as newfile:
			newfile.write(olddata)

		print('Please note that this will NOT replace any base64 values and may not be comprehensive. Please check the ')
		print('final file destination: {0}'.format(newfilename))

	except IOError:
		print('File does not exist.')


if __name__ == '__main__':
	try:
		anonymise(sys.argv[1])
	except IndexError:
		print('Please pass a filename as a parameter.')
