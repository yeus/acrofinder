#!/usr/bin/python
# -*- coding: utf-8 -*-

#script to take a list of acronyms as input and replace
# all acronyms in a text file with \acro{<acronym>}

import re #regular expressions to search and replace acronyms
import sys
from collections import defaultdict
import csv
#import getopt

#repl = "\\acro{}"

#acrolist = re.compile("{(?P<a>.*)}{(?P<b>.*)}")

def buildlatexlist(acrolist):
    latac=r"\begin{acronym}"+"\n"
    for ac in acrolist:
        latac+=r"\acro{"+ac[0]+"}{"+ac[1]+"}"+"\n"
    latac+=r"\end{acronym}"
    return latac

with open("acronymlist.csv", "rt") as acrofile:
    acronyms = csv.reader(acrofile, skipinitialspace=True, delimiter=',')#, quotechar='"')
    acronyms=list(acronyms)
    
#acrostr = acrostr.split("\n")[1:-2]
#acros = [acrolist.search(i).groups() for i in acrostr]

acros = [ac[:2] for ac in acronyms]

#open file
filename = sys.argv[1]
with open(filename) as textfile:
    textstr = textfile.read()
    
##TODO:  if line starts with "\section"  dont replace!!    

newtex = textstr
counter=defaultdict(int)
for acro, acrolong in acros:
    repl = r'\\ac{{{}}}'.format(acro)
    nosec = r'(?![^{]*})' #make sure, regex does no appear between curly braces
    #TODO: do only not replace in section headings between curly braces
    regex = r'(\b'+acro+r'\b)' + nosec  
    newtex, n = re.subn(regex,repl,newtex)
    #if n>0: print("replacements for {}: {}".format(regex,n))
    if n > 0: counter[acro] += n

print(newtex)

with open("acronyms.tex","w") as acrotex:
    acrotex.write(buildlatexlist(acros[1:]))

with open("acro.log","a") as acrolog:
    acrolog.write("found: {}\n".format(dict(counter)))
#print("replacing acros in file: "+ newtex)
#print("found: {}".format(counter))

##class Usage(Exception):
    ##def __init__(self, msg):
        ##self.msg = msg

##def main(argv=None):
    ##if argv is None:
        ##argv = sys.argv
    ##try:
        ##try:
            ##opts, args = getopt.getopt(argv[1:], "h", ["help"])
        ##except getopt.error, msg:
             ##raise Usage(msg)
        ### more code, unchanged
    ##except Usage, err:
        ##print >>sys.stderr, err.msg
        ##print >>sys.stderr, "for help use --help"
        ##return 2

##if __name__ == "__main__":
    ##sys.exit(main())
