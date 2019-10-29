import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

import logic.settings as settings

ent = '\r\n'
def email_report(session_id, to_address):
	print('mailing working dir: ' + os.getcwd())
	fromaddr = 'info@offgridtestcenter.nl'
	# password = input('please type your password: ')# TODO take password from server
	password = "CPk5hp1s4"

	# make mail content
	subject = 'Report on microgrid sizing assessment'

	body = "Dear reader, " + ent + ent +\
	'This E-mail contains the report of a microgrid sizing using the LOGiC tool by the Offgrid Test Centre. You receive this E-mail ' + \
	'because this E-mail address was input as the receiver for this report. The inputs for the simulation ' + \
	'will be saved for 30 days. I you want to have more information on the simulation and the microgrid in ' + \
	'general, please contact the team at at info@offgridtestcenter.nl'+ent+ent+\
	'Best regards,'+ent+\
	'On behalf of the LOGiC team,'+ent+\
	'Our computer'


	filepath = settings.OUTPUT_DIRECTORY + session_id + "/report/" + settings.REPORT_NAME + ".pdf"
	attachment = open(filepath, "rb")
	p = MIMEBase('application', 'octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition', "attachment; filename= " + settings.REPORT_NAME + ".pdf")

	#construct mail object
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = to_address
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))
	msg.attach(p)


	# creates SMTP session
	s = smtplib.SMTP('smtp02.hostnet.nl', 587)
	s.starttls()
	s.login(fromaddr, password)
	text = msg.as_string()

	# sending the mail
	s.sendmail(fromaddr, to_address, text)
