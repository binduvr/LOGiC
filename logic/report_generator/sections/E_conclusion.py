enter = '\r\n'
import os

def conclusion(reportdict):
    #pull stuff from the report dict
    #do we even need a conclusion section?
	con = '\\end{multicols}'+enter+'\\section*{Conclusion}' +enter+ '\\begin{multicols}{2}\\setlength{\\parindent}{0pt}'+ enter + \
	'body text'


	return con
