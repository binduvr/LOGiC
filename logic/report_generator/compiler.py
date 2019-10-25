import os
import logic.settings as settings
def compiler(session_id,reportdict):
    os.system('pdflatex '+settings.OUTPUT_DIRECTORY+'/'+reportdict['reportname']+'.tex')
    os.system('pdflatex '+settings.OUTPUT_DIRECTORY+'/'+reportdict['reportname']+'.tex')