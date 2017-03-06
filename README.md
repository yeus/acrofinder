# Acronyms and Abbreviations finder

This project is about two things:

* A repository containing a list of acronyms for space-related purposes.
* A script that makes your life easier when searching for acronyms in documents.
  The script can handle all text files (latex, markdown etc..), latex files, pdf-files 
  and docx (word) files

acrofinder:   takes a text file and replaces all occurences 
of acronyms in the acronym list with its counterpart

just edit this file to add new acronyms:

[acronymlist.csv](acronymlist.csv)

# Installation

## Prerequisits

* docx2txt
    - install under linux: 
        
        sudo apt install docx2txt
    
    - windows (anaconda): 
        
        conda config --add channels conda-forge
        
        conda install docx2txt

# How to use

## Latex

just put "acrofind" and "acrofinder.py" and 
into the directory with your latex files.

then do:

    ./acrofind

to find all acronyms in all *.tex files and replace
them with \ac{...}.  An acronyms.tex will also be generated
as which you should include manually into your master-file
like this:

    \input(acronyms.tex)

In the case that you changed your latex file and added more acronyms,
you can just run 

    ./acrofind
    
again, to replace the newly found acronmys. Old acronyms that are already
in\ac{...}-form will be peserved.

## Markdown

    python3 acrofinder.py <markdownfile.md>

## Pdf

    python3 acrofinder.py <pdffile>

## Word

    python3 acrofinder.py <mywordfile.docx> > acronyms.txt

will output a list of acronyms which you can copy paste

## FAQ:

* python throws the error:


# TODO

* substitute acronyms 
* search for possible unknown acronyms (for Example Words that have more than one Capital letter)
