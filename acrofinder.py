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

#TODO:  CLI mit python fire

def buildlatexlist(acrolist):
    latac=r"\begin{acronym}"+"\n"
    for ac in acrolist:
        latac+=r"\acro{"+ac[0]+"}{"+ac[1]+"}"+"\n"
    latac+=r"\end{acronym}"
    return latac

def load_acros():
    try:
    
        with open("acronymlist.csv", "rt") as acrofile:
            acronyms = csv.reader(acrofile, skipinitialspace=True, delimiter=',')#, quotechar='"')
            acronyms=list(acronyms)
        
        for ac in acronyms:
            if len(ac) < 2: #csv should have more than two rows
                print("too few values in row: {}".format(ac))
                print("have you checked the csv file for consistency?\n\n\n")
                raise
        
        #acrostr = acrostr.split("\n")[1:-2]
        #acros = [acrolist.search(i).groups() for i in acrostr]

        acros = [ac[:2] for ac in acronyms][1:]
        
        acrodict = {i : j for i,j in acros}
        acroset = set(i for i,j in acros) 
    except Exception as e: 
        print("error, processing acronymlist.csv: {}".format(traceback.format_exc()))
        #raise
        
    return acrodict, acroset
  
def get_txt_data(filename):
    from subprocess import call, check_output
    import os
    from collections import Counter
    from itertools import chain

    if filename[-3:]=="tex": filetype = "tex"
    elif filename[-2:]=="md": filetype= "md"
    elif filename[-4:]=="docx": filetype= "docx"
    elif filename[-3:]=="pdf": filetype="pdf"

    #call(["pandoc",filename,"-s","-o","tmp.md"])
    #call(["pandoc","tmp.odt","-o","tmp.md"])
    if filetype=='md':
        with open(filename) as mdfile:
            data = mdfile.read()
    else:
        if filetype=="docx":
            if os.name == 'posix': 
                try:
                    call(["docx2txt", filename, "tmp"])
                except Exception as e:
                    print("have you installed docx2txt? try: \n\n    >> sudo apt install -y docx2txt")
                    raise
            
                with open("tmp",encoding="utf-8") as myfile:
                    data = myfile.read()#.replace('\n','')
                    
            elif os.name == 'nt':  #@info needs:  "pip install docx2txt"
                import docx2txt
                data = docx2txt.process(filename)
        elif filetype == "pdf":
            try:
                data = check_output(["pdf2txt",filename])
                #print(data)
            except Exception as e:
                print("have you installed pdf2txt? try: \n\n    >> sudo apt install -y python-pdfminer")
                raise
            
    if filetype=='docx' and os.name == 'posix': 
        os.remove("tmp")
    
    return data

def createacrolistfromdoc(filename, filetype):
    #STATIC_DEPS=true pip install lxml falls: ImportError: libiconv.so.2: cannot open shared object file: No such file or directory
    #https://python-docx.readthedocs.io/en/latest/index.html
    #import docx
    #document = docx.Document(filename)
        
    #pandoc required
    
    acrodict, acroset = load_acros()
    
    data = get_txt_data(filename)
    #words = [w.strip(".,:()[]") for w in data.split()]
    words = re.findall(r"[\w']+", data)
    unique=set(words)
    
    #print(list(map(str.split, data)))
    occuring_acros = unique.intersection(acroset)
    
    if filetype=="pdf": acrotable = "\n".join(["|" + acr + "\t |"+ acrodict[acr] + "|" for acr in sorted(occuring_acros)])
    else: acrotable = "\n".join([acr + "\t "+ acrodict[acr] for acr in sorted(occuring_acros)])
    
    print(acrotable)

def searchunknownacros(filename, filetype):
    acrodict, acroset = load_acros()
    
    data = get_txt_data(filename)
    #words = [w.strip(".,:()[]") for w in data.split()]
    words = re.findall(r"[\w']+", data)
    unique=set(words)
    
    #print(list(map(str.split, data)))
    occuring_acros = unique.intersection(acroset)
    
    unknowns=[]
    for word in unique-acroset:
        cnum = sum(1 for c in word if c.isupper())
        if cnum > 1: 
            unknowns.append(word)
            #if 
            #print(word,word in occuring_acros)
        
        
    print("potential unknown acronyms: \n{}".format("\n".join(sorted(unknowns))))
    
def replaceintexfiles(filename):

    #open file
    with open(filename) as textfile:
        textstr = textfile.read()
        
    ##TODO:  if line starts with "\section"  dont replace!!    

    acrodict, acroset = load_acros()

    newtex = textstr
    counter=defaultdict(int)
    for acro, acrolong in acrodict.items():
        repl = r'\\ac{{{}}}'.format(acro)
        nosec = r'(?![^{]*})' #make sure, regex does no appear between curly braces
        #TODO: do only not replace in section headings between curly braces
        regex = r'(\b'+acro+r'\b)' + nosec  
        newtex, n = re.subn(regex,repl,newtex)
        #if n>0: print("replacements for {}: {}".format(regex,n))
        if n > 0: counter[acro] += n

    print(newtex)

    with open("acronyms.tex","w") as acrotex:
        acrotex.write(buildlatexlist(acrodict.items()))

    with open("acro.log","a") as acrolog:
        acrolog.write("found: {}\n".format(dict(counter)))

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            filename = sys.argv[1]
            
            #print("fileending: {}".format(filename[-3:]))
            if filename[-3:]=="tex":
                #print("replacing {}".format(filename[-3:]))
                replaceintexfiles(filename)
            elif filename[-3:]=="pdf":
                createacrolistfromdoc(filename,filename[-3:])
                print("\n\n")
                searchunknownacros(filename,filename[-3:])
            elif filename[-2:]=="md":
                createacrolistfromdoc(filename,filename[-2:])
                print("\n\n")
                searchunknownacros(filename,filename[-2:])
            elif filename[-4:]=="docx":
                #print("creating acronymlist!")
                createacrolistfromdoc(filename,filename[-4:])
                print("\n\n")
                searchunknownacros(filename,filename[-4:])
                
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        # more code, unchanged
    except Usage as err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
