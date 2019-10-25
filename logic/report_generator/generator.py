'''
Marien Boonman 24-102019
File that takes the reportdict LOGIC and generates a pdf report using LaTeX
a LaTeX compiler should be installed (error message to be programmed)
'''
from shutil import copyfile
import numpy as np
import logic.settings as settings
import time
import os
from logic.report_generator.sections.A_introduction import introduction, generalinfo
from logic.report_generator.sections.B_system import systemlayout
from logic.report_generator.sections.C_systemeconomics import systemeconomics
from logic.report_generator.sections.D_qualitativesection import qualitativeproperties
from logic.report_generator.sections.E_conclusion import conclusion
from logic.report_generator.sections.F_appendix import appendix

def generator (session_id, reportdict):
    enter = '/r/n'
    f = open('logic/report_generator/latex_template/preamble.tex', 'r') # is this still valid in the new structure? @Bindu waar kom ik nu uit?
    preamble = f.read()
    f.close()

    # make introduction string from output data
    intro = introduction(reportdict)
    gen = generalinfo(reportdict)
    
    sys = systemlayout(reportdict)

    econ = systemeconomics(reportdict)

    qual = qualitativeproperties(reportdict)
    
    con = conclusion(reportdict)

    apps = appendix(reportdict)

    f = open(settings.OUTPUT_DIRECTIORY+session_id+'/'+reportdict['reportname']+'.tex', 'w+')
    f.write(preamble)
    f.write(enter)
    f.write(intro)
    f.write(enter)
    f.write(gen)
    f.write(enter)
    f.write(sys)
    f.write(enter)
    f.write(econ)
    f.write(enter)
    f.write(qual)
    f.write(enter)
    f.write(con)
    f.write(enter)
    f.write('\\newpage '+enter)
    f.write(apps)
    f.write(enter)
    f.write('\\end{multicols*}')
    f.write(enter)
    f.write('\\end{document}')

    f.close

def repcompile (session_id):	
    copyfile('logic/report_generator/latex_template/logo.jpg', settings.OUTPUT_DIRECTORY+session_id+'/logo.jpg')
    os.system('pdflatex '+ settings.OUTPUT_DIRECTORY+session_id+'/'+reportdict['reportname'] + '.tex')  
    os.system('pdflatex '+ settings.OUTPUT_DIRECTORY+session_id+'/'+reportdict['reportname'] + '.tex')  

def removejunk(session_id):
    folder = settings.OUTPUT_DIRECTORY+session_id+'/'
    filenames = ['',''] #insert names of junkfiles that occur when compiling the pdf (logging stuff)
	
    for name in filenames:
        path = folder+name
    
    os.remove(path)