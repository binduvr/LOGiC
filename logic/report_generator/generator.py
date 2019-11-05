'''
Marien Boonman 24-102019
File that takes the reportdict LOGIC and generates a pdf report using LaTeX
a LaTeX compiler should be installed (error message to be programmed)
'''
from shutil import copyfile
import numpy as np
from logic import settings
import time
import os
from logic.report_generator.sections.A_introduction import introduction, generalinfo
from logic.report_generator.sections.B_system import systemlayout
from logic.report_generator.sections.C_systemeconomics import systemeconomics
from logic.report_generator.sections.D_qualitativesection import qualitativeproperties
from logic.report_generator.sections.E_conclusion import conclusion
from logic.report_generator.sections.F_appendix import appendix
from logic.report_generator.sections.G_method import method
from logic.report_generator.sections.H_contributors import contributors

def generate_report(session_id, reportdict):
    enter = '\r\n'
    f = open('logic/report_generator/latex_template/preamble.tex', 'r')
    preamble = f.read()
    f.close()

    # make introduction string from output data
    intro = introduction(reportdict)
    gen = generalinfo(reportdict)

    yourmg, sys = systemlayout(reportdict)

    econ = systemeconomics(reportdict)

    qual = qualitativeproperties(reportdict)

    meth = method(reportdict)

    con = conclusion(reportdict)

    apps = appendix(reportdict)

    conts = contributors(reportdict)
    f = open(settings.OUTPUT_DIRECTORY+session_id+'/report/'+reportdict['reportname']+'.tex', 'w+')
    f.write(preamble)
    f.write(enter)
    f.write(intro)
    f.write(enter)
    f.write(gen)
    f.write(enter)
    f.write(yourmg)
    f.write(enter)
    f.write(sys)
    f.write(enter)
    f.write(econ)
    f.write(enter)
    #f.write(qual)
    #f.write(enter)
    #f.write(con)
    #f.write(enter)
    #f.write('\\newpage '+enter)
    f.write(meth)
    f.write(apps)
    f.write(enter)
    f.write(conts)
    f.write(enter)
    f.write('\\end{multicols}')
    f.write(enter)
    f.write('\\end{document}')

    f.close
