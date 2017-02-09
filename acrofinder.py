#!/usr/bin/python
# -*- coding: utf-8 -*-

#script to take a list of acronyms as input and replace
# all acronyms in a text file with \acro{<acronym>}

import re #regular expressions to search and replace acronyms
import sys
from collections import defaultdict
import csv
import traceback  #for error reporting
#import getopt

#repl = "\\acro{}"

#acrolist = re.compile("{(?P<a>.*)}{(?P<b>.*)}")

def buildlatexlist(acrolist):
    latac=r"\begin{acronym}"+"\n"
    for ac in acrolist:
        latac+=r"\acro{"+ac[0]+"}{"+ac[1]+"}"+"\n"
    latac+=r"\end{acronym}"
    return latac

def load_acrolist():
    with open("acronymlist.csv", "rt") as acrofile:
        acronyms = csv.reader(acrofile, skipinitialspace=True, delimiter=',')#, quotechar='"')
        acronyms=list(acronyms)
    
    for ac in acronyms:
        if len(ac) < 2:
            print("too few values in row: {}".format(ac))
            raise
    
    #acrostr = acrostr.split("\n")[1:-2]
    #acros = [acrolist.search(i).groups() for i in acrostr]

    acros = [ac[:2] for ac in acronyms]
    return acros[1:]
    

def createacrolistfromdoc(filename):
    #STATIC_DEPS=true pip install lxml falls: ImportError: libiconv.so.2: cannot open shared object file: No such file or directory
    #https://python-docx.readthedocs.io/en/latest/index.html
    #import docx
    #document = docx.Document(filename)
        
    #pandoc required
    
    from subprocess import call
    import os
    from collections import Counter
    from itertools import chain
    
    #call(["pandoc",filename,"-s","-o","tmp.md"])
    #call(["pandoc","tmp.odt","-o","tmp.md"])
    call(["docx2txt", filename, "tmp"])
    
    try:
        acros = load_acrolist()
        acrodict = {i : j for i,j in acros}
    except Exception as e: 
        print("error, processing acronymlist.csv: {}".format(traceback.format_exc()))
        
    acroset = (i for i,j in acros)
    
    counted=0
    #with open(filename,encoding="utf-8") as myfile:
    with open("tmp",encoding="utf-8") as myfile:
        data = myfile.read()#.replace('\n','')
        unique=set(data.split())
        #counted = Counter(data.split())
    
    #print(list(map(str.split, data)))
    occuring_acros = unique.intersection(acroset)
    
    acrotable = "\n".join([acr + "\t "+ acrodict[acr] for acr in occuring_acros])
    
    print(acrotable)
    #print(acrodict)
    
    os.remove("tmp")
    

def replaceintexfiles(filename):

    #open file
    with open(filename) as textfile:
        textstr = textfile.read()
        
    ##TODO:  if line starts with "\section"  dont replace!!    

    acros = load_acrolist()

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
        acrotex.write(buildlatexlist(acros))

    with open("acro.log","a") as acrolog:
        acrolog.write("found: {}\n".format(dict(counter)))

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    import getopt

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            
            filename = sys.argv[1]
            
            #print("fileending: {}".format(filename[-3:]))
            if filename[-3:]=="tex":
                #print("replacing {}".format(filename[-3:]))
                replaceintexfiles(filename)
            elif filename[-4:]=="docx":
                #print("creating acronymlist!")
                createacrolistfromdoc(filename)
                
        except getopt.error as  msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage as err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
