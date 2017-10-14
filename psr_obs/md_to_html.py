import sys
import os
import subprocess
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('md_file', help="The md file to convert to html")	
	parser.add_argument('style', help="Specify the type of webpage to create: code or video")

	args = parser.parse_args()

	in_file = args.md_file
	style = args.style

	file_name = in_file.strip('.md')
	command = ['pandoc', in_file, '-f', 'markdown', '-t', 'html' , '-o', '{}.html'.format(file_name)]
	print '{}'.format(" ".join(command))
	subprocess.call(command)
	html_file = open(file_name + '.html', 'r')
	lines = html_file.readlines()

	if style == 'code':
		css_location = '../css/code_style.css'
	elif style == 'video':
		css_location = '../css/video.css'
#	css_location = 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css'
	new_lines_top = ['<meta name="viewport" content="width=device-width, initial-scale=1">', '<link rel="stylesheet" href="{}">'.format(css_location), '<style>', '\t.markdown-body {', '\t\tbox-sizing: border-box;','\t\tmin-width: 200px;', '\t\tmax-width: 980px;', '\t\tmargin: 0 auto;', '\t\tpadding: 45px;', '\t}','\t@media (max-width: 767px) {', '\t\t.markdown-body {', '\t\t\tpadding: 15px;', '\t\t}', '\t}', '</style>', '<article class="markdown-body">']
	new_lines_bottom = ['</article>']

	out_file = open('{}.html'.format(file_name), 'w')

	for l in new_lines_top:
		if '\n' not in l:
			l += '\n'
		out_file.write(l)
	for l in lines:
		if '\n' not in l:
			l += '\n'
		out_file.write('\t' + l)
	for l in new_lines_bottom:
		if '\n' not in l:
			l += '\n'
		out_file.write(l)

if __name__ == '__main__':
	main()	
