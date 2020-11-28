# from irene
import argparse
import time
import pdb
import re, string
import shutil
import os
from urllib.request import urlopen
from os.path import join

PDF_DIR = 'pdfs/'
# WRITEUP_DIR = 'recipes/'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--folder", required = True, default="bread",help="writeup folder")
	args = parser.parse_args()

	folder = args.folder
	f = open(os.path.join(folder, 'today.md'), 'r')
	writeup = f.readlines()
	f.close()

	info_line = writeup[2]
	if 'TODO' in info_line:
		raise ValueError('today.md has no new information.')
	# authors_raw = info_line.split('[')[0]
	# authors_lst = authors_raw.split(', ')
	# authors_N = len(authors_lst)
	# try:
	# 	all_nums = re.findall(r'\d+', writeup[2])

	# 	year = all_nums[-2]
	# 	cite = all_nums[-1]
	# except:
	# 	pdb.set_trace()
	# 	raise ValueError('Year must end with digits, e.g. "2020."')

	# if authors_N < 4: 
	# 	md_title = []
	# 	for a in authors_lst:
	# 		a = a.strip()
	# 		first3 = a.split(' ')[-1][:3].replace('.', '')
	# 		md_title.append(first3)
	# 	md_title = ''.join(md_title)
	# else:
	# 	a = authors_lst[0]
	# 	first3 = a.split(' ')[-1][:3].replace('.', '')
	# 	md_title = '%sEtAl' % first3
	pattern = re.compile('[\W_]+')
	md_title = pattern.sub('', writeup[0]).lower()[:10]
	# md_tile = writeup[0].replaceAll("[^A-Za-z0-9]", "").lower()[:10]
	title = writeup[0][2:]
	# md_title = md_title + str(year)[-2:]
	md_fname = join(folder, md_title + '.md')

	g = open(md_fname, 'w')
	g.writelines(writeup)
	g.close()

	print('Wrote file to %s' % md_fname)

	f = open('README.md', 'r')
	readme = f.readlines()
	f.close()

	g = open('README_new.md', 'w')
	# readme = ['**MORE TO COME!**']
	# py.test.set_trace()
	found = False
	for i, line in enumerate(readme):
		g.write(line)
		# print(line.lower())
		if '## %s' % folder in line.lower():
			found = True
			date = time.strftime("%b %d, %Y")
			
			new_line = '**%s:** [%s](%s)' % (
				date, title, md_fname
				)
			g.write(new_line + '\n')
			g.write('\n')
			
	g.close()

	

	shutil.copy('README.md', 'README_old.md')
	shutil.move('README_new.md', 'README.md')

	shutil.copy('%s/today.md'% folder, '%s/old.md'%folder)
	shutil.copy('%s/template.md' %folder, '%s/today.md'%folder)
	print('Updated README.md')

if __name__ == '__main__':
	main()