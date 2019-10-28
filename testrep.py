
from logic.report_generator.importer import importer
from logic.report_generator.generator import generator
from logic.report_generator.compiler import compiler

session_id = '20191028144259'
reportdict = importer(session_id)
generator(session_id,reportdict)
compiler(session_id,reportdict)
