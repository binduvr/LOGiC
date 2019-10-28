from logic.report_generator.importer import importer
from logic.report_generator.generator import generator
from logic.report_generator.compiler import compiler
from logic.report_generator.mailer import mailer
def generate_report(session_id):
    reportdict = importer(session_id)
    generator(session_id,reportdict) #mod from C4 reportgenerator repgen @@Bindu; moeten dit soort functies altijd een 0 returnen?
    compiler(session_id)
    # TODO: Implement report generation
    return 0

def email_report(session_id, email):
    # mod from C5 mailer or G mailer > find way to safely store password
    # TODO: Email an existing report
    return 0