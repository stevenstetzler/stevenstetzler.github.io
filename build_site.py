#!/usr/bin/python
import sys
import os
import subprocess
import argparse
from glob import glob

def add_to_html(html_file_name, css_location):
	html_file = open(html_file_name, 'r')
	lines = html_file.readlines()

	new_lines_top = ['<meta name="viewport" content="width=device-width, initial-scale=1">', '<link rel="stylesheet" href="{}">'.format(css_location), '<style>', '\t.markdown-body {', '\t\tbox-sizing: border-box;','\t\tmin-width: 200px;', '\t\tmax-width: 980px;', '\t\tmargin: 0 auto;', '\t\tpadding: 45px;', '\t}','\t@media (max-width: 767px) {', '\t\t.markdown-body {', '\t\t\tpadding: 15px;', '\t\t}', '\t}', '</style>', '<article class="markdown-body">']
	new_lines_bottom = ['</article>']

	out_file = open(html_file_name, 'w')

	print "Adding CSS from {} to HTML {}".format(css_location, html_file_name)

	for l in new_lines_top:
		if '\n' not in l:
			l += '\n'
		out_file.write(l)
	for l in lines:
		if '\n' not in l:
			l += '\n'
		out_file.write(l)
	for l in new_lines_bottom:
		if '\n' not in l:
			l += '\n'
		out_file.write(l)


def descend(directory):
	# Build all sub-directories as well
	all_files = glob(os.path.join(directory, '*'))
	dirs = [f for f in all_files if os.path.isdir(f)]
	for d in dirs:
		print "Moving into directory {}".format(d)
		build(d)	


def build(directory):
	md_files = glob(os.path.join(directory, '*.md'))
	css_files = glob(os.path.join(directory, '*.css'))
	if len(css_files) > 1:
		print "Warning: More than one css file in directory: {} - Moving one directory lower".format(directory)
		descend(directory)
		return
	elif len(css_files) == 0:
		descend(directory)
		return

	css_file = os.path.basename(css_files[0])

	for md in md_files:	

		directory_name = os.path.dirname(md)
		file_name = os.path.basename(md)
		html_file_name = os.path.join(directory_name, '{}.html'.format(file_name.strip('.md')))
		
		command = ['pandoc', md, '-f', 'markdown', '-t', 'html' , '-o', html_file_name]
		print '{}'.format(" ".join(command))
		subprocess.call(command)
		add_to_html(html_file_name, css_file)

	descend(directory)


def main():
	build(os.path.join("./"))


if __name__ == '__main__':
	main()	
