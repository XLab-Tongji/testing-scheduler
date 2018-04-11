#!/usr/bin/env python
import click
import os
from testservice import TestService
@click.command()
@click.option("--src", help="file path of test case")
def parse(src):
	file_prefix, file_name = os.path.split(src)
	print 'start to parse the test case:', file_name
	with open(src) as f:
		print "start to read the file: ", src
		parseStory(f)

def parseStory(file):
	lines = [line.strip() for line in file.readlines()]
	print lines,len(lines)
	max_line = len(lines)
	line_num = 0
	while line_num <= max_line and (lines[line_num] == '' or lines[line_num][0] == '#'):
		line_num += 1
	
	if line_num >= max_line:
		return parseInfo(False, fault_line=line_num)

	if lines[line_num] != 'schema:':
		return parseInfo(False, fault_line=line_num)
	line_num += 1
	if lines[line_num] != 'steps:':
		return parseInfo(False, fault_line=line_num)
	line_num += 1
	while :
		if lines[line_num] == '-':
			line_num += 1
			if lines[line_num][:5] == 'type:'
				


def parseInfo(flag, **msg):
	return {'result': flag, 'message': msg}


if __name__ == "__main__":
	parse() 