from shutil import copyfile
from logic import settings
import os
def compile(session_id,reportdict):
    copyfile('logic/report_generator/latex_template/logo.png', settings.OUTPUT_DIRECTORY+session_id+'/report/logo.png')
    copyfile('data/outputs/'+session_id+'/inputs/per_unit_pv_generation.png', settings.OUTPUT_DIRECTORY+session_id+'/report/per_unit_pv_generation.png')
    copyfile('data/outputs/'+session_id+'/inputs/per_unit_wind_generation.png', settings.OUTPUT_DIRECTORY+session_id+'/report/per_unit_wind_generation.png')
    # copyfile('logic/data/outputs/'+session_id+'/electricity_mg/electricity_mg.png', settings.OUTPUT_DIRECTORY+session_id+'/report/electricity_mg.png')
    # copyfile('logic/data/outputs/'+session_id+'/electricity_mg/electricity_mg_4days.png', settings.OUTPUT_DIRECTORY+session_id+'/report/electricity_mg_4days.png')
    cwd = os.getcwd()
    os.chdir(settings.OUTPUT_DIRECTORY + session_id + '/report')
    os.system('pdflatex '+reportdict['reportname']+'.tex')
    os.system('pdflatex '+reportdict['reportname']+'.tex')
    os.chdir(cwd)

def removejunk(session_id):
    folder = settings.OUTPUT_DIRECTORY+session_id+'/'
    filenames = ['',''] #insert names of junkfiles that occur when compiling the pdf (logging stuff)

    for name in filenames:
        path = folder+name
        os.remove(path)
