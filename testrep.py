
from logic.report_generator.importer import importer
from logic.report_generator.generator import generator as gen
from logic.report_generator.generator import repcompile as comp

def gener(session_id):
  reportdict = importer(session_id)
  z = gen(session_id,reportdict)
  z = comp(session_id)
  return 0
