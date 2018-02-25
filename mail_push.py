import smtplib
import ConfigParser
from email.mime.application import MIMEApplication
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText


def main():	
	config = read_config()

	print 'config was parsed\nnow your email will be sent to:'
	print config.email_list
	print '\n'

	send_email(config)

class Config:
	pass

def read_config():
	config_parser = ConfigParser.ConfigParser()
	config_parser.read('config.txt')

	config = Config()
	config.user = config_parser.get('DEFAULT', 'user')
	config.password = config_parser.get('DEFAULT', 'password')	
	config.email_subject = config_parser.get('DEFAULT', 'subject')
	config.body_path = config_parser.get('DEFAULT', 'body_path')

	config.attachment = Config()
	config.attachment.files = config_parser.get('attachment', 'attachment_files').split('\n')
	# config.attachment.file_name = config_parser.get('attachment', 'attachment_file_name')
	# config.attachment.mime_type = config_parser.get('attachment', 'attachment_mime_type')

	config.email_list = config_parser.get('email_list', 'array').split('\n')

	return config

def send_email(config):
	session = smtplib.SMTP('smtp.gmail.com', 587)
	session.ehlo()
	session.starttls()
	session.login(config.user, config.password)

	# attachment = create_attachment(config)



	for recipient in config.email_list:
		msg = MIMEMultipart()

		msg['Subject'] = config.email_subject
		msg['From'] = config.user		
		msg['To'] = recipient

		body = MIMEText(read_file(config.body_path))
		msg.attach(body)	

		files = config.attachment.files	

		for f in files or []:
			with open(f, "rb") as file:
				part = MIMEApplication(file.read(), Name=basename(f))
        		part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        		msg.attach(part)
        	

		print 'sending message to: ' + recipient
		session.sendmail(config.user, recipient, msg.as_string())
		print 'mail was sent\n'

	session.quit()

def read_file(file_name):
	print 'read file: ' + file_name
	with open(file_name, 'rb') as fp:
		retFile = fp.read()

	return retFile

#run script
main()