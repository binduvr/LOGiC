
from report_generator.importer import importer as imp
from report_generator.generator import generator as gen
from report_generator.generator import repcompile as comp

def gener(session_id):
  reportdict = imp(session_id)
  z = gen(session_id,reportdict)
  z = comp(session_id)
  return 0
