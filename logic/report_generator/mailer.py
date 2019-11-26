import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import configparser as cp

import logic.settings as settings

def email_report(session_id, to_address):
	ent = '\r\n'
	cfg = cp.ConfigParser()
	cfg.read(settings.BASE_DIR + "/" + settings.ADMIN_SETTINGS_FILE)
	fromaddr = cfg.get('email_login', 'email_address')
	password = cfg.get('email_login', 'email_password')

	# make mail content
	subject = 'Report on microgrid sizing assessment'

	# body = open(settings.EMAIL_TEXT_FILE, 'r', encoding="utf-8").read()
	# print(body)

	body = "Dear reader, " + ent + ent +\
    'This E-mail contains the report of a microgrid sizing using the OGTC microgrid assessment tool. \n' +\
    'You receive this E-mail because this E-mail address was input as the receiver for this report. \n' +\
    'The results for your simulation will be stored for 30 days.  \n'+\
    'If you would like more information on the simulation and the microgrid in general, please contact the team at at info@offgridtestcenter.nl. \n\n' +\
	'Best regards,'+ent+\
	'On behalf of the team,'+ent+\
	'Our computer'


	filepath = settings.OUTPUT_DIRECTORY + session_id + "/report/" + settings.REPORT_NAME + ".pdf"
	pdf_file = open(filepath, "rb")
	attachment = MIMEBase('application', 'octet-stream')
	attachment.set_payload((pdf_file).read())
	encoders.encode_base64(attachment)
	attachment.add_header('Content-Disposition', "attachment; filename= " + settings.REPORT_NAME + ".pdf")

	#construct mail object
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = to_address
	msg['Subject'] = subject
	# TODO: Can be changed to html for better styling
	msg.attach(MIMEText(body, 'plain'))
	msg.attach(attachment)


	# creates SMTP session
	mail_server = cfg.get('email_settings', 'mail_server')
	mail_port = cfg.get('email_settings', 'mail_port')
	use_tls = cfg.getint('email_settings', 'mail_use_tls')

	server = smtplib.SMTP(mail_server, mail_port)
	if use_tls:
		server.starttls()
	server.login(fromaddr, password)
	text = msg.as_string()

	# sending the mail
	server.sendmail(fromaddr, to_address, text)
