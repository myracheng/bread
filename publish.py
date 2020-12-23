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
	
	md_title = []
	t_list = writeup[0][2:].lower().split(' ')
	for word in t_list:
		md_title.append(word[:3])

	title = writeup[0][2:-1]
	md_title = ''.join(md_title)
	md_fname = join(folder, md_title + '.md')

	g = open(md_fname, 'w')
	g.writelines(writeup)
	g.close()

	print('Wrote file to %s' % md_fname)

	f = open('README.md', 'r')
	readme = f.readlines()
	f.close()

	g = open('README_new.md', 'w')
	found = False
	for i, line in enumerate(readme):
		g.write(line)
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