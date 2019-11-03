from logic.report_generator import importer as importer
from logic.report_generator import generator as generator
from logic.report_generator import compiler as compiler
# Create report
session_id = '57'
reportdict = importer.import_data(session_id)
generator.generate_report(session_id, reportdict)
compiler.compile(session_id, reportdict)
