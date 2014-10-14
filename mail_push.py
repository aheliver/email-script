import smtplib, os
import email.encoders, email.mime.base
import ConfigParser

from email.MIMEText import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64




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
	config.attachment.path = config_parser.get('attachment', 'attachment_path')	
	config.attachment.file_name = config_parser.get('attachment', 'attachment_file_name')
	config.attachment.mime_type = config_parser.get('attachment', 'attachment_mime_type')

	config.email_list = config_parser.get('email_list', 'array').split('\n')

	return config

def send_email(config):
	session = smtplib.SMTP('smtp.gmail.com', 587)
	session.ehlo()
	session.starttls()
	session.login(config.user, config.password)

	attachment = create_attachment(config)
	body = MIMEText(read_file(config.body_path))

	for recipient in config.email_list:
		msg = email.MIMEMultipart.MIMEMultipart('alternative')
		msg['Subject'] = config.email_subject
		msg['From'] = config.user		
		msg['To'] = recipient
		msg.attach(body)		
		msg.attach(attachment)

		print 'sending message to: ' + recipient
		session.sendmail(config.user, recipient, msg.as_string())
		print 'mail was sent\n'

	session.quit()

def create_attachment(config):	
	fileMsg = MIMEBase('mixed', config.attachment.mime_type)
	fileMsg.set_payload(read_file(config.attachment.path))
	encode_base64(fileMsg)
	fileMsg.add_header('Content-Disposition','attachment;filename=' + config.attachment.file_name)	
	return fileMsg

def read_file(file_name):
	fp = open(file_name, 'rb')
	retFile = fp.read()
	fp.close
	return retFile

#run script
main()