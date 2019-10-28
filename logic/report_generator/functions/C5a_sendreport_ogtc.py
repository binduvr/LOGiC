import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import D41_symbolfunctions as sym
import os
def mailreport(input_dict,output_dict):
	ent = sym.enterkey()
	print('mailing working dir: ' + os.getcwd())
	fromaddr = 'info@offgridtestcenter.nl'		# still from Gmail; smtpserver for official address unknown
	password = input('please type your password: ')
	toaddr = input_dict['user_email']

	# make mail content
	subject = 'Report on microgrid sizing assessment '+ input_dict['project_name'] #subject

	body = "Dear reader, " + ent + ent +\
	'This E-mail contains the report of a microgrid sizing using the LOGiC tool by the Offgrid Test Centre. You receive this E-mail ' + \
	'because this E-mail address was input as the receiver for this report. The inputs for the simulation ' + \
	'will be saved for 30 days. I you want to have more information on the simulation and the microgrid in ' + \
	'general, please contact the team at at info@offgridtestcentre.nl'+ent+ent+\
	'Best regards,'+ent+\
	'On behalf of the LOGiC team,'+ent+\
	'Our computer'


	filename = output_dict['reportname'] + '.pdf'
	attachment = open(filename, "rb")
	p = MIMEBase('application', 'octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition', "attachment; filename= " + filename)

	#construct mail object
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))
	msg.attach(p)


	# creates SMTP session
	s = smtplib.SMTP('smtp02.hostnet.nl', 587)
	s.starttls()
	s.login(fromaddr, password)
	text = msg.as_string()

	# sending the mail
	s.sendmail(fromaddr, toaddr, text)
