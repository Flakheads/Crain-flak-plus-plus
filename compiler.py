from argparse import ArgumentParser,FileType

import re

def cleanup(string):
	string = re.sub("[^()<>[\]{}]","",string)
	return string

def indent(string):
	#Around these parts we indent with tabs
	return "\n\t".join(string.split("\n"))

def balancedQ(string):
	#Determines if a string is balanced
	matches = ["()","[]","<>","{}"]
	scope = []
	for character in string:
		if character in "([<{":
			scope.append(character)
		elif character in ")]>}":
			if scope:
				if scope[-1]+character in matches:
					scope.pop()
				else:return False
			else:return False
		else:return False
	return scope == []

def getdepth(string):
	#Gets the depth of a balanced string
	scope = 0
	maxscope = 0
	for character in string:
		if character in "([{<":
			scope += 1
		elif character in ")]}>":
			scope -= 1
		maxscope = max(scope,maxscope)
	return maxscope

def semicompile(string):
	for target, goal in [("()","A"),("{}","B"),("<>","C"),("[]","D")]:
		string = string.replace(target,goal)
	return string

def compile(string):
	string = semicompile(string)
	depth = getdepth(string)
	code = "#include<iostream>\n#include<vector>\nint main(){%s}"
	code = code % ("long scope [%d] = { };long scopeHeight = 0;\n"%(depth+1)+"%s")
	code = code % ("std::vector<long> * left = new std::vector<long>;std::vector<long> * right = new std::vector<long>;std::vector<long> * temp = NULL;\n"+"%s"+"delete left;delete right;")
	code = code % ("%s"+"for(std::vector<long>::const_iterator i=left->begin();i!=left->end();++i){std::cout<<*i<<std::endl;}")
	replacements = {
		"A": "scope[scopeHeight]+=1;\n",
		"B": "if(!left->empty()){scope[scopeHeight]+=left->back();left->pop_back();}",
		"C": "temp = left;left = right;right = temp;",
		"D": "scope[scopeHeight]+=left->size;",

		"[": "scopeHeight+=1;scope[scopeHeight]=0;\n",
		"<": "scopeHeight+=1;scope[scopeHeight]=0;\n",
		"(": "scopeHeight+=1;scope[scopeHeight]=0;\n",

		"]": "scopeHeight-=1;scope[scopeHeight]-=scope[scopeHeight+1];scope[scopeHeight+1]=0;\n",
		">": "scope[scopeHeight]=0;scopeHeight-=1;\n",
		")": "left->push_back(scope[scopeHeight]);scopeHeight-=1;scope[scopeHeight]+=scope[scopeHeight+1];scope[scopeHeight+1]=0;\n",

		"{": "while(not(left->empty() or left->back()==0)){\n",
		"}": "}\n",
	}
	string = "".join(replacements[x]for x in string)
	code = code % string
	return code
if __name__ == "__main__":

	parser = ArgumentParser(description="Compiles Brain-Flak code into C++")
	parser.add_argument("bfsource",metavar="source",action="store",help="Name of the file Brain-Flak source code to be compiled.",type=file)
	parser.add_argument("dest",metavar="destination",action="store",help="Name of the destination where compiled C++ will be written.",type=FileType("w"))
	args = parser.parse_args()
	source = cleanup(args.bfsource.read())
	args.dest.write(compile(source))
