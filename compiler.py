from argparse import ArgumentParser,FileType

import re

def cleanup(string):
	string = re.sub("[^()<>[\]{}]","",string)
	return string

def indent(string):
	#Around these parts we indent with tabs
	return "\n\t".join(string.split("\n"))

def compile(string):
	pass

if __name__ == "__main__":
	parser = ArgumentParser(description="Compiles Brain-Flak code into C++")
	parser.add_argument("bfsource",metavar="source",action="store",help="Name of the file Brain-Flak source code to be compiled.",type=file)
	parser.add_argument("dest",metavar="destination",action="store",help="Name of the destination where compiled C++ will be written.",type=FileType("w"))
	args = parser.parse_args()
	args.bfsource.read()
